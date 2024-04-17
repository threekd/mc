<script setup lang="ts">
import MoleculeStructure from "./MoleculeStructure.vue";
const props = defineProps({
    molecules: {
      type: Text,
      default: ""
    }
});

</script>



<template>
  <div class="columns is-desktop">
    <div class="column">
      <MoleculeStructure
        :structure= props.molecules
        :width="350"
        :height="300"
        svg-mode
      ></MoleculeStructure>
    </div>
  </div>
</template>
