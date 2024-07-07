<script setup lang="ts">

import GalleryCard from "./GalleryCard.vue";
let notes = [1, 2, 3, 4,5, 6, 7, 8, ,8 ,8 , 8,, 8, 8,8,1, 2, 3, 4,5, 6, 7, 8, ,8 ,8 , 8,, 8, 8,8, 1, 2, 3, 4,5, 6, 7, 8, ,8 ,8 , 8,, 8, 8,8]
</script>

<template>
  <div class="toolbar-container">
    <label>Gallery</label>
  </div>
<div class="card-container">
  <GalleryCard v-for="el in notes" class="card"/>
</div>
</template>

<style scoped>

.card-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
  align-content: flex-start;
  flex: 1;
  overflow: auto;
}
.card {
  margin: 1px;
  padding: 0;
  max-width: 100px;
}

.toolbar-container {
  margin-bottom: 3px;
}

</style>