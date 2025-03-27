<script setup lang="ts">
import { ref } from "vue";

const allFeatures = [
  "year", "make", "model", "trim", "body",
  "transmission", "vin", "state", "condition",
  "odometer", "color", "interior", "seller",
  "mmr", "saledate"
];

const selectedFeatures = ref<string[]>([]);
const predictionResult = ref<null | { price: number; lower: number; upper: number }>(null);

const handlePredict = () => {
  if (selectedFeatures.value.length === 0) {
    return alert("Please select at least one feature.");
  }

  // 模拟返回
  predictionResult.value = {
    price: 23000,
    lower: 21000,
    upper: 25000,
  };
};
</script>

<template>
  <div class="car-price-predict">
    <div class="form-section">
      <el-form @submit.prevent="handlePredict" inline>
        <el-form-item >
          <el-select
            v-model="selectedFeatures"
            multiple
            filterable
            placeholder="Select features"
            style="width: 400px"
          >
            <el-option
              v-for="item in allFeatures"
              :key="item"
              :label="item"
              :value="item"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handlePredict">Predict</el-button>
        </el-form-item>
      </el-form>
    </div>

    <div v-if="predictionResult" class="result-section">
      <p><strong class="price-label">Predicted Price:</strong> <span class="price-value">${{ predictionResult.price }}</span></p>
      <p><strong class="ci-label">Confidence Interval:</strong> <span class="ci-value">${{ predictionResult.lower }} - ${{ predictionResult.upper }}</span></p>
    </div>
  </div>
</template>

<style scoped lang="scss">
.car-price-predict {
  color: #fff;
  padding: 20px;

  .form-section {
    display: flex;
    justify-content: flex-start;
    align-items: center;
    gap: 10px;
  }

  .el-select,
  .el-form-item__label {
    color: #fff !important;
  }

  .result-section {
    background-color: rgba(255, 255, 255, 0.05);
    padding: 16px 24px;
    border-radius: 10px;
    font-size: 30px;
    line-height: 1.8;
    margin-top: 60px; 
    width: fit-content;
    min-width: 300px;
    max-width: 600px;
    
  
    margin-left: auto;
    margin-right: auto;
    text-align: center;
  }

  .price-label {
    color: #00fdfa;
  }

  .ci-label {
    color: #e3b337;
  }

  .price-value {
    font-weight: bold;
    color: #00fdfa;
  }

  .ci-value {
    font-weight: bold;
    color: #e3b337;
  }
}
</style>