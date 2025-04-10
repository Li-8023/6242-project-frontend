<script setup lang="ts">
import { ref, onMounted } from "vue";
import * as echarts from "echarts/core";
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GeoComponent,
} from "echarts/components";
import { MapChart, PieChart } from "echarts/charts";
import { CanvasRenderer } from "echarts/renderers";
import { use } from "echarts/core";
import VChart from "vue-echarts";

// 地图 JSON
import usaJson from '@/assets/USA.json';

use([
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GeoComponent,
  MapChart,
  PieChart,
  CanvasRenderer,
]);

// 注册地图并微调位置
echarts.registerMap('USA', usaJson as any, {
  Alaska: { left: -131, top: 25, width: 15 },
  Hawaii: { left: -110, top: 28, width: 5 },
  'Puerto Rico': { left: -76, top: 26, width: 2 },
});

const stats: Record<string, any> = {
  "Alabama": {
    center: [-86.9023, 32.3182],
    body_data: [
      { name: "SUV", value: 0, percentage: 0.0 },
      { name: "Sedan", value: 1, percentage: 50.0 },
      { name: "Truck", value: 0, percentage: 0.0 },
      { name: "Other", value: 1, percentage: 50.0 }
    ],
    make_data: [
      { name: "Dodge", value: 1, percentage: 50.0 },
      { name: "Chevrolet", value: 1, percentage: 50.0 }
    ]
  },
  "Arizona": {
    center: [-111.0937, 34.0489],
    body_data: [
      { name: "SUV", value: 343, percentage: 23.24 },
      { name: "Sedan", value: 649, percentage: 43.97 },
      { name: "Truck", value: 0, percentage: 0.0 },
      { name: "Other", value: 484, percentage: 32.79 }
    ],
    make_data: [
      { name: "Chevrolet", value: 236, percentage: 26.94 },
      { name: "Ford", value: 223, percentage: 25.46 },
      { name: "Toyota", value: 220, percentage: 25.11 },
      { name: "Nissan", value: 109, percentage: 12.44 },
      { name: "Dodge", value: 88, percentage: 10.05 }
    ]
  },
  "California": {
    center: [-119.4179, 36.7783],
    body_data: [
      { name: "SUV", value: 2031, percentage: 20.64 },
      { name: "Sedan", value: 4807, percentage: 48.85 },
      { name: "Truck", value: 0, percentage: 0.0 },
      { name: "Other", value: 3002, percentage: 30.51 }
    ],
    make_data: [
      { name: "Ford", value: 1297, percentage: 27.26 },
      { name: "Nissan", value: 1289, percentage: 27.09 },
      { name: "Kia", value: 786, percentage: 16.52 },
      { name: "Hyundai", value: 726, percentage: 15.26 },
      { name: "Chevrolet", value: 660, percentage: 13.87 }
    ]
  },
  "Colorado": {
    center: [-105.7821, 39.5501],
    body_data: [
      { name: "SUV", value: 728, percentage: 33.99 },
      { name: "Sedan", value: 956, percentage: 44.63 },
      { name: "Truck", value: 0, percentage: 0.0 },
      { name: "Other", value: 458, percentage: 21.38 }
    ],
    make_data: [
      { name: "Ford", value: 389, percentage: 24.79 },
      { name: "Chevrolet", value: 388, percentage: 24.73 },
      { name: "Kia", value: 380, percentage: 24.22 },
      { name: "Toyota", value: 296, percentage: 18.87 },
      { name: "Jeep", value: 116, percentage: 7.39 }
    ]
  },
  "Florida": {
    center: [-81.5158, 27.6648],
    body_data: [
      { name: "SUV", value: 3315, percentage: 21.5 },
      { name: "Sedan", value: 7287, percentage: 47.26 },
      { name: "Truck", value: 0, percentage: 0.0 },
      { name: "Other", value: 4818, percentage: 31.25 }
    ],
    make_data: [
      { name: "Ford", value: 3253, percentage: 34.75 },
      { name: "Chevrolet", value: 2327, percentage: 24.86 },
      { name: "Toyota", value: 1428, percentage: 15.25 },
      { name: "Dodge", value: 1231, percentage: 13.15 },
      { name: "Kia", value: 1123, percentage: 12.0 }
    ]
  },
  "Georgia": {
    center: [-82.9001, 32.1656],
    body_data: [
      { name: "SUV", value: 1249, percentage: 21.92 },
      { name: "Sedan", value: 2858, percentage: 50.15 },
      { name: "Truck", value: 0, percentage: 0.0 },
      { name: "Other", value: 1592, percentage: 27.93 }
    ],
    make_data: [
      { name: "Ford", value: 1549, percentage: 40.55 },
      { name: "Kia", value: 960, percentage: 25.13 },
      { name: "Toyota", value: 457, percentage: 11.96 },
      { name: "Chevrolet", value: 429, percentage: 11.23 },
      { name: "Nissan", value: 425, percentage: 11.13 }
    ]
  },
  "Hawaii": {
    center: [-155.5828, 19.8968],
    body_data: [
      { name: "SUV", value: 23, percentage: 24.21 },
      { name: "Sedan", value: 39, percentage: 41.05 },
      { name: "Truck", value: 0, percentage: 0.0 },
      { name: "Other", value: 33, percentage: 34.74 }
    ],
    make_data: [
      { name: "Ford", value: 32, percentage: 49.23 },
      { name: "Chevrolet", value: 13, percentage: 20.0 },
      { name: "GMC", value: 7, percentage: 10.77 },
      { name: "Nissan", value: 7, percentage: 10.77 },
      { name: "Dodge", value: 6, percentage: 9.23 }
    ]
  },
  "Illinois": {
    center: [-89.3985, 40.6331],
    body_data: [
      { name: "SUV", value: 1606, percentage: 26.35 },
      { name: "Sedan", value: 2790, percentage: 45.78 },
      { name: "Truck", value: 0, percentage: 0.0 },
      { name: "Other", value: 1699, percentage: 27.88 }
    ],
    make_data: [
      { name: "Chevrolet", value: 1600, percentage: 35.02 },
      { name: "Ford", value: 1593, percentage: 34.87 },
      { name: "Nissan", value: 480, percentage: 10.51 },
      { name: "Chrysler", value: 466, percentage: 10.2 },
      { name: "Dodge", value: 430, percentage: 9.41 }
    ]
  },
  "Indiana": {
    center: [-86.1349, 40.2672],
    body_data: [
      { name: "SUV", value: 100, percentage: 19.34 },
      { name: "Sedan", value: 270, percentage: 52.22 },
      { name: "Truck", value: 0, percentage: 0.0 },
      { name: "Other", value: 147, percentage: 28.43 }
    ],
    make_data: [
      { name: "Dodge", value: 100, percentage: 28.99 },
      { name: "Ford", value: 94, percentage: 27.25 },
      { name: "Chevrolet", value: 72, percentage: 20.87 },
      { name: "Chrysler", value: 44, percentage: 12.75 },
      { name: "Jeep", value: 35, percentage: 10.14 }
    ]
  },
  "Louisiana": {
    center: [-92.3291, 31.2448],
    body_data: [
      { name: "SUV", value: 33, percentage: 21.85 },
      { name: "Sedan", value: 64, percentage: 42.38 },
      { name: "Truck", value: 0, percentage: 0.0 },
      { name: "Other", value: 54, percentage: 35.76 }
    ],
    make_data: [
      { name: "Ford", value: 33, percentage: 32.35 },
      { name: "Chevrolet", value: 29, percentage: 28.43 },
      { name: "Nissan", value: 22, percentage: 21.57 },
      { name: "Mazda", value: 10, percentage: 9.8 },
      { name: "Toyota", value: 8, percentage: 7.84 }
    ]
  },
  "Maryland": {
    center: [-76.6413, 39.0458],
    body_data: [
      { name: "SUV", value: 176, percentage: 26.99 },
      { name: "Sedan", value: 287, percentage: 44.02 },
      { name: "Truck", value: 0, percentage: 0.0 },
      { name: "Other", value: 189, percentage: 28.99 }
    ],
    make_data: [
      { name: "Ford", value: 211, percentage: 49.3 },
      { name: "Chevrolet", value: 67, percentage: 15.65 },
      { name: "Nissan", value: 56, percentage: 13.08 },
      { name: "Toyota", value: 51, percentage: 11.92 },
      { name: "Dodge", value: 43, percentage: 10.05 }
    ]
  },
  "Massachusetts": {
    center: [-71.3824, 42.4072],
    body_data: [
      { name: "SUV", value: 47, percentage: 34.56 },
      { name: "Sedan", value: 69, percentage: 50.74 },
      { name: "Truck", value: 0, percentage: 0.0 },
      { name: "Other", value: 20, percentage: 14.71 }
    ],
    make_data: [
      { name: "Ford", value: 44, percentage: 46.32 },
      { name: "Chevrolet", value: 14, percentage: 14.74 },
      { name: "Nissan", value: 14, percentage: 14.74 },
      { name: "Dodge", value: 13, percentage: 13.68 },
      { name: "Chrysler", value: 10, percentage: 10.53 }
    ]
  },
  "Michigan": {
    center: [-85.6024, 44.3148],
    body_data: [
      { name: "SUV", value: 551, percentage: 26.88 },
      { name: "Sedan", value: 667, percentage: 32.54 },
      { name: "Truck", value: 0, percentage: 0.0 },
      { name: "Other", value: 832, percentage: 40.59 }
    ],
    make_data: [
      { name: "Ford", value: 679, percentage: 41.78 },
      { name: "Chevrolet", value: 479, percentage: 29.48 },
      { name: "Chrysler", value: 172, percentage: 10.58 },
      { name: "GMC", value: 165, percentage: 10.15 },
      { name: "Dodge", value: 130, percentage: 8.0 }
    ]
  },
  "Minnesota": {
    center: [-94.6859, 46.7296],
    body_data: [
      { name: "SUV", value: 707, percentage: 35.23 },
      { name: "Sedan", value: 566, percentage: 28.2 },
      { name: "Truck", value: 0, percentage: 0.0 },
      { name: "Other", value: 734, percentage: 36.57 }
    ],
    make_data: [
      { name: "Ford", value: 406, percentage: 27.45 },
      { name: "Dodge", value: 378, percentage: 25.56 },
      { name: "Chrysler", value: 333, percentage: 22.52 },
      { name: "Chevrolet", value: 185, percentage: 12.51 },
      { name: "Jeep", value: 177, percentage: 11.97 }
    ]
  },
  "Mississippi": {
    center: [-89.3985, 32.3547],
    body_data: [
      { name: "SUV", value: 64, percentage: 20.0 },
      { name: "Sedan", value: 163, percentage: 50.94 },
      { name: "Truck", value: 0, percentage: 0.0 },
      { name: "Other", value: 93, percentage: 29.06 }
    ],
    make_data: [
      { name: "Ford", value: 67, percentage: 31.6 },
      { name: "Chevrolet", value: 58, percentage: 27.36 },
      { name: "Nissan", value: 33, percentage: 15.57 },
      { name: "Dodge", value: 29, percentage: 13.68 },
      { name: "Toyota", value: 25, percentage: 11.79 }
    ]
  },
  "Missouri": {
    center: [-92.2884, 37.9643],
    body_data: [
      { name: "SUV", value: 1157, percentage: 28.65 },
      { name: "Sedan", value: 1681, percentage: 41.62 },
      { name: "Truck", value: 0, percentage: 0.0 },
      { name: "Other", value: 1201, percentage: 29.74 }
    ],
    make_data: [
      { name: "Ford", value: 2145, percentage: 67.24 },
      { name: "Chevrolet", value: 370, percentage: 11.6 },
      { name: "Kia", value: 245, percentage: 7.68 },
      { name: "Dodge", value: 232, percentage: 7.27 },
      { name: "Toyota", value: 198, percentage: 6.21 }
    ]
  },
  "Nebraska": {
    center: [-99.9018, 41.4925],
    body_data: [
      { name: "SUV", value: 220, percentage: 33.85 },
      { name: "Sedan", value: 246, percentage: 37.85 },
      { name: "Truck", value: 0, percentage: 0.0 },
      { name: "Other", value: 184, percentage: 28.31 }
    ],
    make_data: [
      { name: "Chevrolet", value: 185, percentage: 41.86 },
      { name: "Ford", value: 108, percentage: 24.43 },
      { name: "Dodge", value: 59, percentage: 13.35 },
      { name: "Chrysler", value: 50, percentage: 11.31 },
      { name: "GMC", value: 40, percentage: 9.05 }
    ]
  },
  "Nevada": {
    center: [-116.4194, 38.8026],
    body_data: [
      { name: "SUV", value: 625, percentage: 23.78 },
      { name: "Sedan", value: 1228, percentage: 46.73 },
      { name: "Truck", value: 0, percentage: 0.0 },
      { name: "Other", value: 775, percentage: 29.49 }
    ],
    make_data: [
      { name: "Kia", value: 585, percentage: 34.39 },
      { name: "Ford", value: 371, percentage: 21.81 },
      { name: "Toyota", value: 364, percentage: 21.4 },
      { name: "Chevrolet", value: 201, percentage: 11.82 },
      { name: "Nissan", value: 180, percentage: 10.58 }
    ]
  },
  "New Jersey": {
    center: [-74.4057, 40.0583],
    body_data: [
      { name: "SUV", value: 712, percentage: 21.79 },
      { name: "Sedan", value: 1442, percentage: 44.14 },
      { name: "Truck", value: 0, percentage: 0.0 },
      { name: "Other", value: 1113, percentage: 34.07 }
    ],
    make_data: [
      { name: "BMW", value: 669, percentage: 32.4 },
      { name: "Ford", value: 473, percentage: 22.91 },
      { name: "Subaru", value: 374, percentage: 18.11 },
      { name: "Kia", value: 293, percentage: 14.19 },
      { name: "Nissan", value: 256, percentage: 12.4 }
    ]
  },
  "New Mexico": {
    center: [-106.2485, 34.3071],
    body_data: [
      { name: "SUV", value: 4, percentage: 28.57 },
      { name: "Sedan", value: 8, percentage: 57.14 },
      { name: "Truck", value: 0, percentage: 0.0 },
      { name: "Other", value: 2, percentage: 14.29 }
    ],
    make_data: [
      { name: "Ford", value: 3, percentage: 30.0 },
      { name: "Toyota", value: 2, percentage: 20.0 },
      { name: "Hyundai", value: 2, percentage: 20.0 },
      { name: "Chevrolet", value: 2, percentage: 20.0 },
      { name: "Jeep", value: 1, percentage: 10.0 }
    ]
  },
  "New York": {
    center: [-74.2179, 43.2994],
    body_data: [
      { name: "SUV", value: 138, percentage: 27.38 },
      { name: "Sedan", value: 207, percentage: 41.07 },
      { name: "Truck", value: 0, percentage: 0.0 },
      { name: "Other", value: 159, percentage: 31.55 }
    ],
    make_data: [
      { name: "Ford", value: 352, percentage: 82.63 },
      { name: "Dodge", value: 21, percentage: 4.93 },
      { name: "Nissan", value: 19, percentage: 4.46 },
      { name: "Chevrolet", value: 18, percentage: 4.23 },
      { name: "Jeep", value: 16, percentage: 3.76 }
    ]
  },
  "North Carolina": {
    center: [-79.0193, 35.7596],
    body_data: [
      { name: "SUV", value: 295, percentage: 17.92 },
      { name: "Sedan", value: 999, percentage: 60.69 },
      { name: "Truck", value: 0, percentage: 0.0 },
      { name: "Other", value: 352, percentage: 21.39 }
    ],
    make_data: [
      { name: "Toyota", value: 511, percentage: 42.69 },
      { name: "Chevrolet", value: 231, percentage: 19.3 },
      { name: "Dodge", value: 185, percentage: 15.46 },
      { name: "Ford", value: 182, percentage: 15.2 },
      { name: "Nissan", value: 88, percentage: 7.35 }
    ]
  },
  "Ohio": {
    center: [-82.9071, 40.4173],
    body_data: [
      { name: "SUV", value: 691, percentage: 25.08 },
      { name: "Sedan", value: 1279, percentage: 46.42 },
      { name: "Truck", value: 0, percentage: 0.0 },
      { name: "Other", value: 785, percentage: 28.49 }
    ],
    make_data: [
      { name: "BMW", value: 896, percentage: 43.06 },
      { name: "Kia", value: 509, percentage: 24.46 },
      { name: "Ford", value: 314, percentage: 15.09 },
      { name: "Toyota", value: 221, percentage: 10.62 },
      { name: "Chevrolet", value: 141, percentage: 6.78 }
    ]
  },
  "Oklahoma": {
    center: [-97.0929, 35.0078],
    body_data: [
      { name: "SUV", value: 0, percentage: 0.0 },
      { name: "Sedan", value: 1, percentage: 100.0 },
      { name: "Truck", value: 0, percentage: 0.0 },
      { name: "Other", value: 0, percentage: 0.0 }
    ],
    make_data: [
      { name: "Hyundai", value: 1, percentage: 100.0 }
    ]
  },
  "Oregon": {
    center: [-120.5542, 43.8041],
    body_data: [
      { name: "SUV", value: 47, percentage: 19.34 },
      { name: "Sedan", value: 89, percentage: 36.63 },
      { name: "Truck", value: 0, percentage: 0.0 },
      { name: "Other", value: 107, percentage: 44.03 }
    ],
    make_data: [
      { name: "Ford", value: 51, percentage: 34.93 },
      { name: "Chevrolet", value: 44, percentage: 30.14 },
      { name: "Subaru", value: 19, percentage: 13.01 },
      { name: "Hyundai", value: 16, percentage: 10.96 },
      { name: "Nissan", value: 16, percentage: 10.96 }
    ]
  },
  "Pennsylvania": {
    center: [-77.1945, 41.2033],
    body_data: [
      { name: "SUV", value: 2008, percentage: 27.99 },
      { name: "Sedan", value: 2569, percentage: 35.81 },
      { name: "Truck", value: 0, percentage: 0.0 },
      { name: "Other", value: 2596, percentage: 36.19 }
    ],
    make_data: [
      { name: "Ford", value: 1345, percentage: 30.98 },
      { name: "Chevrolet", value: 951, percentage: 21.9 },
      { name: "Dodge", value: 878, percentage: 20.22 },
      { name: "Chrysler", value: 621, percentage: 14.3 },
      { name: "Jeep", value: 547, percentage: 12.6 }
    ]
  },
  "Puerto Rico": {
    center: [-66.5901, 18.2208],
    body_data: [
      { name: "SUV", value: 35, percentage: 11.95 },
      { name: "Sedan", value: 104, percentage: 35.49 },
      { name: "Truck", value: 0, percentage: 0.0 },
      { name: "Other", value: 154, percentage: 52.56 }
    ],
    make_data: [
      { name: "Toyota", value: 107, percentage: 47.77 },
      { name: "Mitsubishi", value: 46, percentage: 20.54 },
      { name: "Ford", value: 26, percentage: 11.61 },
      { name: "Nissan", value: 24, percentage: 10.71 },
      { name: "Jeep", value: 21, percentage: 9.38 }
    ]
  },
  "South Carolina": {
    center: [-81.1637, 33.8361],
    body_data: [
      { name: "SUV", value: 198, percentage: 27.89 },
      { name: "Sedan", value: 320, percentage: 45.07 },
      { name: "Truck", value: 0, percentage: 0.0 },
      { name: "Other", value: 192, percentage: 27.04 }
    ],
    make_data: [
      { name: "Chevrolet", value: 160, percentage: 34.86 },
      { name: "Ford", value: 119, percentage: 25.93 },
      { name: "Hyundai", value: 64, percentage: 13.94 },
      { name: "Toyota", value: 61, percentage: 13.29 },
      { name: "Dodge", value: 55, percentage: 11.98 }
    ]
  },
  "Tennessee": {
    center: [-86.5804, 35.5175],
    body_data: [
      { name: "SUV", value: 1403, percentage: 27.86 },
      { name: "Sedan", value: 2171, percentage: 43.12 },
      { name: "Truck", value: 0, percentage: 0.0 },
      { name: "Other", value: 1461, percentage: 29.02 }
    ],
    make_data: [
      { name: "Ford", value: 1915, percentage: 53.18 },
      { name: "Nissan", value: 745, percentage: 20.69 },
      { name: "Chevrolet", value: 384, percentage: 10.66 },
      { name: "Lincoln", value: 285, percentage: 7.91 },
      { name: "Infiniti", value: 272, percentage: 7.55 }
    ]
  },
  "Texas": {
    center: [-99.9018, 31.9686],
    body_data: [
      { name: "SUV", value: 1885, percentage: 23.68 },
      { name: "Sedan", value: 3454, percentage: 43.39 },
      { name: "Truck", value: 0, percentage: 0.0 },
      { name: "Other", value: 2622, percentage: 32.94 }
    ],
    make_data: [
      { name: "Ford", value: 2321, percentage: 41.91 },
      { name: "Chevrolet", value: 971, percentage: 17.53 },
      { name: "Kia", value: 900, percentage: 16.25 },
      { name: "Dodge", value: 736, percentage: 13.29 },
      { name: "Nissan", value: 610, percentage: 11.01 }
    ]
  },
  "Utah": {
    center: [-111.0937, 40.1500],
    body_data: [
      { name: "SUV", value: 37, percentage: 22.56 },
      { name: "Sedan", value: 50, percentage: 30.49 },
      { name: "Truck", value: 0, percentage: 0.0 },
      { name: "Other", value: 77, percentage: 46.95 }
    ],
    make_data: [
      { name: "Ford", value: 46, percentage: 39.32 },
      { name: "Chevrolet", value: 37, percentage: 31.62 },
      { name: "GMC", value: 16, percentage: 13.68 },
      { name: "Hyundai", value: 9, percentage: 7.69 },
      { name: "Toyota", value: 9, percentage: 7.69 }
    ]
  },
  "Virginia": {
    center: [-78.6569, 37.4316],
    body_data: [
      { name: "SUV", value: 361, percentage: 22.83 },
      { name: "Sedan", value: 414, percentage: 26.19 },
      { name: "Truck", value: 0, percentage: 0.0 },
      { name: "Other", value: 806, percentage: 50.98 }
    ],
    make_data: [
      { name: "Dodge", value: 465, percentage: 36.07 },
      { name: "Chrysler", value: 411, percentage: 31.89 },
      { name: "Jeep", value: 172, percentage: 13.34 },
      { name: "Chevrolet", value: 125, percentage: 9.7 },
      { name: "Ford", value: 116, percentage: 9.0 }
    ]
  },
  "Washington": {
    center: [-120.7401, 47.7511],
    body_data: [
      { name: "SUV", value: 323, percentage: 22.96 },
      { name: "Sedan", value: 582, percentage: 41.36 },
      { name: "Truck", value: 0, percentage: 0.0 },
      { name: "Other", value: 502, percentage: 35.68 }
    ],
    make_data: [
      { name: "Kia", value: 306, percentage: 31.35 },
      { name: "Ford", value: 266, percentage: 27.25 },
      { name: "Toyota", value: 225, percentage: 23.05 },
      { name: "Subaru", value: 107, percentage: 10.96 },
      { name: "Volvo", value: 72, percentage: 7.38 }
    ]
  },
  "Wisconsin": {
    center: [-88.7879, 43.7844],
    body_data: [
      { name: "SUV", value: 342, percentage: 24.26 },
      { name: "Sedan", value: 800, percentage: 56.74 },
      { name: "Truck", value: 0, percentage: 0.0 },
      { name: "Other", value: 268, percentage: 19.01 }
    ],
    make_data: [
      { name: "Kia", value: 682, percentage: 61.11 },
      { name: "Toyota", value: 130, percentage: 11.65 },
      { name: "Chevrolet", value: 114, percentage: 10.22 },
      { name: "Mercedes‑Benz", value: 96, percentage: 8.6 },
      { name: "Ford", value: 94, percentage: 8.42 }
    ]
  }
};


