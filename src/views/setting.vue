<script setup lang="ts">
import { useSettingStore } from "@/stores/index";
import { ref } from "vue";
import {storeToRefs} from "pinia"
const isScaleRadio = ref(false);
const leftBottomRadio=ref(true)
const rightBottomRadio=ref(true)
const settingStore = useSettingStore();
const {indexConfig}=storeToRefs(settingStore)

const init = () => {
  settingStore.initSetting();
  isScaleRadio.value = settingStore.isScale;

  leftBottomRadio.value=indexConfig.value.leftBottomSwiper
  rightBottomRadio.value=indexConfig.value.rightBottomSwiper

};
init();
const handleClose = () => {};

const cancelClick = () => {
  settingStore.setSettingShow(false);
};

const confirmClick = () => {};
const isScaleChange = (flag: boolean) => {
  settingStore.setIsScale(flag);
};
const radiochange = (blag: boolean) => {
  settingStore.setIsScale(blag);
  // this.$store.commit('setting/updateSwiper', { val, type })
};
const indexRadioChange=(flag: boolean)=>{
  settingStore.setIndexConfig({
    leftBottomSwiper: leftBottomRadio.value,//左轮播
    rightBottomSwiper:rightBottomRadio.value,//右下轮播
  });
}
</script>

<template>
  <el-drawer v-model="settingStore.settingShow" direction="rtl" size="360px">
    <template #header>
      <h2 class="setting-title">setting</h2>
    </template>
    <template #default>
      <div class="left_shu">Global Settings</div>
      <div class="setting_item">
        <span class="setting_label">
          Enable automatic adaptation<span class="setting_label_tip"
            >(default resolution 1920*1080)</span
          >:
        </span>
        <div class="setting_content">
          <el-radio-group v-model="isScaleRadio" @change="(flag)=>isScaleChange(flag as boolean)">
            <el-radio :label="true">Yes</el-radio>
            <el-radio :label="false">No</el-radio>
          </el-radio-group>
        </div>
      </div>
      <div class="left_shu">Real-Time Monitoring</div>
      <div class="setting_item">
        <span class="setting_label">
          Enable device wake-up polling: <span class="setting_label_tip"></span>
        </span>
        <div class="setting_content">
          <el-radio-group
            v-model="leftBottomRadio"
            @change="(flag)=>indexRadioChange(flag as boolean)"
          >
            <el-radio :label="true">Yes</el-radio>
            <el-radio :label="false">No</el-radio>
          </el-radio-group>
        </div>
      </div>
      <div class="setting_item">
        <span class="setting_label"> Enable real-time warning polling: </span>
        <div class="setting_content">
          <el-radio-group
            v-model="rightBottomRadio"
            @change="(flag)=>indexRadioChange(flag as boolean)"
          >
            <el-radio :label="true">Yes</el-radio>
            <el-radio :label="false">No</el-radio>
          </el-radio-group>
        </div>
      </div>
    </template>
    <!-- <template #footer>
      <div style="flex: auto">
        <el-button @click="cancelClick">取消</el-button>
        <el-button type="primary" @click="confirmClick">确定</el-button>
      </div>
    </template> -->
  </el-drawer>
</template>

<style scoped lang="scss">
.setting-title {
  font-size: 20px;
  color: #000;
  font-weight: 900;
  text-align: center;
  line-height: 1;
}
.left_shu {
  color: #000;
  font-weight: 900;
  position: relative;
  text-indent: 10px;
  padding: 16px 0 10px 0;
  line-height: 1;
  &::before {
    display: block;
    content: " ";
    height: 16px;
    width: 4px;
    border-radius: 2px;
    background: #0072ff;
    position: absolute;
    left: 0px;
  }
}
.setting_item {
  font-size: 14px;
  line-height: 1.5;

  // display: flex;
  .setting_label {
    color: #555454;
  }
  .setting_label_tip {
    font-size: 12px;
    color: #838282;
  }
}
</style>
