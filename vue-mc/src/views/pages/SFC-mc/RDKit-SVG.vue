<script setup lang="ts">
import MoleculeStructure from "./rdkit-js/examples/vue/src/components/MoleculeStructure.vue";

const props = defineProps({
    molecules: {
      type: String,
      default: ""
    }
});
const molecules_list = [props.molecules];

</script>


<template>
  <div id="component-example-svg" class="container">
    <section class="hero">
      <div class="hero-body">
      </div>
    </section>
  </div>
  <div class="columns is-desktop">
    <div class="column" v-for="(mol, idx) in molecules_list">
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