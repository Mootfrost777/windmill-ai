<script setup lang="ts">
import Image from "../Image.ts";
import config from "../config.ts";
import {onMounted, reactive, ref, watch} from "vue";
import Defect from "../Defect.ts";

const props = defineProps<{ image: Image, canvas}>()

const rect_canvas = ref(null)

onMounted(() => {
  const canvas = document.getElementById("canv");
  const context = canvas.getContext("2d");
  canvas.width = 300;
  canvas.height = 300;
})

watch(() => props.image, async (old_i, new_i) => {
  console.log('sadsad')
  const canvas = rect_canvas.value;
  if (props.image.defects == undefined || props.image.defects == null) {
    return;
  }
  const context = canvas.getContext("2d");
  context.clearRect(0, 0, canvas.width, canvas.height);
  console.log(old_i)
  for (let defect of old_i.defects) {
    let cords = JSON.parse(defect.coordinates)
    context.beginPath();
    context.strokeStyle = defect.type.color;
    context.rect(cords.x, cords.y, cords.w - cords.x, (cords.h  - cords.y));
    context.fillStyle = defect.type.color
    context.font = "10px serif";
    context.fillText(`${defect.type.name}:${defect.confidence.toFixed(2)*100}%`, cords.x, cords.y - 2);
    context.stroke();
  }
}, { immediate: true, deep: true })



</script>

<template>
  <img v-if="image"
       :src="`${config.apiEndpoint}/static/${image.filename}`" class="image" >
  <canvas class="canvas-overlay" ref="rect_canvas" id="canv"></canvas>
  <label v-if="!image" >{{ $t('select_image_to_continue') }}</label>
</template>

<style scoped lang="scss">
template {
  position: relative;
}
.image {
  position: absolute;
  transform: scale(1.3, 1.3);

}
.canvas-overlay {
  position: absolute;
  height: 300px;
  width: 300px;
  transform: scale(1.3, 1.3);
}
</style>