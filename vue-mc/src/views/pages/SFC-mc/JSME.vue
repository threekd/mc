<template>
  <div ref="jsmeContainer" style="width: 100%; height: 100%;"></div>
  <pre>{{ smiles }}</pre>
</template>

<script setup>
import { onMounted, ref } from 'vue';

const jsmeContainer = ref(null);
const smiles = ref('');
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
  });

  // 监听结构改变事件来更新SMILES
  jsmeApplet.setAfterStructureModifiedCallback(getSmilesFromJSME);
}

function getSmilesFromJSME() {
  // 获取SMILES字符串并更新响应式属性
  smiles.value = jsmeApplet.smiles();
}
</script>