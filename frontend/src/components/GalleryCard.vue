<script setup lang="ts">
import Image from "../Image.ts";
const endpoint = import.meta.env.VITE_APP_API_ENDPOINT
defineProps<{ image: Image }>()
defineEmits<{
  (e: 'img-click'): void
}>()

</script>

<template>
  <img :src="`${endpoint}/static/${image.filename}`" v-on:click="$emit('img-click')" class="img-card">
</template>

<style scoped lang="scss">
.img-card {
  &:hover {
    filter: brightness(0.7);
  }
  &:active {
    filter: brightness(0.5);
  }
  transition: linear 0.07s;
}

</style>
