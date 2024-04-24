<script setup>
import { onMounted, ref } from 'vue';

const jsmeContainer = ref(null);
const SMILES = ref('');
let jsmeApplet;

onMounted(() => {
  const jsmeScript = document.createElement('script');
  jsmeScript.type = 'text/javascript';
  jsmeScript.src = '/public/jsme/jsme.nocache.js';
  jsmeScript.onload = initJsme;
  document.head.appendChild(jsmeScript);
});

function initJsme() {

  if (!jsmeContainer.value) {
    return;
  }

  const id = `jsme-container-${Math.random().toString(36).substr(2, 9)}`;
  jsmeContainer.value.id = id;
  jsmeApplet = new JSApplet.JSME(id, "100%", "100%", {
    options: "fullScreenIcon,query,hydrogens",
    "guicolor": "#FFE082",
    "guiAtomColor": "#000000"
  });
  jsmeApplet.setAfterStructureModifiedCallback(getSMILESFromJSME);
}

function getSMILESFromJSME() {
  SMILES.value = jsmeApplet.smiles();
}
</script>

<template>
  <div ref="jsmeContainer" style="width: 100%; height: 100%;"></div>
</template>
