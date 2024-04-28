<template>
  <p v-if="rdkitError">Error loading renderer</p>

  <p v-if="!rdkitLoaded">Loading renderer</p>

  <span
    v-else-if="!isValidMolString(structure)"
    :title="`Cannot render structure: ${structure}`"
  ></span>

  <div
    v-else-if="svgMode"
    :class="`molecule-structure-svg ${className}`"
    :style="{ width: props.width, height: props.height }"
    v-html="svg"
  ></div>

  <div v-else :class="`molecule-canvas-container ${className}`">
    <canvas
      :title="structure"
      :id="id"
      :width="width"
      :height="height"
    ></canvas>
  </div>
</template>

<script setup lang="ts">
import { nextTick, onMounted, onUnmounted, onUpdated, reactive, ref, watch } from "vue";

import { JSMol } from "../../../../typescript";
import initRDKit from "../utils/initRDKit";

const props = defineProps({
  /**
   * Generic props
   */
  id: {
    type: String,
    required: true
  },
  className: {
    type: String,
    default: ""
  },
  svgMode: {
    type: Boolean,
    default: false
  },
  width: {
    type: Number,
    default: 250
  },
  height: {
    type: Number,
    default: 200
  },
  /**
   * RDKit-specific props
   */
  structure: {
    type: String,
    required: true
  },
  subStructure: {
    type: String,
    default: ""
  },
  extraDetails: {
    type: Object,
    default: {}
  },
  drawingDelay: {
    type: Number,
    default: undefined
  }
});

// Refs for SVG and Canvas containers
const svgContainer = ref(null);
const canvasContainer = ref(null);

/**
 * Automatically adjust width and height based on parent container size
 */
function autoAdjustSize() {
  if (props.svgMode && svgContainer.value) {
    molDetails.width = svgContainer.value.clientWidth;
    molDetails.height = svgContainer.value.clientHeight;
  } else if (!props.svgMode && canvasContainer.value) {
    molDetails.width = canvasContainer.value.clientWidth;
    molDetails.height = canvasContainer.value.clientHeight;
  }
}

/**
 * Redraw molecule with adjusted sizes
 */
function redrawMolecule() {
  autoAdjustSize();
  drawSVGorCanvas();
}

// Load molecule on component mount
onMounted(() => {
  initRDKit()
    .then(() => {
      rdkitLoaded.value = true;
      autoAdjustSize();
      draw();
    })
    .catch((err) => {
      console.error(err);
      rdkitError.value = true;
    });
});

// Watch for prop changes and redraw molecule
watch(props, redrawMolecule);

// Watch for window resize events and redraw molecule
window.addEventListener('resize', redrawMolecule);

// Cleanup resize event listener
onUnmounted(() => {
  window.removeEventListener('resize', redrawMolecule);
});

// RDKit state reporting values
let rdkitLoaded = ref(false);
let rdkitError = ref(false);

// Molecule state values
let wasCalled = ref(false);
let molDetails = reactive({
  width: props.width,
  height: props.height,
  bondLineWidth: 1,
  addStereoAnnotation: true,
  ...props.extraDetails
});
let svg = ref("");

/**
 * Validate the molecule
 */
function isValid(m: JSMol | null) {
  return !!m;
}

/**
 * Validate the string representation of the molecule
 */
function isValidMolString(s: string) {
  const mol = window.RDKit.get_mol(s || "invalid");
  const isValidMol = isValid(mol);
  mol?.delete();

  return isValidMol;
}

/**
 * Get highlight details for molecule
 */
function getMolDetails(mol: JSMol | null, qmol: JSMol | null) {
  if (isValid(mol) && isValid(qmol)) {
    // get substructure highlight details
    const details = JSON.parse(mol?.get_substruct_matches(qmol as JSMol) || "");
    // reduce the list of objects to a single list object with all atoms and bonds
    const detailsMerged: { atoms: number[]; bonds: number[] } = details
      ? details.reduce(
          (
            acc: { atoms: number[]; bonds: number[] },
            { atoms, bonds }: { atoms: number[]; bonds: number[] }
          ) => ({
            atoms: [...acc.atoms, ...atoms],
            bonds: [...acc.bonds, ...bonds]
          }),
          { atoms: [], bonds: [] }
        )
      : details;

    return JSON.stringify({
      ...molDetails,
      ...(props.extraDetails || {}),
      ...detailsMerged
    });
  } else {
    // if one of the molecules are not valid, return no highlight details
    return JSON.stringify({
      ...molDetails,
      ...(props.extraDetails || {})
    });
  }
}

/**
 * Draw the molecule to the canvas, or return set the SVG variable
 */
async function drawSVGorCanvas() {
  const mol = window.RDKit.get_mol(props.structure || "invalid");
  const qmol = window.RDKit.get_qmol(props.subStructure || "invalid");
  const isValidMol = isValid(mol);

  if (props.svgMode && isValidMol) {
    const svgGenerated = (mol as JSMol).get_svg_with_highlights(getMolDetails(mol, qmol));
    svg.value = svgGenerated;
  } else if (isValidMol) {
    await nextTick(); // function needs to wait until canvas is rendered
    const canvas = document.getElementById(props.id) as HTMLCanvasElement;
    (mol as JSMol).draw_to_canvas_with_highlights(canvas, getMolDetails(mol, qmol));
  }

  /**
   * Delete C++ mol objects manually
   * https://emscripten.org/docs/porting/connecting_cpp_and_javascript/embind.html#memory-management
   */
  mol?.delete();
  qmol?.delete();
}

/**
 * Calls the main drawing logic, either with a delay or without
 */
function draw() {
  if (props.drawingDelay) {
    setTimeout(() => drawSVGorCanvas(), props.drawingDelay);
  } else {
    drawSVGorCanvas();
  }
}

/**
 * Ensures draw() is only called once
 */
function drawOnce() {
  return () => {
    if (wasCalled.value === false) {
      wasCalled.value = true;
      draw();
    }
  };
}

/**
 * Load molecule on component mount
 */
onMounted(() => {
  initRDKit()
    .then(() => {
      rdkitLoaded.value = true;
      try {
        draw();
      } catch (err) {
        console.error(err);
      }
    })
    .catch((err) => {
      console.error(err);
      rdkitError.value = true;
    });
});

/**
 * Redraw molecule on component update, or props changes
 */

onUpdated(() => {
  if (!rdkitError && rdkitLoaded && !props.svgMode) {
    drawOnce();
  }
});

watch(props, () => draw());
</script>

<style>
.molecule-structure-svg svg rect:first-of-type {
  fill: transparent !important;
}
.molecule-structure-svg svg {
  width: 100%;
  height: 100%;
}
</style>
