<script setup lang="ts">
let notes = ['1', '2', '3']
</script>

<template>
  <div class="toolbar-container">
    <label>Legend</label>
  </div>
  <div class="data-container">
    <label>1</label>
    <label>1</label>
    <label>1</label>
    <label>1</label>
    <label>1</label>
  </div>
</template>

<style scoped>
.data-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
}
</style>