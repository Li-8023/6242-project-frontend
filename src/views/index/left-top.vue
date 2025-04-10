<template>
  <v-chart
    class="chart"
    :option="option"
    style="width: 100%; height: 450px;"
  />
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import * as echarts from 'echarts/core';
import { use } from 'echarts/core';
import {
  TooltipComponent,
  GridComponent,
  LegendComponent,
} from 'echarts/components';
import { ScatterChart } from 'echarts/charts';
import { CanvasRenderer } from 'echarts/renderers';
import VChart from 'vue-echarts';

// your raw JSON imports
import clusterData from '@/assets/cluster_data.json';
import clusterPiecesRaw from '@/assets/cluster_pieces.json';

use([
  TooltipComponent,
  GridComponent,
  LegendComponent,
  ScatterChart,
  CanvasRenderer,
]);

// strip any "Cluster X:" prefix from labels
const clusterLabels = (clusterPiecesRaw as any[]).map(p =>
  p.label.replace(/^Cluster\s*\d+:\s*/i, '')
);
const clusterColors = (clusterPiecesRaw as any[]).map(p => p.color);

// flatten raw points [mileage, price, clusterIndex]
const allPoints: [number, number, number][] =
  (clusterData.data as any[][]).map(([x, y, idx]) => [x, y, idx]);

// centroids [mileage, price, clusterIndex]
const centroids: [number, number, number][] =
  (clusterData.centroids as any[]).map((c, i) => [
    c.odometer,
    c.sellingprice,
    i,
  ]);


function sample<T>(arr: T[], max: number): T[] {
  if (arr.length <= max) return arr;
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a.slice(0, max);
}

// pick 10 nearest neighbors for each centroid
const neighborPoints: [number, number, number][] = [];
centroids.forEach(([cx, cy, idx]) => {
  const pts = allPoints.filter(p => p[2] === idx);
  const withDist = pts.map(p => ({
    p,
    dist: Math.hypot(p[0] - cx, p[1] - cy),
  }));
  withDist.sort((a, b) => a.dist - b.dist);
  withDist.slice(0, 10).forEach(w => neighborPoints.push(w.p));
});

const MAX_POINTS_PER_CLUSTER = 200;

const option = ref({});

onMounted(() => {
  option.value = {
    // backgroundColor: '#2c343c',
    legend: {
      top: 10,
      left: 'center',
      orient: 'horizontal',
      data: clusterLabels,
      textStyle: { color: '#fff' },
    },
    tooltip: {
      position: 'top',
      formatter: (params: any) => {
        const d = params.data;
        const series = params.seriesName;
        if (series === 'Neighbors') {
          return `Mileage: ${d[0]}<br/>Price: ${d[1]}<br/>${clusterLabels[d[2]]}`;
        }
        // for clusters and centroids, seriesName is the cluster label
        return `Mileage: ${d[0]}<br/>Price: ${d[1]}<br/>${series}`;
      },
    },
    xAxis: {
      name: 'Mileage',
      axisLine: { lineStyle: { color: '#fff' } },
      splitLine: { lineStyle: { color: 'grey' } },
    },
    yAxis: {
      name: 'Price',
      axisLine: { lineStyle: { color: '#fff' } },
      splitLine: { lineStyle: { color: 'grey' } },
    },
    series: [
      // one sampled scatter series per cluster
      ...clusterLabels.map((label, idx) => {
        const pts = allPoints.filter(p => p[2] === idx);
        const sampled = sample(pts, MAX_POINTS_PER_CLUSTER);
        return {
          name: label,
          type: 'scatter',
          data: sampled.map(p => [p[0], p[1]]),
          symbolSize: 15,
          itemStyle: {
            color: clusterColors[idx],
            borderColor: '#555',
          },
        };
      }),
      // centroids as big white triangles (no label)
      {
        name: 'Centroids',
        type: 'scatter',
        data: centroids.map(c => [c[0], c[1], c[2]]),
        symbol: 'triangle',
        symbolSize: 25,
        label: { show: false },
        itemStyle: {
          color: '#fff',
          borderColor: '#000',
          borderWidth: 2,
        },
        showInLegend: false,
      },
      // 10 nearest neighbors as small diamonds
      {
        name: 'Neighbors',
        type: 'scatter',
        data: neighborPoints.map(p => [p[0], p[1], p[2]]),
        symbol: 'diamond',
        symbolSize: 10,
        itemStyle: {
          color: (p: any) => clusterColors[p.data[2]],
          borderColor: '#000',
          borderWidth: 1,
        },
        showInLegend: false,
      },
    ],
  };
});
</script>

<style scoped>
.chart {
  width: 100%;
  height: 100%;
  background: transparent !important;
}
</style>
