<script setup lang="ts">
import Viewer from "./Viewer.vue";
import Gallery from "./Gallery.vue";
import Legend from "./Legend.vue";

import axios from 'axios'
import {onMounted, ref} from "vue";
import config from "../config";
import Image from "../Image";

const images = ref<Image[]>([])
const viewingImage = ref<Image | null>(null)

onMounted(async () => {
  const resp = await axios.get<Image[]>(`${config.apiEndpoint}/images`, {
    params: {
      user_id: 1
    }
  })
  images.value = resp.data
  viewingImage.value = images.value[0]
})

function changeViewingImage(image: Image) {
  viewingImage.value = image
}
</script>

<template>
  <div class="container">
    <div class="viewer-container">
      <div class="legend-wrapper">
        <Legend class="legend"/>
      </div>
      <div class="viewer-wrapper">
        <Viewer
        :image="viewingImage"
        />
      </div>
    </div>
    <div class="gallery-wrapper">
      <Gallery
      :images="images"
      @img-click="changeViewingImage"
      />
    </div>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  width: 100vw;
  height: 100vh;
}

.viewer-container {
  display: flex;
  flex-direction: row;
  flex-grow: 6;
}
.gallery-wrapper{
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  flex-grow: 4;
  max-height: 40vh;
  margin: 7px;
  box-shadow:
      0 1px 1px hsl(0deg 0% 0% / 0.075),
      0 2px 2px hsl(0deg 0% 0% / 0.075),
      0 4px 4px hsl(0deg 0% 0% / 0.075),
      0 8px 8px hsl(0deg 0% 0% / 0.075),
      0 16px 16px hsl(0deg 0% 0% / 0.075)
;
  border-radius: 8px;
}

.legend-wrapper {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  box-shadow:
      0 1px 1px hsl(0deg 0% 0% / 0.075),
      0 2px 2px hsl(0deg 0% 0% / 0.075),
      0 4px 4px hsl(0deg 0% 0% / 0.075),
      0 8px 8px hsl(0deg 0% 0% / 0.075),
      0 16px 16px hsl(0deg 0% 0% / 0.075)
;
  margin: 7px;
  border-radius: 8px;
}
.viewer-wrapper {
  display: flex;
  flex-grow: 1;
  align-items: center;
  justify-content: center;
  box-shadow:
      0 1px 1px hsl(0deg 0% 0% / 0.075),
      0 2px 2px hsl(0deg 0% 0% / 0.075),
      0 4px 4px hsl(0deg 0% 0% / 0.075),
      0 8px 8px hsl(0deg 0% 0% / 0.075),
      0 16px 16px hsl(0deg 0% 0% / 0.075)
;
  border-radius: 8px;
  margin: 7px;
}
</style>