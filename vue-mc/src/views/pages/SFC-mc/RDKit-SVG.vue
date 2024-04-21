<script setup lang="ts">
import { ref, watch, defineProps } from 'vue';
import MoleculeStructure from "./MoleculeStructure.vue";

const props = defineProps({
  molecules: {
    type: String,
    default: ""
  }
});

const molecules_list = ref([props.molecules]);

watch(() => props.molecules, (newMolecule) => {
  molecules_list.value = [newMolecule];
}, { immediate: true });

</script>

<template>
  <div id="component-example-svg" class="container">
    <section class="hero">
      <div class="hero-body">
      </div>
    </section>
  </div>
  <div class="columns is-desktop">
    <div class="column" v-for="(mol, idx) in molecules_list" :key="idx">
      <MoleculeStructure
        :id="`structure-example-svg-${idx}`"
        :structure="mol"
        :width="300"
        :height="300"
        svg-mode
      ></MoleculeStructure>
    </div>
  </div>
</template>