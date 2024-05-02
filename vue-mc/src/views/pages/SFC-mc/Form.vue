<script setup>
import { ref } from 'vue';
import JSME from './JSME.vue'
import { useToast } from 'primevue/usetoast';

const toast = useToast();
const message = ref([]);
const count = ref(0);

const addMessage = (type) => {
    if (type === 'success') {
        message.value = [{ severity: 'success', detail: 'Success Message', content: 'Message sent', id: count.value++ }];
    } else if (type === 'info') {
        message.value = [{ severity: 'info', detail: 'Info Message', content: 'PrimeVue rocks', id: count.value++ }];
    } else if (type === 'warn') {
        message.value = [{ severity: 'warn', detail: 'Warn Message', content: 'There are unsaved changes', id: count.value++ }];
    } else if (type === 'error') {
        message.value = [{ severity: 'error', detail: 'Error Message', content: 'SMILES is invalid', id: count.value++ }];
    }
};

const showSuccess = () => {
    toast.add({ severity: 'success', summary: 'Success Message', detail: 'Message Detail', life: 3000 });
};

const showInfo = () => {
    toast.add({ severity: 'info', summary: 'Info Message', detail: 'Message Detail', life: 3000 });
};

const showWarn = () => {
    toast.add({ severity: 'warn', summary: 'Warn Message', detail: 'Message Detail', life: 3000 });
};

const showError = () => {
    toast.add({ severity: 'error', summary: 'Error Message', detail: 'Message Detail', life: 3000 });
};

const smiles_or_inchi_or_file = defineModel('smiles_or_inchi_or_file',{ type:String, default: '' })
const isSubmit = defineModel('isSubmit',{ default: false })
const AdductType_dropdownItem = defineModel('AdductType_dropdownItem',{ type:Object, default: { name: '[M+H]+', code: '[M+H]+' } })
const SpectraType_dropdownItem = defineModel('SpectraType_dropdownItem',{ type:Object, default: { name: 'ESI', code: 'ESI' } })

const SpectraType_dropdownItems = ref([
    { name: 'ESI', code: 'ESI' },
]);

const AdductType_dropdownItems = ref([
    { name: '[M+H]+', code: '[M+H]+' },
    { name: '[M-H]-', code: '[M-H]-' },
]);

const clearCompoundString = () => {
    smiles_or_inchi_or_file.value = ''; 
}
const drawCompoundString = () => {
//
}
const submitCompoundString = () => {
    if (smiles_or_inchi_or_file.value === '')
    {
        addMessage('error')
    }
    else{
        isSubmit.value = true; 
    }
}
const display = ref(false);
const open = () => {
    display.value = true;
};
const close = () => {
    display.value = false;
};

const moleculeSmiles = ref('');
const handleSmilesChange = (newSmiles) => {
  moleculeSmiles.value = newSmiles;
};
const emit = defineEmits(['update', 'confirm']);
const confirmSmiles = () => {
  emit('confirm', moleculeSmiles.value);
  close(); 
};
</script>

<template>
    <div class="grid">
        <div class="col-12">
            <div class="card">
                <Dialog header="JSME Molecule Editor" v-model:visible="display" :breakpoints="{ '960px': '75vw' }" :modal="true">
                    <div  class="responsive-container">
                        <JSME :width="'100%'" :height="'50vh' ":modelValue="moleculeSmiles" @update:modelValue="handleSmilesChange"/>
                    </div>
                    <template #footer>
                        <div class="flex flex-column gap-2 mt-2">
                            <span class="text-xl font-semibold text-cyan-500">{{ moleculeSmiles }}</span>
                        </div>
                        <Button label="Ok" @click="confirmSmiles" icon="pi pi-check" class="p-button-outlined" />
                    </template>
                </Dialog>
                <h4>Spectra Prediction</h4>
                <div class="p-fluid formgrid grid">
                    <div class="field col-12 md:col-12">
                        <label for="Parent_Compound_Structure">Parent Compound Structure</label>
                        <InputGroup>
                            <InputGroupAddon @click="drawCompoundString">
                                <div @click="open" class="p-link flex align-items-center justify-content-center bg-orange-100 border-round" style="width: 2.0rem; height: 2.0rem">
                                    <i class="pi pi-pencil text-orange-500 text-xl"></i>
                                </div>
                            </InputGroupAddon>
                            <InputText v-model="smiles_or_inchi_or_file" id="Parent_Compound_Structure" type="text"
                                placeholder="Draw or Enter a SMILES string" />
                            <InputGroupAddon @click="clearCompoundString">
                                <button @click="clearCompoundString" class="p-link layout-topbar-button">
                                    <i class="pi pi-eraser"></i>
                                </button>  
                            </InputGroupAddon>                          
                        </InputGroup>
                        <transition-group name="p-message" tag="div">
                            <Message v-for="msg of message" :severity="msg.severity" :key="msg.content">{{ msg.content }}</Message>
                        </transition-group>
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
                    </div>
                </div>
                <div class="card">
                    <div class="p-fluid formgrid grid">
                        <div class="field col-12 md:col-12">
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

<style scoped>
.responsive-container {
    width: 37vw;
    height: 50vh;
}

@media (max-width: 960px) {
    .responsive-container {
        width: 60vw;
    }
}
</style>