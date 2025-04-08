'''
主要fastapi接口文件
命令行使用
uvicorn app:app --reload
代码可以启动这个fastapi的app
注意无法从浏览器端口进入，需要右键index.html文件选择用浏览器打开

1）prediction
车价预测

这里只用odometer和condition
其他变量因为做了binary categorical的处理失去了实际意义
变量重要性的可视化部分可以删除，也可以联系我和萱，我们给一个固定不变的伪重要性

输入odometer和condition，再点击predict，可以给出四种模型的预测值和置信区间
其中XGB算法每次预测的时候会调用整棵树结构给出一个值，所以不会产生置信区间
predict会给出来一个字典，字典的key是模型种类，value是[预测值,(置信区间下限，置信区间上限)]

2) holt-winters
销量预测

首先先过一个筛选器，然后对筛选以后的表格进行回归
这个筛选器目前写了的是：make, state, seller这三个字符串字段
如果有需要，我们还可以对odometer和condition这两个数值变量进行筛选
页面中这三个框都空着就是不筛选
若筛选出来的表格总长度小于10000，会提示无法用模型进行回归

Enable yORm: 默认勾选，勾选是用1995-2014年预测2015-2019年
不勾选是按月份预测，数据集天然确实每一年的7-11月部分，所以每一年是1-6月和12月，每一年有7个数据点

Enable seasonality：如果yORm勾选了，这个seasonality无效，也就是说只有跑月份回归才有用
另外如果勾选了，必须输入season period

原来我们图表里面的smooth值可以换成season period
原因是咱们模型会自动选择最优的smooth值，但是season period是可以人为选择的
'''

import math

from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd
import os

# -------------------------
# 加载模型与工具
# -------------------------

model_path = "car_models.joblib"

saved_data = joblib.load(model_path)
models = saved_data['models']
scaler = saved_data['scaler']
numeric_features = saved_data['numeric_features']
trained_features = saved_data['trained_features']

# -------------------------
# FastAPI App 配置
# -------------------------

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 可以改为 ["http://localhost:3000"] 限定前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# 请求数据模型
# -------------------------

class PredictRequest(BaseModel):
    features: Dict[str, Any]

# -------------------------
# 预测接口
# -------------------------

@app.post("/predict")
def predict_price(request: PredictRequest):
    input_data = request.features

    # 构造完整输入（缺省项设为0）
    full_input = {feature: 0 for feature in trained_features}
    for k, v in input_data.items():
        if k in full_input:
            full_input[k] = v

    input_df = pd.DataFrame([full_input])

    # 特征缩放
    input_df[numeric_features] = scaler.transform(input_df[numeric_features])

    # 模型预测 + 置信区间
    results = {}

    for model_name, model in models.items():
        X_input = input_df.values
        pred = model.predict(X_input)[0]

        try:
            if model_name == 'RF':
                bootstrap_preds = [tree.predict(X_input)[0] for tree in model.estimators_]
                lower = np.percentile(bootstrap_preds, 2.5)
                upper = np.percentile(bootstrap_preds, 97.5)

            elif model_name == 'LGBM':
                num_iterations = model.n_estimators_
                bootstrap_preds = [
                    model.predict(X_input, num_iteration=i + 1)[0]
                    for i in range(num_iterations)
                ]
                lower = np.percentile(bootstrap_preds, 2.5)
                upper = np.percentile(bootstrap_preds, 97.5)

            elif model_name == 'LR':
                half = 8740.7353 * 1.96
                lower, upper = pred - half, pred + half  # 简化处理
            else:
                lower = upper = pred
        except Exception:
            lower = upper = pred

        results[model_name] = [float(pred), [float(lower), float(upper)]]

    return results




# -------------------------
# Holt-Winters 接口部分
# -------------------------

dt = pd.read_csv('car_prices.csv')

# DATE PROCESSING

# extract exact date
dt['parsed_date'] = pd.to_datetime(dt['saledate'], errors='coerce', utc=True)
dt = dt.dropna(subset=['parsed_date'])
dt['date'] = dt['parsed_date'].dt.strftime('%Y-%m-%d')
dt['date'] = pd.to_datetime(dt['date'])

# delete useless columns
dt = dt.drop(columns = ['saledate','parsed_date'])

# extract year, week and day
dt['YEAR'] = dt['year']
dt = dt.drop(columns = ['year'])

dt['month'] = dt['date'].dt.month
dt['day'] = dt['date'].dt.day
dt['weekday'] = dt['date'].dt.day_name()

# real date
dt['DATE'] = pd.to_datetime(dt[['YEAR', 'month', 'day']])
dt = dt.drop(columns = ['date','model','trim','body','transmission','vin','color','interior','mmr'])

# 定义请求数据结构
class HoltWinterRequest(BaseModel):
    make: str = None
    state: str = None
    seller: str = None
    yORm: bool = True
    season: bool = False
    season_period: int = 0

from Holtwinters import holtwinters

@app.post("/holtwinter")
def holtwinter_api(request: HoltWinterRequest):
    try:
        result = holtwinters(
            data=dt,
            make=request.make,
            state=request.state,
            seller=request.seller,
            yORm=request.yORm,
            season=request.season,
            season_period=request.season_period
        )
        return result
    except Exception as e:
        return {"error": str(e)}