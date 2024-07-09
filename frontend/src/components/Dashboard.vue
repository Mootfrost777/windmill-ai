<script setup lang="ts">
import Viewer from "./Viewer.vue";
import Gallery from "./Gallery.vue";
import Legend from "./Legend.vue";

import axios from 'axios'
import {onMounted, ref} from "vue";
import { useNotification } from "@kyvg/vue3-notification";
const { notify }  = useNotification()
import config from "../config";
import Image from "../Image";

const images = ref<Image[]>([])
const viewingImage = ref<Image>({} as Image)

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

async function binProcessImages(imagesToUpdate: Image[]){
  const resp = await axios.post<Image[]>(`${config.apiEndpoint}/ml/check_bin`, { ids: images.value.map(x => x.id) })
  return resp.data
}

async function binCheckImages(imagesToUpdate: Image[], recheck: boolean = false) {
  notify({ title: 'Image scanning', text: 'Scanning started...'})
  if (recheck){
    imagesToUpdate = imagesToUpdate.filter(x => x.defective == null)
  }
  const result = await binProcessImages(imagesToUpdate.filter(x => x.defective == null))
  for (let img of result) {
    const stored = images.value.find(x => x.id == img.id)
    stored.defective = img.defective
  }
  notify({ title: 'Image scanning', text: 'Scanning complete!', type: 'success'})

}
</script>

<template>
  <div class="container">
    <div class="viewer-container">
      <div class="legend-wrapper">
        <Legend class="legend"
                :image="viewingImage"
                @bin-check-image="binCheckImages"
        />
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
      @bin-check-images="binCheckImages"
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
  max-height: 60vh;
  height: 50vh;
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
  flex-grow: 2;
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
  flex-grow: 4;
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
  flex-flow: column;
  width: 6vw;
}
</style>