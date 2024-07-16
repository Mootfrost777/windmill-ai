<script setup lang="ts">
import Image from "../Image.ts";
import config from "../config.ts";

defineProps<{ image: Image }>()
defineEmits<{
  (e: 'img-click'): void
}>()

</script>

<template>
  <img :src="`${config.apiEndpoint}/api/static/${image.filename}`" v-on:click="$emit('img-click')" class="img-card">
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