const option = ref<any>({});

onMounted(() => {
  const mapSeries = {
    type: 'map',
    map: 'USA',
    geoIndex: 0,
    roam: false,
    emphasis: { label: { show: true }, itemStyle: { areaColor: '#cccccc' } },
  };

  // 缩小版的 pieSeries
  const pieSeries = Object.entries(stats).map(([name, s]) => {
    const total = s.body_data.reduce((sum: number, d: any) => sum + d.value, 0);
    // 缩小系数：开方后除以4，最小6px，最大30px
    const raw = Math.sqrt(total) / 4;
    const radius = Math.min(Math.max(6, raw), 30);
    return {
      type: 'pie',
      coordinateSystem: 'geo',
      data: s.body_data,
      center: s.center,
      radius,
      label: { show: false },
      labelLine: { show: false },
      emphasis: { label: { show: true, formatter: '{b}\n{c} ({d}%)' } },
      tooltip: { formatter: '{b}: {c} ({d}%)' },
      animation: false,
    };
  });

  option.value = {
    tooltip: {
      trigger: 'item',
      formatter: (params: any) => {
        if (params.seriesType === 'map') {
          const makes = stats[params.name]?.make_data || [];
          return `${params.name}<br/>` +
            makes.map((m: any) => `${m.name}: ${m.value} (${m.percentage}%)`).join('<br/>');
        }
        return `${params.name}: ${params.value} (${params.percent}%)`;
      },
    },
    legend: {
      data: ['SUV', 'Sedan', 'Truck', 'Other'],
      bottom: 10,
      textStyle: { color: '#ffffff' },
    },
    geo: {
      map: 'USA',
      roam: false,
      zoom: 1.1,
      aspectScale: 0.9,
      itemStyle: { areaColor: '#e7e8ea' },
      emphasis: { itemStyle: { areaColor: '#d1d1d1' } },
    },
    series: [mapSeries, ...pieSeries],
  };
});
</script>

<template>
  <v-chart
    class="chart"
    :option="option"
    style="width: 100%; height: 450px"
  />
</template>

<style>
.chart {
background: transparent !important;
}
</style>