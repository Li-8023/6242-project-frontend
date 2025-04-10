<script setup lang="ts">
import { ref, onMounted } from "vue";
import * as echarts from "echarts";
// import data from "@/assets/confidence-band.json";

// UI state
const chartRef = ref();
let myChart: echarts.ECharts;

const holtResult = ref<any>(null);

const isDrawerOpen = ref(false);

const make = ref("");
const state = ref("");
const seller = ref("");
const yORm = ref(true);
const season = ref(false);
const seasonPeriod = ref(0);

const fakeHistory = {
  "2010-01-01": 10000,
  "2011-01-01": 14000,
  "2012-01-01": 18000,
  "2013-01-01": 22000,
  "2014-01-01": 27000,
};

const fakeForecast = {
  "2015-01-01": 29000,
  "2016-01-01": 31000,
  "2017-01-01": 33500,
  "2018-01-01": 36000,
  "2019-01-01": 39000,
};

// Draw ECharts
function drawChart(data: {
  history: Record<string, number>;
  forecast: Record<string, number>;
}) {
  const history = Object.entries(data.history).map(([date, val]) => ({
    date,
    value: val,
  }));
  const forecast = Object.entries(data.forecast).map(([date, val]) => ({
    date,
    value: val,
  }));

  const xLabels = [...history, ...forecast].map((d) => d.date);
  const historyData = history.map((d) => d.value);
  const forecastData = new Array(history.length)
    .fill(null)
    .concat(forecast.map((d) => d.value));

  const option: echarts.EChartsOption = {
    title: {
      text: "Holt-Winters Forecast",
      left: "center",
      textStyle: { color: "#fff" },
    },
    tooltip: { trigger: "axis" },
    xAxis: { type: "category", data: xLabels, axisLabel: { color: "#fff" } },
    yAxis: { type: "value", axisLabel: { color: "#fff" } },
    series: [
      { name: "History", type: "line", data: historyData, color: "#888" },
      { name: "Forecast", type: "line", data: forecastData, color: "#00fdfa" },
    ],
  };

  myChart.setOption(option);
}

const submitHoltWinter = async () => {
  try {
    const res = await fetch("http://127.0.0.1:8000/holtwinter", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        make: make.value || null,
        state: state.value || null,
        seller: seller.value || null,
        yORm: yORm.value,
        season: season.value,
        season_period: seasonPeriod.value,
      }),
    });
    const json = await res.json();
    if (
      typeof json.error === "string" &&
      json.error.includes("No enough records")
    ) {
      alert("Not enough records to perform Holt-Winters forecasting.");
      holtResult.value = null;
      return;
    }
    holtResult.value = json;
    drawChart(json);
    isDrawerOpen.value = false;
  } catch (err) {
    console.error("Prediction error:", err);
    alert("Something went wrong with the forecast.");
  }
};

onMounted(() => {
  myChart = echarts.init(chartRef.value);
  drawChart({ history: fakeHistory, forecast: fakeForecast });
});

// function drawChart() {
//   myChart.showLoading();
//   myChart.hideLoading();

//   const base = -Math.floor(
//     data.reduce((min, val) => Math.min(min, val.l), Infinity)
//   );

