<script setup lang="ts">
import {ref, watch} from "vue";
import Image from "../Image.ts";
import Defect from "../Defect.ts";

const props = defineProps<{ defects: Defect[] }>()

const defects_count = ref<{}>({})

watch(() => props.defects, async (new_i, old_i) => {
  defects_count.value = {}
  new_i.forEach(x => defects_count.value[x.type.name] = (defects_count.value[x.type.name] || 0) + 1 )
})
</script>

<template>
  <div class="toolbar-container">
    <label>{{ $t('summary') }}</label>
  </div>
  <label v-for="(count, defect) in defects_count" :key="defect">{{ defect }}: {{ count }}<br></label>
</template>

<style scoped>

</style>