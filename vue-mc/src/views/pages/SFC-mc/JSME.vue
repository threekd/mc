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

  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';

// 定义组件的props
const props = defineProps({
  width: { type: String, default: '' },
  height: { type: String, default: '"100%"' },
  onChange: { type: Function, default: () => {} },
  src: { type: String, default: '/public/jsme/jsme.nocache.js' },
  modelValue: { type: String, default: '' },
});

// 定义组件会发出的事件
const emit = defineEmits(['update:modelValue']);

// 生成一个随机ID给JSME编辑器的DOM容器
const jsmeId = `JME-${Math.random().toString(36).substr(2, 9)}`;

// 响应式变量表示JSME是否载入完成
const jsmeIsLoaded = ref(false);

// SMILES字符串响应式变量初始化为props.modelValue的值
const smiles = ref(props.modelValue);

let jsmeApplet;

// 函数用于动态加载JSME脚本
const loadJsme = () => {
  const newScript = document.createElement('script');
  newScript.type = 'text/javascript';
  newScript.src = props.src;
  newScript.onload = initJsme; // 当脚本加载完毕，调用initJsme方法
  document.head.appendChild(newScript);
};

// 函数用于初始化JSME编译器
const initJsme = () => {
  jsmeApplet = new window.JSApplet.JSME(jsmeId, props.width, props.height, {
    options: "fullScreenIcon,query,hydrogens",
    "guicolor": "#FFE082",
    "guiAtomColor": "#000000"
  });

  // 如果提供了初始的SMILES字符串，就将其加载进编辑器
  if (props.modelValue) {
    jsmeApplet.readGenericMolecularInput(props.modelValue);
  }

  // 设置结构修改后的回调
  jsmeApplet.setCallBack('AfterStructureModified', (event) => {
    const newSmiles = event.src.smiles(); // 获取新的SMILES字符串
    smiles.value = newSmiles; // 更新响应式变量
    emit('update:modelValue', newSmiles); // 发出事件通知
    props.onChange(newSmiles); // 调用onChange回调
  });

  jsmeIsLoaded.value = true; // 更新状态为已加载完成
};

// 在组件被销毁前的清理工作
const cleanUpJsme = () => {
  if (jsmeApplet && jsmeApplet.destroy) {
    jsmeApplet.destroy(); // 销毁JSME编辑器
  }
};

onMounted(() => {
  if (window.JSApplet?.JSME) {
    initJsme(); // 如果JSME脚本已经可用，直接初始化
  } else {
    loadJsme(); // 否则加载脚本
  }
});

onBeforeUnmount(() => {
  cleanUpJsme(); // 组件被销毁前执行清理
});
</script>