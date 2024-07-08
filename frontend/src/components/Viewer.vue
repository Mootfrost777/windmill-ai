<script setup lang="ts">
import Image from "../Image.ts";
import config from "../config.ts";

defineProps<{ image: Image | null}>()
</script>

<template>
  <img v-if="image"
      :src="`${config.apiEndpoint}/static/${image.filename}`">
</template>

<style scoped lang="scss">
img {
  margin: auto;

}

</style>