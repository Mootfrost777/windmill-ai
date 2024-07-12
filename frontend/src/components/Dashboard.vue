<script setup lang="ts">
import Viewer from "./Viewer.vue";
import Gallery from "./Gallery.vue";
import Legend from "./Legend.vue";

import axios from 'axios'
import {onMounted, ref, watch} from "vue";
import { useNotification } from "@kyvg/vue3-notification";
const { notify }  = useNotification()
import FormData from 'form-data'


import config from "../config";
import Image from "../Image";
import Toolbar from "./Toolbar.vue";
import ScanResult from "../ScanResult.ts";
import Defect from "../Defect.ts";

const images = ref<Image[]>([])
const viewingImage = ref<Image>({} as Image)
const scanResults = ref<ScanResult[]>([])
const scanResult = ref<ScanResult>()
const defects = ref<Defect[]>([])

const sortBy = ref<String as keyof typeof Image>('defective')

onMounted(async () => {
  const resp = await axios.get<Image[]>(`${config.apiEndpoint}/images`, {
    params: {
      user_id: 1
    }
  })
  images.value = resp.data
  viewingImage.value = images.value[0]
  sortImages()
})

function sortImages(){
  images.value = images.value.sort((n1, n2) => {
    if (n1[sortBy] > n2[sortBy]) {
      return 1;
    }
    if (n1[sortBy]< n2[sortBy]) {
      return -1;
    }
    return 0;
  })
}

async function changeViewingImage(image: Image) {
  viewingImage.value = image
  const resp = await axios.get<ScanResult[]>(`${config.apiEndpoint}/images/scan_results`, {
    params: {
      image_id: image.id
    }
  })
  scanResults.value = resp.data
  scanResult.value = scanResults.value[0]
}

watch(scanResult, async (new_r, old_r) => {
  console.log('bebra')
  const resp = await axios.get<Defect[]>(`${config.apiEndpoint}/images/defects`, {
    params: {
      scan_id: new_r?.id
    }
  })
  viewingImage.value.defects = resp.data
  defects.value = resp.data
}, {deep: true})

async function binProcessImages(imagesToUpdate: Image[]){
  const resp = await axios.post<Image[]>(`${config.apiEndpoint}/ml/check_bin`, { ids: imagesToUpdate.map(x => x.id) })
  return resp.data
}

async function binCheckImages(imagesToUpdate: Image[], recheck: boolean = false) {
  let start = new Date().getTime();
  notify({ title: 'Image scanning', text: 'Scanning started...'})
  if (!recheck){
    imagesToUpdate = imagesToUpdate.filter(x => x.defective == null)
  }
  if (!imagesToUpdate.length){
    return notify({ title: 'Image scanning', text: 'No unprocessed images', type: 'warn'})
  }

  const result = await binProcessImages(imagesToUpdate)
  for (let img of result) {
    const stored = images.value.find(x => x.id == img.id)
    stored.defective = img.defective
  }
  notify({ title: 'Image scanning', text: `Scanning complete in ${(new Date().getTime() - start)/1000}s!`, type: 'success'})

}

async function uploadImage(e) {
  const files =  e.target.files
  console.log(files)
  let data = new FormData();
  for (let f of files) {
    data.append('files', f);
  }
  const response = await axios.post<Image[]>(`${config.apiEndpoint}/images/upload`, data)
  images.value.push(...response.data)
  sortImages()
}
</script>

<template>
  <div class="container">
    <div class="viewer-container">
      <div class="legend-wrapper">
        <Legend class="legend"
                :image="viewingImage"
                @bin-check-image="(recheck) => binCheckImages([viewingImage], recheck)"
        />
      </div>
      <div class="viewer-wrapper">
        <Viewer
            :image="viewingImage"
            :defects="defects"
        />

      </div>
    </div>
    <div class="gallery-wrapper">
      <Toolbar
          @bin-check-images="(recheck) => binCheckImages(images, recheck)"
          @upload-image="uploadImage"
      />
      <Gallery
      :images="images"
      @img-click="changeViewingImage"
      />
    </div>
  </div>
</template>

<style scoped>
Viewer {
  position: relative;
}

.container {
  display: flex;
  flex-direction: column;
  width: 100vw;
  height: 100vh;
}

.viewer-container {
  position: relative;
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