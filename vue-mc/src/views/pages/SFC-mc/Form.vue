<script setup>
import { ref } from 'vue';

const smiles_or_inchi_or_file = defineModel('smiles_or_inchi_or_file',{ type:String, default: '' })
const isSubmit = defineModel('isSubmit',{ default: false })
const AdductType_dropdownItem = defineModel('AdductType_dropdownItem',{ type:Object, default: { name: '[M+H]+', code: '[M+H]+' } })
const SpectraType_dropdownItem = defineModel('SpectraType_dropdownItem',{ type:Object, default: { name: 'ESI', code: 'ESI' } })
const Example = defineModel('Example',{ type:String, default: '' })

const SpectraType_dropdownItems = ref([
    { name: 'ESI', code: 'ESI' },
]);

const Examples = ref([
    { name: 'Example1', code: 'InChI=1S/C11H14N2/c1-12-7-6-9-8-13-11-5-3-2-4-10(9)11/h2-5,8,12-13H,6-7H2,1H3' },
    { name: 'Example2', code: 'CNCCC1=CNC2=CC=CC=C21' },
    { name: 'Example3', code: 'CCCCC/C=C\C/C=C\C/C=C\C/C=C\CCCC(=O)N[C@H](C)CO' }
]);

const AdductType_dropdownItems = ref([
    { name: '[M+H]+', code: '[M+H]+' },
    { name: '[M-H]-', code: '[M-H]-' },
]);

const clearCompoundString = () => {
    smiles_or_inchi_or_file.value = ''; // Clear the value
}
const submitCompoundString = () => {
    isSubmit.value = true; // Clear the value
}
</script>

<template>
    <div class="grid">
        <div class="col-12">
            <div class="card">
                <h4>Spectra Prediction</h4>
                <div class="p-fluid formgrid grid">
                    <div class="field col-12 md:col-12">
                        <label for="Parent_Compound_Structure">Parent Compound Structure</label>
                        <InputGroup>
                            <InputText v-model="smiles_or_inchi_or_file" id="Parent_Compound_Structure" type="text"
                                placeholder="Enter an InChI or SMILES string" />
                            <InputGroupAddon @click="clearCompoundString">
                                <button @click="clearCompoundString" class="p-link layout-topbar-button">
                                    <i class="pi pi-eraser"></i>
                                </button>  
                            </InputGroupAddon>                          
                        </InputGroup>
                    </div>
                </div>
                <div class="card p-fluid">
                    <!--    <h5>Vertical Grid</h5>   -->
                    <div class="formgrid grid">
                        <div class="field col-12 md:col-2">
                            <label for="SpectraType">Spectra Type</label>
                            <Dropdown id="SpectraType" v-model="SpectraType_dropdownItem"
                                :options="SpectraType_dropdownItems" optionLabel="name" placeholder="ESI"></Dropdown>
                        </div>
                        <div class="field col-12 md:col-2">
                            <label for="AdductType">Adduct Type</label>
                            <Dropdown id="AdductType" v-model="AdductType_dropdownItem"
                                :options="AdductType_dropdownItems" optionLabel="name" placeholder="[M+H]+"></Dropdown>
                        </div>
                        <!-- to be delete
                        <div class="field col-12 md:col-2">
                            <label for="Example">Examples</label>
                            <Dropdown id="Example" v-model="Example" :options="Examples"
                                optionLabel="name" placeholder="Select one to try"></Dropdown>
                        </div>
                        -->
                    </div>
                </div>
                <div class="card">
                    <div class="p-fluid formgrid grid">
                        <div class="field col-12 md:col-12">
                            <label>InChI=1S/C11H14N2/c1-12-7-6-9-8-13-11-5-3-2-4-10(9)11/h2-5,8,12-13H,6-7H2,1H3</label>
                        </div>
                        <div class="field col-12 md:col-2">
                            <Button @click="submitCompoundString" label="Submit" v-model="isSubmit" class="mr-2 mb-2"></Button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
