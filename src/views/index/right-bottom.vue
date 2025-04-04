<script setup lang="ts">
import { ref, onMounted, watch } from "vue";

const allFeatures = [
  "year",
  "make",
  "model",
  "trim",
  "body",
  "transmission",
  "vin",
  "state",
  "condition",
  "odometer",
  "color",
  "interior",
  "seller",
  "mmr",
  "saledate",
];

const selectedFeatures = ref<string[]>([]);
const predictionResult = ref<null | {
  price: number;
  lower: number;
  upper: number;
}>(null);

const isFeatureDrawerOpen = ref(false);

const allModels = ["Random Forest", "Linear Regression", "XGBoost"];
const selectedModel = ref("Random Forest");

// const handlePredict = () => {
//   if (selectedFeatures.value.length === 0) {
//     return alert("Please select at least one feature.");
//   }

//   // Fake realistic prediction output
//   predictionResult.value = {
//     price: 31314,
//     lower: 9807.5,
//     upper: 82918.75,
//   };
// };

onMounted(() => {
  // Preload fake prediction result on component mount
  predictionResult.value = {
    price: 31314,
    lower: 9807.5,
    upper: 82918.75,
  };

  selectedFeatures.value = ["year", "make", "model"];
});

watch(selectedModel, () => {
  if (selectedModel.value === "Random Forest") {
    predictionResult.value = {
      price: 31314,
      lower: 9807.5,
      upper: 82918.75,
    };
  } else if (selectedModel.value === "Linear Regression") {
    predictionResult.value = {
      price: 27800,
      lower: 21500,
      upper: 34500,
    };
  }
});
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
                class="h-full bg-blue-500 rounded-full"
                style="width: 85%"
              ></div>
            </div>
            <span class="text-sm font-medium ml-2">85%</span>
          </div>
        </div>
      </div>
      <div class="space-y-4">
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
                <div
                  class="h-[2px] bg-blue-200"
                  :style="{
                    width: `${
                      ((predictionResult.upper - predictionResult.lower) /
                        predictionResult.upper) *
                      100
                    }%`,
                    marginLeft: `${
                      (predictionResult.lower / predictionResult.upper) * 100
                    }%`,
                  }"
                ></div>
              </div>
              <div
                class="absolute h-4 w-4 rounded-full bg-blue-500 top-1/2 transform -translate-y-1/2 -translate-x-1/2 flex items-center justify-center"
                :style="{
                  left: `${
                    (predictionResult.lower / predictionResult.upper) * 100
                  }%`,
                }"
              >
                <span
                  class="absolute whitespace-nowrap text-xs font-medium -bottom-6"
                >
                  ${{ predictionResult.lower.toLocaleString() }}
                </span>
              </div>
              <div
                class="absolute h-4 w-4 rounded-full bg-blue-500 top-1/2 left-1/2 transform -translate-y-1/2 -translate-x-1/2 flex items-center justify-center"
              >
                <span class="font-semibold text-xl">
                  ${{ predictionResult.price.toLocaleString() }}
                </span>
              </div>
              <div
                class="absolute h-4 w-4 rounded-full bg-blue-500 top-1/2 transform -translate-y-1/2 translate-x-1/2 flex items-center justify-center"
                :style="{
                  right: `${
                    (1 - predictionResult.upper / predictionResult.upper) * 100
                  }%`,
                }"
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

        <div class="feature-importance mt-6 animate-in">
          <h3 class="text-sm font-medium mb-3">Key Factors</h3>
          <div class="space-y-2">
            <div class="flex items-center justify-between">
              <span class="text-xs text-gray-300">Historical Sales</span>
              <div class="w-32 h-2 bg-gray-200 rounded-full overflow-hidden">
                <div
                  class="h-full bg-blue-500 rounded-full"
                  style="width: 92%"
                ></div>
              </div>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-xs text-gray-300">Seasonal Patterns</span>
              <div class="w-32 h-2 bg-gray-200 rounded-full overflow-hidden">
                <div
                  class="h-full bg-blue-500 rounded-full"
                  style="width: 78%"
                ></div>
              </div>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-xs text-gray-300">Customer Demographics</span>
              <div class="w-32 h-2 bg-gray-200 rounded-full overflow-hidden">
                <div
                  class="h-full bg-blue-500 rounded-full"
                  style="width: 65%"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- begin model and feature selection (inline) -->
<div class="flex items-center justify-between gap-4 mt-2">
  <!-- Model Dropdown -->
  <div class="w-1/2">
    <select
      v-model="selectedModel"
      class="bg-gray-800 border border-gray-600 text-white text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
    >
      <option v-for="model in allModels" :key="model" :value="model">
        {{ model }}
      </option>
    </select>
  </div>

  <!-- Feature Selection Button -->
  <div class="w-1/2 flex justify-end items-end">
    <button
      @click="isFeatureDrawerOpen = true"
      class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
    >
      Select Features
    </button>
  </div>
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
          <label
            v-for="feature in allFeatures"
            :key="feature"
            class="flex items-center space-x-2"
          >
            <input
              type="checkbox"
              v-model="selectedFeatures"
              :value="feature"
              class="form-checkbox text-blue-500"
            />
            <span class="text-sm">{{ feature }}</span>
          </label>
        </div>

        <button
          class="mt-6 w-full bg-blue-600 hover:bg-blue-700 transition py-2 rounded text-white font-semibold"
          @click="isFeatureDrawerOpen = false"
        >
          Done
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
  background-color: rgba(
    255,
    255,
    255,
    0.05
  ); // Or rgba(255, 255, 255, 0.05) for translucent
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
  font-size: 0.9em;
  letter-spacing: -0.02em;
}
</style>
