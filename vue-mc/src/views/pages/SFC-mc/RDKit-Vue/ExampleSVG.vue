<script setup lang="ts">
import MoleculeStructure from "./MoleculeStructure.vue";

const molecules = ["CCCCC/C=C\C/C=C\C/C=C\C/C=C\CCCC(=O)N[C@H](C)CO"];
</script>



<template>
  <div class="columns is-desktop">
    <div class="column" v-for="(mol, idx) in molecules">
      <MoleculeStructure
        :id="`structure-example-svg-${idx}`"
        :structure="mol"
        :width="350"
        :height="300"
        svg-mode
      ></MoleculeStructure>
    </div>
  </div>
</template>
