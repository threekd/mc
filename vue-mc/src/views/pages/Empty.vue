<script setup>
import Bar from './SFC-mc/Bar.vue'
import Form from './SFC-mc/Form.vue'
import Energy_data from './data/energy_data.json'
import axios from 'axios'
import { ref } from 'vue'

const msg = ref(null)
const showBar = ref(false) 

const toggleBarVisibility = () => { 
  showBar.value = true
  sendMessage()
}


const sendMessage = () => {
  axios.post("/update", { 
    smiles: "InChI=1S/C8H10N4O2/c1-10-4-9-6-5(10)7(13)12(3)8(14)11(6)2/h4H,1-3H3"
    // 如果模型需要其他字段，请确保它们在这里发送
  })
  .then((res) => {
    msg.value = res.data.result // Corrected this line
    console.log(res.data);
  })
  .catch((error) => {
    console.error(error.response.data);  // 打印错误信息，它会包括验证错误内容
  });
};

const getMessage = () => {
  axios.get("/")
    .then((res) => {
      msg.value = res.data; // 更新响应式引用的值
    });
};

</script>

<template>
  <h1>Here is MC</h1>
  <div class="field col-12 md:col-3">
      <Button label="Submit" class="mr-2 mb-2" @click="toggleBarVisibility"></Button>
  </div>
  <Form />
  <Bar v-if="showBar" :energyData="msg.energy1" :a="1"/>
  <Bar v-if="showBar && msg" :energyData="msg.energy2" :a="1"/>


</template>