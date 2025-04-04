<script setup lang="ts">
import { ref, onMounted } from "vue";
import * as echarts from "echarts";
import data from "@/assets/confidence-band.json";

// UI state
const chartRef = ref();
let myChart: echarts.ECharts;

const modelOptions = ["Moving Average", "Exponential Smoothing", "Holt-Winters"];
const selectedModel = ref("Moving Average");

const trend = ref(true);
const seasonality = ref(true);
const smoothing = ref(0.5);

function submitForecast() {
  console.log("Selected model:", selectedModel.value);
  console.log("Trend:", trend.value, "Seasonality:", seasonality.value, "Smoothing:", smoothing.value);
  // Here you would normally trigger the backend forecast logic
  drawChart(); // for demo purpose
}

function drawChart() {
  myChart.showLoading();
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
        lineStyle: { color: "#666" },
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
        areaStyle: { color: "rgba(200, 200, 200, 0.3)" },
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
}

onMounted(() => {
  myChart = echarts.init(chartRef.value);
  drawChart();
});
</script>

<template>
  <div style="padding: 20px; color: white">
    <!-- 控件 -->
    <div style="display: flex; flex-wrap: wrap; align-items: center; gap: 12px; margin-bottom: 20px">
      <label style="color: white;">Model:</label>
      <select v-model="selectedModel" style="background: #111; color: #fff; border: 1px solid #555; padding: 4px 8px">
        <option v-for="model in modelOptions" :key="model" :value="model">{{ model }}</option>
      </select>

      <label style="color: white;">Trend:</label>
      <input type="checkbox" v-model="trend" />

      <label style="color: white;">Seasonality:</label>
      <input type="checkbox" v-model="seasonality" />

      <label style="color: white;">Smoothing:</label>
      <input type="range" min="0" max="1" step="0.1" v-model="smoothing" />

      <button @click="submitForecast" style="background: #00aaff; color: white; border: none; padding: 6px 14px; border-radius: 4px; cursor: pointer">
        Submit
      </button>
    </div>

    <!-- 图表容器 -->
    <div ref="chartRef" style="width: 100%; height: 350px" />
  </div>
</template>

<style scoped>
select,
input,
button {
  padding: 5px 10px;
  font-size: 14px;
}
button {
  background-color: #00aaff;
  color: white;
  border: none;
  cursor: pointer;
}
</style>