<script setup lang="ts">
import { ref, onMounted, watch, computed } from "vue";

import axios from "axios";

const odometer = ref("");
const condition = ref("");

// Model selection
const allModels = ["Random Forest", "Linear Regression", "XGBoost", "LightGBM"];
const selectedModel = ref("Random Forest");

// Result state
const predictionResult = ref<null | {
  price: number;
  lower: number;
  upper: number;
}>({
  price: 31314,
  lower: 9807.5,
  upper: 82918.75,
});

const isFeatureDrawerOpen = ref(false);
const selectedFeatures = ref<string[]>([]);

const reliabilityMap: Record<string, number> = {
  "Random Forest": 0.7719,
  "LightGBM": 0.6783,
  "XGBoost": 0.5717,
  "Linear Regression": 0.0712,
};

// Computed value for current reliability score
const reliabilityScore = computed(() => {
  return reliabilityMap[selectedModel.value] ?? 0;
});

// Width for the blue progress bar (in %)
const reliabilityPercentWidth = computed(() =>
  (reliabilityScore.value * 100).toFixed(1) + '%'
);

// For display as percentage text
const reliabilityDisplayText = computed(() =>
  (reliabilityScore.value * 100).toFixed(1) + '%'
);


const getLeftPercent = (value: number) => {
  if (!predictionResult.value) return 0;
  const { lower, upper } = predictionResult.value;
  const range = upper - lower;
  if (range <= 0) return 50;

  const offset = 2;
  const percent = ((value - lower) / range) * (100 - offset * 2) + offset;
  return percent;
};

const handlePredict = async () => {
  if (!odometer.value || !condition.value) {
    alert("Please enter both odometer and condition.");
    return;
  }

  const featuresPayload = {
    odometer: parseFloat(odometer.value),
    condition: parseFloat(condition.value),
  };

  try {
    const response = await axios.post("http://127.0.0.1:8000/predict", {
      features: featuresPayload,
    });

    const modelMap: Record<string, string> = {
      "Random Forest": "RF",
      "Linear Regression": "LR",
      XGBoost: "XGB",
      LightGBM: "LGBM",
    };

    const selectedKey = modelMap[selectedModel.value];
    const result = response.data[selectedKey];

    if (result) {
      predictionResult.value = {
        price: result[0],
        lower: result[1][0],
        upper: result[1][1],
      };
    }
  } catch (error) {
    console.error("Prediction error:", error);
    alert("Failed to fetch prediction.");
  }
};
</script>

