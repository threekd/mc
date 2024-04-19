<script setup>
import { ref } from 'vue';

const Compound_string = defineModel('Compound_string',{ default: '' })
const isSubmit = defineModel('isSubmit',{ default: false })

const SpectraType_dropdownItems = ref([
    { name: 'ESI', code: 'ESI' },
]);

const IonMode_dropdownItems = ref([
    { name: 'Positive', code: 'Positive' },
    { name: 'Nagetive', code: 'Nagetive' },
]);

const AdductType_dropdownItems = ref([
    { name: '[M+H]+', code: '[M+H]+' },
    { name: '[M-H]-', code: '[M-H]-' },
]);

const SpectraType_dropdownItem = ref(null);
const IonMode_dropdownItem = ref(null);
const AdductType_dropdownItem = ref(null);

const clearCompoundString = () => {
    Compound_string.value = ''; // Clear the value
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
                            <InputText v-model="Compound_string" id="Parent_Compound_Structure" type="text"
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
                            <label for="SpectraType">Adduct Type</label>
                            <Dropdown id="SpectraType" v-model="SpectraType_dropdownItem"
                                :options="SpectraType_dropdownItems" optionLabel="name" placeholder="ESI"></Dropdown>
                        </div>
                        <div class="field col-12 md:col-2">
                            <label for="AdductType">Adduct Type</label>
                            <Dropdown id="AdductType" v-model="AdductType_dropdownItem"
                                :options="AdductType_dropdownItems" optionLabel="name" placeholder="[M+H]+"></Dropdown>
                        </div>
                        <div class="field col-12 md:col-2">
                            <label for="IonMode">Ion Mode</label>
                            <Dropdown id="IonMode" v-model="IonMode_dropdownItem" :options="IonMode_dropdownItems"
                                optionLabel="name" placeholder="Positive"></Dropdown>
                        </div>
                    </div>
                </div>
                <div class="card">
                    <div class="p-fluid formgrid grid">
                        <div class="field col-12 md:col-2">
                            <Button @click="submitCompoundString" label="Submit" v-model="isSubmit" class="mr-2 mb-2"></Button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
