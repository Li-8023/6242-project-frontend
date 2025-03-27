<script setup lang="ts">
import { ref, onMounted } from "vue";
import * as echarts from "echarts/core";
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GeoComponent,
} from "echarts/components";
import { PieChart } from "echarts/charts";
import { CanvasRenderer } from "echarts/renderers";
import { use } from "echarts/core";
import { graphic } from "echarts/core";
import VChart from "vue-echarts";
import usaJson from "@/assets/USA.json"; // 确保你放了地图 JSON 文件

use([
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GeoComponent,
  PieChart,
  CanvasRenderer,
]);

const option = ref({});

//注册名为 "USA" 的地图，并对某些偏远州（阿拉斯加、夏威夷、波多黎各）进行位置缩放和偏移，使它们出现在更合适的位置。
echarts.registerMap("USA", usaJson, {
  Alaska: {
    left: -131,
    top: 25,
    width: 15,
  },
  Hawaii: {
    left: -110,
    top: 28,
    width: 5,
  },
  "Puerto Rico": {
    left: -76,
    top: 26,
    width: 2,
  },
});

function randomPieSeries(center: string | number[], radius: number) {
  const data = ["SUV", "Sedan", "Truck", "Other"].map((t) => {
    return {
      value: Math.round(Math.random() * 100),
      name: t,
    };
  });
  return {
    type: "pie",
    coordinateSystem: "geo",
    tooltip: {
      formatter: "{b}: {c} ({d}%)",
    },
    label: {
      show: false,
    },
    labelLine: {
      show: false,
    },
    animationDuration: 0,
    radius,
    center,
    data,
  };
}

onMounted(() => {
  option.value = {
    geo: {
      map: "USA",
      // roam: true, //可以拖拽
      itemStyle: {
        areaColor: "#e7e8ea",
      },
    },
    tooltip: {},
    legend: {
      data: ["SUV", "Sedan", "Truck", "Other"],
      textStyle: {
        color: "#ffffff", 
  
      },
    },
    series: [
      randomPieSeries([-86.753504, 33.01077], 15),
      randomPieSeries([-116.853504, 39.8], 25),
      randomPieSeries([-99, 31.5], 30),
      randomPieSeries([-69, 45.5], 12),
    ],
  };
});
</script>

<template>
  <v-chart class="chart" :option="option" style="width: 100%; height: 450px" />
</template>