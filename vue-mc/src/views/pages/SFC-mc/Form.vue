<script setup>
import { ref } from 'vue';

const Compound_string = defineModel()

const IonMode_dropdownItems = ref([
    { name: 'Positive', code: 'Positive' },
    { name: 'Nagetive', code: 'Nagetive' },
]);

const AdductType_dropdownItems = ref([
    { name: '[M+H]+', code: '[M+H]+' },
    { name: '[M-H]-', code: '[M-H]-' },
]);

const IonMode_dropdownItem = ref(null);
const AdductType_dropdownItem = ref(null);
</script>

<template>
    <div class="grid">
        <div class="col-12">
            <div class="card">
                <h4>Spectra Prediction</h4>
                <div class="p-fluid formgrid grid">
                    <div class="field col-12 md:col-10">
                        <label for="Parent_Compound_Structure">Parent Compound Structure</label>
                        <InputText v-model="Compound_string" id="Parent_Compound_Structure" type="text" placeholder="Enter an InChI or SMILES string" />
                    </div>
                    <div class="field col-12 md:col-2">
                        <label for="AdductType">Adduct Type</label>
                        <Dropdown id="AdductType" v-model="AdductType_dropdownItem" :options="AdductType_dropdownItems" optionLabel="name" placeholder="Select One"></Dropdown>
                    </div>
                    <div class="field col-12 md:col-2">
                        <Button label="Reset" class="mr-2 mb-2"></Button>
                    </div>
                    <div class="field col-12 md:col-2">
                        <Button label="Submit" class="mr-2 mb-2"></Button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
