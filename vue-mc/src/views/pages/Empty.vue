<script setup>
import Bar from './SFC-mc/Bar.vue'
import Form from './SFC-mc/Form.vue'
import ProgressBar from './SFC-mc/ProgressBar.vue'
import List_results from './SFC-mc/List.vue'
import Energy_data from './data/energy_data.json'
import axios from 'axios'
import { ref } from 'vue'

//childs
const Compound_string = ref('')
const msg = ref(null)
const isSubmit = ref(false)

/*
import { watch } from 'vue'

watch(isSubmit, (newValue) => {
  if (newValue) {
    sendMessage();
  }
});

const sendMessage = () => {
  axios.post("/update", {
    smiles: Compound_string.value
  })
    .then((res) => {
      msg.value = res.data.result
      console.log(res.data);
    })
    .catch((error) => {
      console.error(error.response.data);
    });
};
/*
const getMessage = () => {
  axios.get("/")
    .then((res) => {
      msg.value = res.data; 
    });
};
*/
</script>

<template>
<!-- for docker version
  <h1>Here is MC</h1>
  <Form v-model:Compound_string="Compound_string" v-model:isSubmit="isSubmit"/>
  <ProgressBar v-if="isSubmit" />
  <Bar v-if="isSubmit && msg && msg.energy0" :energyData="msg.energy0" :Energy_level="'Low Energy'" />
  <Bar v-if="isSubmit && msg && msg.energy1" :energyData="msg.energy1" :Energy_level="'Middle Energy'" />
  <Bar v-if="isSubmit && msg && msg.energy2" :energyData="msg.energy2" :Energy_level="'High Energy'" />
  <List_results v-if="isSubmit && msg && msg.structure" :energyData="msg.structure" />
-->
  <h1>Here is CFM-ID</h1>

  <Form v-model:Compound_string="Compound_string" v-model:isSubmit="isSubmit"/>
  <ProgressBar v-if="isSubmit" />
  <Bar v-if="isSubmit" :energyData="Energy_data.energy0" :Energy_level="'Low Energy'" />
  <Bar v-if="isSubmit" :energyData="Energy_data.energy1" :Energy_level="'Middle Energy'" />
  <Bar v-if="isSubmit" :energyData="Energy_data.energy2" :Energy_level="'High Energy'" />
  <List_results v-if="isSubmit" :energyData="Energy_data.structure" />

</template>
