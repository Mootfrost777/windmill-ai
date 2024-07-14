<script setup lang="ts">

import Image from "../Image.ts";
import {ref, watch} from "vue";
import {useI18n} from "vue-i18n";
const i18n = useI18n();


const props = defineProps<{ image: Image }>()
defineEmits<{
  (e: 'bin-check-image', recheck: boolean): void,
  (e: 'yolo-check-image'): void
}>()

const defects = ref<{}>({})

const defective = {
  true: { text: i18n.t('yes'), color: 'red' },
  false: { text: i18n.t('no'), color: 'green' },
}

watch(() => props.image, async (new_i, old_i) => {
  defects.value = {}
  if (new_i.defects != undefined){
    new_i.defects.forEach(x => defects.value[x.type.name] = (defects.value[x.type.name] || 0) + 1 )
  }
}, {deep: true})

</script>

<template>
  <div class="toolbar-container">
    <label>{{ $t('gallery') }}</label>
    <button @click="$emit('bin-check-image', true)">{{ $t('legend.scan_rescan') }}</button>
    <button @click="$emit('yolo-check-image')">{{ $t('legend.find_defects') }}</button>
  </div>
  <div class="data-container" v-if="image">
    <label>{{ $t('name') }}: {{ image.name }}</label>
    <label v-if="image.defective != null" :class=" defective[image.defective].color">{{ $t('legend.defective') }}: {{ defective[image.defective].text }}</label>
    <label v-else>{{ $t('legend.not_scanned') }}</label>

    <div class="summary-container">
      <label>{{ $t('legend.defects_summary') }}:<br></label>
      <label v-for="(count, defect) in defects" :key="defect">{{ defect }}: {{ count }}<br></label>
    </div>
  </div>
  <div v-else>
    <label>{{ $t('select_image_to_continue') }}</label>
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