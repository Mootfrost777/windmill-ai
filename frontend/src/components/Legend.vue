<script setup lang="ts">

import Image from "../Image.ts";
import {ref, watch} from "vue";

const props = defineProps<{ image: Image }>()
defineEmits<{
  (e: 'bin-check-image', recheck: boolean): void
}>()

const defects = ref<{}>({})

const defective = {
  true: 'yes',
  false: 'no'
}

watch(() => props.image, async (new_i, old_i) => {
  defects.value = {}
  new_i.defects.forEach(x => defects.value[x.type.name] = (defects.value[x.type.name] || 0) + 1 )
}, {deep: true})

</script>

<template>
  <div class="toolbar-container">
    <label>Legend</label>
    <button @click="$emit('bin-check-image', true)">Scan/Rescan</button>
  </div>
  <div class="data-container" v-if="image">
    <label>Name: {{ image.name }}</label>
    <label v-if="image.defective != null">Defective: {{ defective[image.defective] }}</label>
    <label v-else>Not checked</label>

    <div class="summary-container">
      <label>Defects summary:<br></label>
      <label v-for="(count, defect) in defects" :key="defect">{{ defect }}: {{ count }}<br></label>
    </div>
  </div>
  <div v-else>
    <label>Select image to continue</label>
  </div>
</template>

<style scoped>
.data-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.summary-container {
  margin-top: 10px;
}
</style>