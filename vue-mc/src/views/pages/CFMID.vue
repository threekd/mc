<script setup>
import { ref, watch } from 'vue'
import axios from 'axios'
import Bar from './SFC-mc/Bar.vue'
import Form from './SFC-mc/Form.vue'
import ProgressBar from './SFC-mc/ProgressBar.vue'
import List_results from './SFC-mc/List.vue'
import { useToast } from 'primevue/usetoast';

const toast = useToast();
const smiles_or_inchi_or_file = ref('')
const AdductType_dropdownItem = ref({ name: '[M+H]+', code: '[M+H]+' })
const isSubmit = ref(false)
const msg = ref(null)
const confirm = ref('')

const showError = () => {
    toast.add({ severity: 'error', summary: 'Error Message', detail: 'Something wrong', life: 5000 });
};

watch(isSubmit, (newValue) => {
  if (newValue) {
    sendMessage();
  }
});
const res_status = ref(null)
const sendMessage = () => {
  isSubmit.value = true;
  axios.post("/predict", {
    smiles_or_inchi_or_file: smiles_or_inchi_or_file.value,
    AdductType: AdductType_dropdownItem.value.code
  })
    .then((res) => {
      res_status.value = res.status
      if (res.status == 200){
        msg.value = res.data.result;
      }
      else{
        showError();
      }
      isSubmit.value = false;
    })
    .catch((error) => {
      //console.error(error.response.data);
      showError();
      isSubmit.value = false;
    });
};

</script>

<template>
  <h1>IntelliSpectra</h1>

  <Form v-model:smiles_or_inchi_or_file="smiles_or_inchi_or_file" v-model:isSubmit="isSubmit" v-model:AdductType_dropdownItem="AdductType_dropdownItem" @confirm="(msg) => smiles_or_inchi_or_file = msg"/>
  <ProgressBar v-if="isSubmit" />
  <Bar v-if="!isSubmit && msg && msg.energy0" :energyData="msg.energy0" :Energy_level="'Low Energy'" />
  <Bar v-if="!isSubmit && msg && msg.energy1" :energyData="msg.energy1" :Energy_level="'Middle Energy'" />
  <Bar v-if="!isSubmit && msg && msg.energy2" :energyData="msg.energy2" :Energy_level="'High Energy'" />
  <List_results v-if="!isSubmit && msg && msg.fragment" :energyData="msg.fragment" />

</template>
