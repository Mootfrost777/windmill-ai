<script setup lang="ts">
import Image from "../Image.ts";
import config from "../config.ts";

defineProps<{ image: Image | null}>()
</script>

<template>
  <img v-if="image"
       :src="`${config.apiEndpoint}/static/${image.filename}`">

  <label v-if="!image" >Select image to continue</label>
</template>

<style scoped lang="scss">
img {
  margin: 0;

}
</style>