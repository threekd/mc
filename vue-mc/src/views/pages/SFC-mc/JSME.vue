<template>
  <div>
    <div
      :style="{
        width: width,
        height: height,
        outline: jsmeIsLoaded ? '' : '1px solid black',
        outlineOffset: '-.5px',
        textAlign: 'center',
      }"
    >
      <div :id="jsmeId"></div>
    </div>
    <div v-if="jsmeIsLoaded">
      <pre>{{ smiles }}</pre>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const props = defineProps({
  width: { type: String, default: '800px' },
  height: { type: String, default: '500px' },
  options: { type: String, default: 'fullScreenIcon' },
  onChange: { type: Function, required: false },
  src: { type: String, default: '/public/jsme/jsme.nocache.js' },
  modelValue: { type: String, default: '' },
});

const emit = defineEmits(['update:modelValue']);
const jsmeId = 'JME' + Math.random().toString(36).substr(2, 9);
const jsmeIsLoaded = ref(false);
const smiles = ref(props.modelValue);

const loadJsme = () => {
  const newScript = document.createElement('script');
  newScript.type = 'text/javascript';
  newScript.src = props.src;
  newScript.onload = initJsme;
  document.head.appendChild(newScript);
};

const initJsme = () => {
  const jsme = new window.JSApplet.JSME(jsmeId, props.width, props.height, {
    options: props.options,
  });
  jsme.readGenericMolecularInput(props.modelValue);
  jsme.setCallBack('AfterStructureModified', (e) => {
    const newSmiles = e.src.smiles();
    smiles.value = newSmiles;
    emit('update:modelValue', newSmiles);
    props.onChange?.(newSmiles);
  });
  jsmeIsLoaded.value = true;
};

onMounted(() => {
  if (window.JSApplet) {
    initJsme();
  } else {
    loadJsme();
  }
});
</script>