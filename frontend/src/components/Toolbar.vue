<script setup lang="ts">
import Image from "../Image.ts";

defineEmits<{
  (e: 'bin-check-images', recheck?: boolean): void
  (e: 'upload-image', event): void
}>()
</script>

<template>
  <div class="toolbar-container">
    <input type="file" ref="file" style="display: none" @change="$emit('upload-image', $event)" accept="image/jpeg" multiple/>

    <label>{{ $t('gallery') }}</label>
    <button @click="$emit('bin-check-images')">{{ $t('toolbar.scan') }}</button>
    <button @click="$emit('bin-check-images', true)">{{ $t('toolbar.scan_all') }}</button>
    <button @click="$refs.file.click()">{{ $t('toolbar.upload') }}</button>
  </div>
</template>

<style scoped>

</style>