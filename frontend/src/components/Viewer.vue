<script setup lang="ts">
import Image from "../Image.ts";
import config from "../config.ts";
import {onMounted, reactive, ref, watch} from "vue";
import Defect from "../Defect.ts";

const props = defineProps<{ image: Image, canvas}>()



watch(() => props.image, async (old_i, new_i) => {
  console.log('sadsad')
  const canvas = document.getElementById("canv");
  if (props.image.defects == undefined || props.image.defects == null) {
    return;
  }
  const context = canvas.getContext("2d");
  context.clearRect(0, 0, canvas.width, canvas.height);
  console.log(old_i)
  for (let defect of old_i.defects) {
    let cords = JSON.parse(defect.coordinates)
    context.beginPath();
    context.strokeStyle = 'red';
    context.rect(cords.x, cords.y / 2, cords.w - cords.x, (cords.h  - cords.y)/ 2);
    context.stroke();
  }

  const ctx = canvas.getContext("2d");

  ctx.beginPath();
  ctx.stroke();
}, { immediate: true, deep: true })



</script>

<template>
  <img v-if="image"
       :src="`${config.apiEndpoint}/static/${image.filename}`" class="image">
  <canvas class="canvas-overlay" ref="canvas" id="canv"></canvas>

    <label v-if="!image" >Select image to continue</label>
</template>

<style scoped lang="scss">
template {
  position: relative;
}
.image {
  position: absolute;
}
.canvas-overlay {
  position: absolute;
  height: 300px;
  width: 300px;
}
</style>