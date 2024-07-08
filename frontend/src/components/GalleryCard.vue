<script setup lang="ts">
import Image from "../Image.ts";
import config from "../config.ts";

defineProps<{ image: Image }>()
defineEmits<{
  (e: 'img-click'): void
}>()

</script>

<template>
  <img :src="`${config.apiEndpoint}/static/${image.filename}`" v-on:click="$emit('img-click')">
</template>

<style scoped>
</style>