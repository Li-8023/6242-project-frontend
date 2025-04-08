<script setup lang="ts">
import { ref, onMounted } from "vue";
import * as echarts from "echarts";
import data from "@/assets/confidence-band.json";

// UI state
const chartRef = ref();
let myChart: echarts.ECharts;

const modelOptions = [
  "Moving Average",
  "Exponential Smoothing",
  "Holt-Winters",
];
const selectedModel = ref("Moving Average");

const isForecastDrawerOpen = ref(false);

const make = ref("");
const state = ref("");
const seller = ref("");
const yORm = ref(true);
const season = ref(false);
const season_period = ref(0);

function submitForecast() {
  const payload = {
    make: make.value || null,
    state: state.value || null,
    seller: seller.value || null,
    yORm: yORm.value,
    season: season.value,
    season_period: season_period.value,
  };

  console.log("Holt-Winters payload:", payload);

  drawChart();
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
      // subtext: "Trend, Seasonality, and Confidence Bands",
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
    <!-- 图表容器 -->
    <div ref="chartRef" style="width: 100%; height: 350px" />
    <!-- Forecast Button -->
    <div class="flex justify-center mt-6">
      <button
        @click="isForecastDrawerOpen = true"
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
      >
        Set Forecast Options
      </button>
    </div>

    <!-- Overlay -->
    <div
      v-if="isForecastDrawerOpen"
      class="fixed inset-0 bg-black bg-opacity-50 z-40"
      @click.self="isForecastDrawerOpen = false"
    />

    <!-- Drawer Panel -->
    <div
      v-if="isForecastDrawerOpen"
      class="fixed top-0 right-0 w-80 h-full bg-gray-900 text-white p-6 z-50 shadow-lg transition-transform duration-300"
    >
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-lg font-semibold">Holt-Winters Options</h3>
        <button
          @click="isForecastDrawerOpen = false"
          class="text-white text-2xl"
        >
          &times;
        </button>
      </div>

      <!-- Form Fields -->
      <div class="space-y-4">
        <div>
          <label class="block text-sm mb-1">Make:</label>
          <input
            v-model="make"
            placeholder="e.g. Kia"
            class="w-full p-2 rounded bg-gray-800 border border-gray-600 text-white"
          />
        </div>

        <div>
          <label class="block text-sm mb-1">State:</label>
          <input
            v-model="state"
            placeholder="e.g. ca"
            class="w-full p-2 rounded bg-gray-800 border border-gray-600 text-white"
          />
        </div>

        <div>
          <label class="block text-sm mb-1">Seller:</label>
          <input
            v-model="seller"
            placeholder="e.g. avis tra"
            class="w-full p-2 rounded bg-gray-800 border border-gray-600 text-white"
          />
        </div>

        <div class="flex items-center space-x-2">
          <input
            type="checkbox"
            v-model="yORm"
            class="form-checkbox text-blue-500"
          />
          <label>Enable yORm</label>
        </div>

        <div class="flex items-center space-x-2">
          <input
            type="checkbox"
            v-model="season"
            class="form-checkbox text-blue-500"
          />
          <label>Enable seasonality</label>
        </div>

        <div>
          <label class="block text-sm mb-1">Season Period:</label>
          <input
            type="number"
            v-model="season_period"
            class="w-full p-2 rounded bg-gray-800 border border-gray-600 text-white"
          />
        </div>
      </div>

      <!-- Submit -->
      <button
        class="mt-6 w-full bg-blue-600 hover:bg-blue-700 transition py-2 rounded text-white font-semibold"
        @click="
          () => {
            submitForecast();
            isForecastDrawerOpen = false;
          }
        "
      >
        Submit
      </button>
    </div>
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
.input-style {
  background: #111;
  color: #fff;
  border: 1px solid #555;
  padding: 6px 10px;
  border-radius: 4px;
}
.submit-btn {
  background-color: #00aaff;
  color: white;
  border: none;
  padding: 6px 14px;
  border-radius: 4px;
  cursor: pointer;
}
</style>
