<script setup>
import Bar from './SFC-mc/Bar.vue'
import Form from './SFC-mc/Form.vue'
import ProgressBar from './SFC-mc/ProgressBar.vue'
import List_results from './SFC-mc/List.vue'
import Energy_data from './data/energy_data.json'
import axios from 'axios'
import { ref } from 'vue'

//childs
const smiles_or_inchi_or_file = ref('')
const AdductType_dropdownItem = ref({ name: '[M+H]+', code: '[M+H]+' })
const isSubmit = ref(false)
const msg = ref(null)

import { watch } from 'vue'

watch(isSubmit, (newValue) => {
  if (newValue) {
    sendMessage();
  }
});

const sendMessage = () => {
  axios.post("/predict", {
    smiles_or_inchi_or_file: smiles_or_inchi_or_file.value,
    AdductType: AdductType_dropdownItem.value.code
  })
    .then((res) => {
      msg.value = res.data.result
      console.log(res.data);
    })
    .catch((error) => {
      console.error(error.response.data);
    });
};

</script>

<template>

  <h1>CFM-ID</h1>
  <Form v-model:smiles_or_inchi_or_file="smiles_or_inchi_or_file" v-model:isSubmit="isSubmit" v-model:AdductType_dropdownItem="AdductType_dropdownItem" />
  <ProgressBar v-if="isSubmit" />
  <Bar v-if="isSubmit && msg && msg.energy0" :energyData="msg.energy0" :Energy_level="'Low Energy'" />
  <Bar v-if="isSubmit && msg && msg.energy1" :energyData="msg.energy1" :Energy_level="'Middle Energy'" />
  <Bar v-if="isSubmit && msg && msg.energy2" :energyData="msg.energy2" :Energy_level="'High Energy'" />
  <List_results v-if="isSubmit && msg && msg.structure" :energyData="msg.structure" />

<!-- 
  <h1>Here is CFM-ID</h1>

  <Form v-model:smiles_or_inchi_or_file="smiles_or_inchi_or_file" v-model:isSubmit="isSubmit"/>
  <ProgressBar v-if="isSubmit" />
  <Bar v-if="isSubmit" :energyData="Energy_data.energy0" :Energy_level="'Low Energy'" />
  <Bar v-if="isSubmit" :energyData="Energy_data.energy1" :Energy_level="'Middle Energy'" />
  <Bar v-if="isSubmit" :energyData="Energy_data.energy2" :Energy_level="'High Energy'" />
  <List_results v-if="isSubmit" :energyData="Energy_data.structure" />
-->
</template>
