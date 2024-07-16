<script setup lang="ts">
import Image from "../Image.ts";
import {onMounted, ref, watch} from "vue";

const props = defineProps<{ image: Image }>()

const rect_canvas = ref<HTMLCanvasElement>()
const endpoint = import.meta.env.VITE_APP_API_ENDPOINT
onMounted(() => {
  if (rect_canvas.value == undefined) {
    return;
  }

  rect_canvas.value.width = 300;
  rect_canvas.value.height = 300;
})

watch(() => props.image, async (old_i) => {
  if (rect_canvas.value == undefined) {
    return;
  }
  const canvas = rect_canvas.value;
  if (props.image.defects == undefined || props.image.defects == null) {
    return;
  }
  const context  = canvas.getContext("2d");
  if (context == undefined) {
    return;
  }
  context!.clearRect(0, 0, canvas!.width, canvas!.height);
  console.log('viewer detected')
  for (let defect of old_i.defects) {
    let cords = JSON.parse(defect.coordinates)
    context.beginPath();
    context.strokeStyle = defect.type.color;
    context.rect(cords.x, cords.y, cords.w - cords.x, (cords.h  - cords.y));
    context.fillStyle = defect.type.color
    context.font = "10px serif";
    context.fillText(`${defect.type.name}:${(100*defect.confidence).toFixed(2)}%`, cords.x, cords.y - 2);
    context.stroke();
  }
}, { immediate: true, deep: true })



</script>

<template>
  <img v-if="image"
       :src="`${endpoint}/static/${image.filename}`" class="image" >
  <label v-else>{{ $t('select_image_to_continue') }}</label>
  <canvas class="canvas-overlay" ref="rect_canvas" id="canv"></canvas>
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