//   const option: echarts.EChartsOption = {
//     title: {
//       text: "Sales Forecasting",
//       // subtext: "Trend, Seasonality, and Confidence Bands",
//       left: "center",
//       textStyle: { color: "#fff" },
//       subtextStyle: { color: "#ccc" },
//     },
//     tooltip: {
//       trigger: "axis",
//       axisPointer: {
//         type: "cross",
//         animation: false,
//         label: {
//           backgroundColor: "#ccc",
//           borderColor: "#aaa",
//           borderWidth: 1,
//           color: "#222",
//         },
//       },
//       formatter(params: any) {
//         return (
//           `<strong>${params[2].name}</strong><br/>` +
//           `Forecasted Sales Change: ` +
//           ((params[2].value - base) * 100).toFixed(1) +
//           "%"
//         );
//       },
//     },
//     grid: {
//       left: "3%",
//       right: "4%",
//       bottom: "3%",
//       containLabel: true,
//     },
//     xAxis: {
//       type: "category",
//       data: data.map((item) => item.date),
//       axisLabel: {
//         color: "#fff",
//         formatter(value: string, idx: number) {
//           const date = new Date(value);
//           return idx === 0
//             ? value
//             : [date.getMonth() + 1, date.getDate()].join("-");
//         },
//       },
//       boundaryGap: false,
//     },
//     yAxis: {
//       axisLabel: {
//         color: "#fff",
//         formatter(val: number) {
//           return (val - base) * 100 + "%";
//         },
//       },
//       axisPointer: {
//         label: {
//           formatter(params: any) {
//             return ((params.value - base) * 100).toFixed(1) + "%";
//           },
//         },
//       },
//       splitLine: {
//         lineStyle: { color: "#666" },
//       },
//     },
//     series: [
//       {
//         name: "Lower Bound",
//         type: "line",
//         data: data.map((item) => item.l + base),
//         lineStyle: { opacity: 0 },
//         stack: "confidence-band",
//         symbol: "none",
//       },
//       {
//         name: "Confidence Interval",
//         type: "line",
//         data: data.map((item) => item.u - item.l),
//         lineStyle: { opacity: 0 },
//         areaStyle: { color: "rgba(200, 200, 200, 0.3)" },
//         stack: "confidence-band",
//         symbol: "none",
//       },
//       {
//         name: "Forecasted Sales",
//         type: "line",
//         data: data.map((item) => item.value + base),
//         itemStyle: { color: "#00fdfa" },
//         showSymbol: false,
//       },
//     ],
//   };

//   myChart.setOption(option);
// }

// onMounted(() => {
//   myChart = echarts.init(chartRef.value);
//   drawChart();
// });
</script>

<template>
  <div style="padding: 20px; color: white">
    <!-- 图表容器 -->
    <div ref="chartRef" style="width: 100%; height: 350px" />

    <!-- Trigger button -->
    <div class="flex justify-center mt-2">
      <button
        @click="isDrawerOpen = true"
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
      >
        Holt-Winters Forecast
      </button>
    </div>

    <!-- Drawer -->
    <div
      v-if="isDrawerOpen"
      class="fixed inset-0 z-50 bg-black bg-opacity-50"
      @click.self="isDrawerOpen = false"
    >
      <div
        class="fixed right-0 top-0 w-96 h-full bg-gray-900 text-white p-6 shadow-lg z-50"
      >
        <h2 class="text-lg font-semibold mb-4">Holt-Winters Settings</h2>

        <div class="space-y-4">
          <div>
            <label class="block text-sm mb-1">Make:</label>
            <input
              v-model="make"
              class="w-full p-2 bg-gray-800 border border-gray-600 rounded"
              placeholder="e.g. Kia"
            />
          </div>

          <div>
            <label class="block text-sm mb-1">State:</label>
            <input
              v-model="state"
              class="w-full p-2 bg-gray-800 border border-gray-600 rounded"
              placeholder="e.g. ca"
            />
          </div>

          <div>
            <label class="block text-sm mb-1">Seller:</label>
            <input
              v-model="seller"
              class="w-full p-2 bg-gray-800 border border-gray-600 rounded"
              placeholder="e.g. avis"
            />
          </div>

          <div class="flex items-center space-x-2">
            <input type="checkbox" v-model="yORm" />
            <label>Enable yORm</label>
          </div>

          <div class="flex items-center space-x-2">
            <input type="checkbox" v-model="season" />
            <label>Enable seasonality</label>
          </div>

          <div>
            <label class="block text-sm mb-1">Season Period:</label>
            <input
              type="number"
              v-model="seasonPeriod"
              class="w-full p-2 bg-gray-800 border border-gray-600 rounded"
            />
          </div>

          <button
            @click="submitHoltWinter"
            class="w-full bg-blue-600 hover:bg-blue-700 py-2 rounded text-white font-semibold"
          >
            Submit
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
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
  border-radius: 4px;
  cursor: pointer;
}
</style>
