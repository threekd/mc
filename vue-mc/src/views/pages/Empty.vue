<script setup>
import Bar from './SFC-mc/Bar.vue'
import Form from './SFC-mc/Form.vue'
import Energy_data from './data/energy_data.json'
</script>

<template>
  <h1>Here is MC</h1>
  <Form />
  <Bar :energyData="Energy_data.energy1" :a="0.1"/>
  <Bar :energyData="Energy_data.energy2" :a="1"/>
</template>
