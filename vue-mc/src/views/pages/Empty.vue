<script setup>
import Bar from './SFC-mc/Bar.vue'
import Form from './SFC-mc/Form.vue'
import Energy_data from './data/energy_data.json'
import axios from 'axios'
import { ref } from 'vue'

const msg = ref(null)
const showBar = ref(false) // 新增：控制Bar组件显示的状态

const toggleBarVisibility = () => { // 定义方法切换Bar的可见性
  showBar.value = true
}

axios.get("/")
  .then((res) => {
    msg.value = res.data; 
  })
  .catch((error) => {
    console.error("Error fetching data:", error);
  });

</script>

<template>
  <h1>Here is MC</h1>
  <div class="field col-12 md:col-3">
      <Button label="Submit" class="mr-2 mb-2" @click="toggleBarVisibility"></Button>
  </div>
  <Form />
  <Bar v-if="showBar" :energyData="Energy_data.energy1" :a="1"/>
  <Bar v-if="showBar && msg" :energyData="msg.energy2" :a="1"/>

</template>