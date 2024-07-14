<script setup lang="ts">

import Image from "../Image.ts";
import {ref, watch} from "vue";

const props = defineProps<{ image: Image }>()
defineEmits<{
  (e: 'bin-check-image', recheck: boolean): void
}>()

const defects = ref<{}>({})

const defective = {
  true: { text: 'да', color: 'red' },
  false: { text: 'нет', color: 'green' },
}

watch(() => props.image, async (new_i, old_i) => {
  defects.value = {}
  new_i.defects.forEach(x => defects.value[x.type.name] = (defects.value[x.type.name] || 0) + 1 )
}, {deep: true})

</script>

<template>
  <div class="toolbar-container">
    <label></label>
    <button @click="$emit('bin-check-image', true)">Scan/Rescan</button>
  </div>
  <div class="data-container" v-if="image">
    <label>Name: {{ image.name }}</label>
    <label v-if="image.defective != null" :class=" defective[image.defective].color">Имеет повреждения: {{ defective[image.defective].text }}</label>
    <label v-else>Not checked</label>

    <div class="summary-container">
      <label>Статистика дефектов:<br></label>
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

.red {
  color: red;
}

.green {
  color: mediumspringgreen;
}

.data-container {
  font-size: 20px;
}
</style>