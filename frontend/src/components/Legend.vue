<script setup lang="ts">

import Image from "../Image.ts";

defineProps<{ image: Image }>()
defineEmits<{
  (e: 'bin-check-image', recheck: boolean): void
}>()

const defective = {
  true: 'yes',
  false: 'no'
}
</script>

<template>
  <div class="toolbar-container">
    <label>Legend</label>
    <button @click="$emit('bin-check-image', true)">Scan/Rescan</button>
  </div>
  <div class="data-container" v-if="image">
    <label>Name: {{ image.name }}</label>
    <label v-if="image.defective != null">Defective: {{ defective[image.defective] }}</label>
    <div v-else>
      <label>Not checked</label>
    </div>
  </div>
  <div v-else>
    <label>Select image to continue</label>
  </div>
</template>

<style scoped>
.data-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
}
</style>