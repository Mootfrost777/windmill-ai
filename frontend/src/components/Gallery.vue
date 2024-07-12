<script setup lang="ts">

import GalleryCard from "./GalleryCard.vue";
import Image from "../Image.ts";

defineProps<{ images: Image[] }>()
defineEmits<{
  (e: 'img-click', image: Image): void
}>()
</script>

<template>
  <div class="card-container">
    <GalleryCard v-for="el in images"
                 :key="el.id"
                 :image="el"
                 class="card"
                 @img-click="$emit('img-click', el)"
    />
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

</style>