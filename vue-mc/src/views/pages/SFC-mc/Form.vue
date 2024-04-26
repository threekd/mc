<script setup>
import { ref } from 'vue';
import JSME from './JSME.vue'

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
    isSubmit.value = true; 
}
const display = ref(false);
const open = () => {
    display.value = true;
};
const close = () => {
    display.value = false;
};
// 使用ref来创建一个响应式的分子SMILES字符串
const moleculeSmiles = ref('');

// 方法用于处理SMILES字符串的改变
const handleSmilesChange = (newSmiles) => {
  // 更新分子的SMILES字符串
  moleculeSmiles.value = newSmiles;
};
const emit = defineEmits(['update', 'confirm']);
const confirmSmiles = () => {
  // 使用自定义事件 'confirm' 将 SMILES 字符串传递给父组件
  emit('confirm', moleculeSmiles.value);
  close(); // 关闭弹窗
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