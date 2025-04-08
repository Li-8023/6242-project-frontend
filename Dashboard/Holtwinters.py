import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def holtwinters(data, make=None, state=None, seller=None, yORm=True, season=None, season_period=0):
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    import matplotlib.pyplot as plt

    df = data.copy()
    if make:
        df = df[df['make'] == make]
    if state:
        df = df[df['state'] == state]
    if seller:
        df = df[df['seller'] == seller]

    if len(df) < 10000:
        return 'No enough records'

    if yORm:
        # 年预测
        dt_1 = df
        dt_2 = dt_1[~dt_1['YEAR'].isin([
            1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990,
            1991, 1992, 1993, 1994, 2015
        ])]
        pivot_year = dt_2.pivot_table(index='YEAR', aggfunc='size')
        pivot_year.index = pd.to_datetime(pivot_year.index, format='%Y')
        result_history = pivot_year.to_dict()

        model = ExponentialSmoothing(pivot_year, trend='add', seasonal=None)
        fit = model.fit()
        forecast = fit.forecast(5)
        result_forecast = forecast.to_dict()

        return {
            'history': result_history,
            'forecast': result_forecast
        }

    else:
        # 月预测
        if season is not None:
            if season_period == 0:
                return 'Please check season_period'
            seasonality = 'add'
        else:
            seasonality = None

        dt_1 = df
        dt_2 = dt_1[~dt_1['YEAR'].isin([
            1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990,
            1991, 1992, 1993, 1994, 2015
        ])]

        pivot_month = dt_2.pivot_table(index=['YEAR', 'month'], aggfunc='size').reset_index(name='count')
        pivot_month = pivot_month[pivot_month['month'] != 7].reset_index(drop=True)
        pivot_month['date'] = pd.to_datetime(pivot_month[['YEAR', 'month']].assign(DAY=1))
        pivot_month = pivot_month.sort_values('date')

        result_history = dict(zip(pivot_month['date'], pivot_month['count']))

        model = ExponentialSmoothing(
            pivot_month['count'],
            trend='add',
            seasonal=seasonality,
            seasonal_periods=season_period if seasonality else None
        )
        fit = model.fit()
        forecast = fit.forecast(35)

        last_date = pivot_month['date'].max()
        future_dates = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=35, freq='MS')

        df_forecast = pd.DataFrame({
            'date': future_dates,
            'count': forecast.values
        })
        df_forecast['count'] = df_forecast['count'].clip(lower=0)
        df_forecast['YEAR'] = df_forecast['date'].dt.year
        df_forecast['month'] = df_forecast['date'].dt.month

        result_forecast = dict(zip(df_forecast['date'], df_forecast['count']))

        return {
            'history': result_history,
            'forecast': result_forecast
        }