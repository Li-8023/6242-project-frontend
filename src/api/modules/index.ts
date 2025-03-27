import {GET,POST,FILE,FILEPOST,PUT,GETNOBASE} from "../api";
const indexUrl=  {
    'leftTop':'/bigscreen/countDeviceNum',//左上
    'leftCenter':'/bigscreen/countUserNum',//左中
    "centerMap":"/bigscreen/centerMap",
    "centerBottom":"/bigscreen/installationPlan",

    'leftBottom':"/bigscreen/leftBottom", //左下
    'rightTop':"/bigscreen/alarmNum", //Dealer Region Aggregation
    'rightBottom':'/bigscreen/rightBottom',//右下 
    'rightCenter':'/bigscreen/ranking',// 报警排名
}

export default indexUrl

/**左上--Car Segmentation */
export const countDeviceNum=(param:any={})=>{
    return GET(indexUrl.leftTop,param)
}

/**左中--用户总览 */
export const countUserNum=(param:any={})=>{
    return GET(indexUrl.leftCenter,param)
}

/**左下--Sales Forecasting */
export const leftBottom=(param:any={})=>{
    return GET(indexUrl.leftBottom,param)
}

/**中上--地图 */
export const centerMap=(param:any={})=>{
    return GET(indexUrl.centerMap,param)
}

/**中下--安装计划 */
export const installationPlan=(param:any={})=>{
    return GET(indexUrl.centerBottom,param)
}

/**右上--Dealer Region Aggregation */
export const alarmNum=(param:any={})=>{
    return GET(indexUrl.rightTop,param)
}

/**右中--报警排名 */
export const ranking=(param:any={})=>{
    return GET(indexUrl.rightCenter,param)
}

/**右下--设备状态 */
export const rightBottom=(param:any={})=>{
    return GET(indexUrl.rightBottom,param)
}