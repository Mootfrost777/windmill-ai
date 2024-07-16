<script setup lang="ts">
import Viewer from "./Viewer.vue";
import Gallery from "./Gallery.vue";
import Legend from "./Legend.vue";

import axios from 'axios'
import {onMounted, ref, watch} from "vue";
import {useNotification} from "@kyvg/vue3-notification";

const {notify} = useNotification()
import FormData from 'form-data'
import {useI18n} from "vue-i18n";
const i18n = useI18n();



import Toolbar from "./Toolbar.vue";
import ScanResult from "../ScanResult.ts";
import Defect from "../Defect.ts";
import Summary from "./Summary.vue";
import Image from "../Image.ts";

const images = ref<Image[]>([])
const viewingImage = ref<Image>({} as Image)
const scanResults = ref<ScanResult[]>([])
const scanResult = ref<ScanResult>()
const summary = ref<Defect[]>([])


async function getScanResults(image_id: number): Promise<ScanResult[]> {
  const resp = await axios.get<ScanResult[]>('/images/scan_results', {
    params: {
      image_id: image_id
    }
  })
  return resp.data
}

async function getDefects(scanResult: ScanResult): Promise<Defect[]>{
  const resp = await axios.get<Defect[]>('/images/defects', {
    params: {
      scan_id: scanResult?.id
    }
  })
  return resp.data
}

async function getSummary(): Promise<Defect[]> {
  const resp = await axios.get<Defect[]>('/images/summary', {
    params: {
      user_id: 1
    }
  })
  return resp.data
}

onMounted(async () => {
  let resp = await axios.get<Image[]>(`/images`, {
    params: {
      user_id: 1
    }
  })
  images.value = resp.data
  viewingImage.value = images.value[0]
  summary.value = await getSummary()
})


async function changeViewingImage(image: Image) {
  viewingImage.value = image
  scanResults.value = await getScanResults(image.id)
  scanResult.value = scanResults.value[0]
}

async function uploadImage(e: Event) {
  const files = (<HTMLInputElement>e.target).files
  if (files == null) {
    return
  }

  let data = new FormData();
  for (let f of files) {
    data.append('files', f);
  }
  const response = await axios.post<Image[]>('/images/upload', data)
  images.value.push(...response.data)
}

watch(scanResult, async (new_r) => {
  if (new_r == undefined) {
    viewingImage.value.defects = []
    return
  }
  viewingImage.value.defects = await getDefects(new_r)
}, {deep: true})

async function binProcessImages(imagesToUpdate: Image[]) {
  const resp = await axios.post<Image[]>('/ml/check_bin', {ids: imagesToUpdate.map(x => x.id)})
  return resp.data
}

async function binCheckImages(imagesToUpdate: Image[], recheck: boolean = false) {
  let start = new Date().getTime();
  if (!recheck) {
    imagesToUpdate = imagesToUpdate.filter(x => x.defective == null)
  }
  if (!imagesToUpdate.length) {
    return notify({title: i18n.t('alert.image_scanning'), text: i18n.t('alert.no_unscanned_images'), type: 'warn'})
  }
  notify({title: i18n.t('alert.image_scanning'), text: i18n.t('alert.scanning_started')})
  const result = await binProcessImages(imagesToUpdate)
  for (let img of result) {
    const stored = images.value.find(x => x.id == img.id)
    if (stored != undefined) {
      stored.defective = img.defective
    }
  }
  notify({
    title: i18n.t('alert.image_scanning'),
    text: i18n.t('alert.scanning_finished', [(new Date().getTime() - start) / 1000]),
    type: 'success'
  })

}

async function yoloCheckImage(imagesToCheck: Image[]) {
  await axios.post<ScanResult[]>(`/ml/check_yolo`, {ids: imagesToCheck.map(x => x.id)})
  for (let img of imagesToCheck){
    const results = await getScanResults(img.id)
    img.defects = await getDefects(results[0])
  }
  await getSummary()
}

async function getReport() {
  let resp = await axios.get('/stats/report', {
    params: {
      user_id: 1
    },
    responseType: 'arraybuffer'
  })
  let blob = new Blob([resp.data], { type: 'image/png' })
  let link = document.createElement('a')
  link.href = window.URL.createObjectURL(blob)
  link.download = 'Report.png'
  link.click()
}
</script>

<template>
  <div class="container">
    <div class="viewer-container">
      <div class="summary-container">
        <div class="legend-wrapper">
          <Legend class="legend"
                  :image="viewingImage"
                  @bin-check-image="(recheck) => binCheckImages([viewingImage], recheck)"
                  @yolo-check-image="() => yoloCheckImage([viewingImage])"
          />
        </div>
        <div class="legend-wrapper">
          <Summary
              :defects="summary"
          />
        </div>
      </div>
      <div class="viewer-wrapper">
        <Viewer
            :image="viewingImage"
        />

      </div>
    </div>
    <div class="gallery-wrapper">
      <Toolbar
          @bin-check-images="(recheck) => binCheckImages(images, recheck)"
          @upload-image="uploadImage"
          @get-report="getReport"
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

.box {

}

.summary-container {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
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

.gallery-wrapper {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  flex-grow: 4;
  max-height: 40vh;
  margin: 7px;
  box-shadow: 0 1px 1px hsl(0deg 0% 0% / 0.075),
  0 2px 2px hsl(0deg 0% 0% / 0.075),
  0 4px 4px hsl(0deg 0% 0% / 0.075),
  0 8px 8px hsl(0deg 0% 0% / 0.075),
  0 16px 16px hsl(0deg 0% 0% / 0.075);
  border-radius: 8px;

}

.legend-wrapper {
  display: flex;
  flex-direction: column;
  flex-grow: 2;
  box-shadow: 0 1px 1px hsl(0deg 0% 0% / 0.075),
  0 2px 2px hsl(0deg 0% 0% / 0.075),
  0 4px 4px hsl(0deg 0% 0% / 0.075),
  0 8px 8px hsl(0deg 0% 0% / 0.075),
  0 16px 16px hsl(0deg 0% 0% / 0.075);
  margin: 7px;
  border-radius: 8px;
  max-height: 30vh;
}

.viewer-wrapper {
  display: flex;
  flex-grow: 4;
  align-items: center;
  justify-content: center;
  box-shadow: 0 1px 1px hsl(0deg 0% 0% / 0.075),
  0 2px 2px hsl(0deg 0% 0% / 0.075),
  0 4px 4px hsl(0deg 0% 0% / 0.075),
  0 8px 8px hsl(0deg 0% 0% / 0.075),
  0 16px 16px hsl(0deg 0% 0% / 0.075);
  border-radius: 8px;
  margin: 7px;
  flex-flow: column;
  width: 6vw;
}
</style>
