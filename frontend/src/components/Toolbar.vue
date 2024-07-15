<script setup lang="ts">
import Image from "../Image.ts";
import {ref} from "vue";

defineEmits<{
  (e: 'bin-check-images', recheck?: boolean): void
  (e: 'upload-image', event: Event): void,
  (e: 'yolo-check-images'): void
  (e: 'get-report'): void
}>()

const file = ref<HTMLInputElement>()

function uploadClick() {
  if (file.value == undefined) {
    return;
  }
  file.value.click()
}
</script>

<template>
  <div class="toolbar-container">
    <input type="file" ref="file" style="display: none" @change="$emit('upload-image', $event)" accept="image/jpeg" multiple/>

    <label>{{ $t('gallery') }}</label>
    <button @click="$emit('bin-check-images')">{{ $t('toolbar.scan') }}</button>
    <button @click="$emit('bin-check-images', true)">{{ $t('toolbar.scan_all') }}</button>
    <button @click="uploadClick">{{ $t('toolbar.upload') }}</button>
    <button @click="$emit('yolo-check-images')">{{ $t('toolbar.find_defects') }}</button>
    <button @click="$emit('get-report')" class="report-btn">{{ $t('toolbar.generate_report') }}</button>
  </div>
</template>

<style scoped>
.report-btn {
  background: mediumspringgreen;
}
</style>