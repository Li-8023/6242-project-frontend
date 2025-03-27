<script setup lang="ts">
import { onMounted, ref } from "vue";
import * as echarts from "echarts";
import data from "@/assets/confidence-band.json";

const chartRef = ref();
let myChart: echarts.ECharts;

interface DataItem {
  l: number;
  u: number;
  date: string;
  value: number;
}

onMounted(() => {
  myChart = echarts.init(chartRef.value);
  myChart.showLoading();
  console.log(data);
  myChart.hideLoading();

  const base = -Math.floor(
    data.reduce((min, val) => Math.min(min, val.l), Infinity)
  );

  const option: echarts.EChartsOption = {
    title: {
      text: "Sales Forecasting",
      subtext: "Trend, Seasonality, and Confidence Bands",
      left: "center",
      textStyle: { color: "#fff" },
      subtextStyle: { color: "#ccc" },
    },
    tooltip: {
      trigger: "axis",
      axisPointer: {
        type: "cross",
        animation: false,
        label: {
          backgroundColor: "#ccc",
          borderColor: "#aaa",
          borderWidth: 1,
          color: "#222",
        },
      },
      formatter(params: any) {
        return (
          `<strong>${params[2].name}</strong><br/>` +
          `Forecasted Sales Change: ` +
          ((params[2].value - base) * 100).toFixed(1) +
          "%"
        );
      },
    },
    grid: {
      left: "3%",
      right: "4%",
      bottom: "3%",
      containLabel: true,
    },
    xAxis: {
      type: "category",
      data: data.map((item) => item.date),
      axisLabel: {
        color: "#fff",
        formatter(value: string, idx: number) {
          const date = new Date(value);
          return idx === 0
            ? value
            : [date.getMonth() + 1, date.getDate()].join("-");
        },
      },
      boundaryGap: false,
    },
    yAxis: {
      axisLabel: {
        color: "#fff",
        formatter(val: number) {
          return (val - base) * 100 + "%";
        },
      },
      axisPointer: {
        label: {
          formatter(params: any) {
            return ((params.value - base) * 100).toFixed(1) + "%";
          },
        },
      },
      splitLine: {
        lineStyle: {
          color: "#666",
        },
      },
    },
    series: [
      {
        name: "Lower Bound",
        type: "line",
        data: data.map((item) => item.l + base),
        lineStyle: { opacity: 0 },
        stack: "confidence-band",
        symbol: "none",
      },
      {
        name: "Confidence Interval",
        type: "line",
        data: data.map((item) => item.u - item.l),
        lineStyle: { opacity: 0 },
        areaStyle: { color: "#999" },
        stack: "confidence-band",
        symbol: "none",
      },
      {
        name: "Forecasted Sales",
        type: "line",
        data: data.map((item) => item.value + base),
        itemStyle: { color: "#00fdfa" },
        showSymbol: false,
      },
    ],
  };

  myChart.setOption(option);
});
</script>

<template>
  <div ref="chartRef" style="width: 100%; height: 400px" />
</template>