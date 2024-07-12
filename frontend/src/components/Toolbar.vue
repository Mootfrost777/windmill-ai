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

    <label>Gallery</label>
    <button @click="$emit('bin-check-images')">Scan all</button>
    <button @click="$emit('bin-check-images', true)">Rescan all</button>
    <button @click="$refs.file.click()">Upload</button>
  </div>
</template>

<style scoped>

</style>