<template>
  <div
    v-if="predictionResult"
    class="grid grid-cols-1 gap-8 mb-12 mt-10 justify-center"
  >
    <div class="text-white rounded-lg w-[780px] h-[800px] ml-10 px-4">
      <div class="flex justify-between items-start mb-6">
        <div>
          <h2 class="text-lg font-medium">{{ selectedModel }} Model</h2>
          <p class="text-sm text-gray-300 font-geist-mono">Ensemble-based</p>
        </div>
        <div class="model-score">
          <span class="text-sm font-medium">Reliability Score</span>
          <div class="flex items-center mt-1">
    <div class="h-2 w-24 bg-gray-200 rounded-full overflow-hidden">
      <div
        class="h-full bg-blue-500 rounded-full transition-all duration-300"
        :style="{ width: reliabilityPercentWidth }"
      ></div>
    </div>
    <span class="text-sm font-medium ml-2">{{ reliabilityDisplayText }}</span>
  </div>
        </div>
      </div>
      <div class="space-y-4 mt-14">
        <div class="prediction-box animate-in">
          <div class="flex justify-between items-center">
            <span class="text-gray-300">Predicted Price</span>
            <span class="font-semibold text-xl"
              >${{ predictionResult.price.toLocaleString() }}</span
            >
          </div>
          <div class="confidence-interval mt-3">
            <div class="flex justify-between text-xs text-gray-300 mb-1">
              <span>95% Confidence Interval</span>
            </div>
            <div class="relative h-10">
              <div class="absolute inset-0 flex items-center">
                <div class="h-[2px] w-full bg-gray-200"></div>
              </div>
              <div class="absolute inset-0 flex items-center">
                <div class="h-[2px] bg-blue-200"></div>
              </div>
              <div
                class="absolute h-4 w-4 rounded-full bg-blue-500 top-1/2 transform -translate-y-1/2 -translate-x-1/2 flex items-center justify-center"
                :style="{ left: `${getLeftPercent(predictionResult.lower)}%` }"
              >
                <span
                  class="absolute whitespace-nowrap text-xs font-medium -bottom-6"
                >
                  ${{ predictionResult.lower.toLocaleString() }}
                </span>
              </div>
              <div
                class="absolute h-4 w-4 rounded-full bg-blue-500 top-1/2 left-1/2 transform -translate-y-1/2 -translate-x-1/2 flex items-center justify-center"
                :style="{ left: `${getLeftPercent(predictionResult.price)}%` }"
              >
                <span class="font-semibold text-xl">
                  ${{ predictionResult.price.toLocaleString() }}
                </span>
              </div>
              <div
                class="absolute h-4 w-4 rounded-full bg-blue-500 top-1/2 transform -translate-y-1/2 translate-x-1/2 flex items-center justify-center"
                :style="{ left: `${getLeftPercent(predictionResult.upper)}%` }"
              >
                <span
                  class="absolute whitespace-nowrap text-xs font-medium -bottom-6"
                >
                  ${{ predictionResult.upper.toLocaleString() }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- begin model and feature selection -->
      <div class="flex justify-center mt-14">
        <button
          @click="isFeatureDrawerOpen = true"
          class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
        >
          Select Features
        </button>
      </div>
      <!-- end model and feature selection -->

      <!-- Overlay -->
      <div
        v-if="isFeatureDrawerOpen"
        class="fixed inset-0 bg-black bg-opacity-50 z-40"
        @click.self="isFeatureDrawerOpen = false"
      ></div>
      <!-- Drawer Panel -->
      <div
        v-if="isFeatureDrawerOpen"
        class="fixed top-0 right-0 w-80 h-full bg-gray-900 text-white p-6 z-50 shadow-lg transition-transform duration-300"
      >
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-semibold">Choose Features</h3>
          <button
            @click="isFeatureDrawerOpen = false"
            class="text-white text-2xl"
          >
            &times;
          </button>
        </div>

        <div class="flex flex-col gap-2 max-h-[85vh] overflow-y-auto">
          <div class="mb-4">
            <label class="block mb-2 text-sm font-medium text-white"
              >Select Model:</label
            >
            <select
              v-model="selectedModel"
              class="bg-gray-800 border border-gray-600 text-white text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
            >
              <option v-for="model in allModels" :key="model" :value="model">
                {{ model }}
              </option>
            </select>
          </div>

          <div class="space-y-4">
            <div>
              <label for="condition" class="block text-sm mb-1"
                >Condition:</label
              >
              <input
                id="condition"
                v-model="condition"
                type="text"
                class="w-full p-2 rounded bg-gray-800 border border-gray-600 text-white"
                placeholder="e.g. 18"
              />
            </div>

            <div>
              <label for="odometer" class="block text-sm mb-1">Odometer:</label>
              <input
                id="odometer"
                v-model="odometer"
                type="number"
                class="w-full p-2 rounded bg-gray-800 border border-gray-600 text-white"
                placeholder="e.g. 15000"
              />
            </div>
          </div>
        </div>

        <button
          class="mt-6 w-full bg-blue-600 hover:bg-blue-700 transition py-2 rounded text-white font-semibold"
          @click="
            () => {
              handlePredict();
              isFeatureDrawerOpen = false;
            }
          "
        >
          Predict
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.prediction-box,
.feature-importance {
  opacity: 0;
  transform: translateY(10px);
  transition: opacity 0.5s ease, transform 0.5s ease;
}

.animate-in {
  opacity: 1;
  transform: translateY(0);
}

.confidence-interval {
  position: relative;
  margin: 1.5rem 0;
}
.prediction-box {
  background-color: rgba(255, 255, 255, 0.05);
  color: #fff;
  border: 1px solid #2d2d2d;
  border-radius: 0.5rem;
  padding: 1rem;
  max-width: 730px;
  margin-left: 20px;
  
}

.model-score {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.font-geist-mono {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas,
    "Liberation Mono", "Courier New", monospace;
  font-size: 1.3em;
  letter-spacing: -0.02em;
}
</style>
