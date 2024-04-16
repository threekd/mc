<script setup>
import { ref } from 'vue';

const IonMode_dropdownItems = ref([
    { name: 'Positive', code: 'Positive' },
    { name: 'Nagetive', code: 'Nagetive' },
]);

const AdductType_dropdownItems = ref([
    { name: '[M+H]+', code: '[M+H]+' },
    { name: 'Option 2', code: 'Option 2' },
    { name: 'Option 3', code: 'Option 3' }
]);

const IonMode_dropdownItem = ref(null);
const AdductType_dropdownItem = ref(null);
</script>

<template>
    <div class="grid">
        <div class="col-12">
            <div class="card">
                <h5>Advanced</h5>
                <div class="p-fluid formgrid grid">
                    <div class="field col-12 md:col-12">
                        <label for="Parent Compound Structure">Parent Compound Structure</label>
                        <InputText id="Parent Compound Structure" type="text" />
                    </div>
                    <div class="field col-12 md:col-3">
                        <label for="IonMode">Ion Mode</label>
                        <Dropdown id="IonMode" v-model="IonMode_dropdownItem" :options="IonMode_dropdownItems" optionLabel="name" placeholder="Select One"></Dropdown>
                    </div>
                    <div class="field col-12 md:col-3">
                        <label for="AdductType">Adduct Type</label>
                        <Dropdown id="AdductType" v-model="AdductType_dropdownItem" :options="AdductType_dropdownItems" optionLabel="name" placeholder="Select One"></Dropdown>
                    </div>
                    <div class="field col-12 md:col-3">
                        <label for="Submit">run</label>
                        <Button label="Submit" class="mr-2 mb-2"></Button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
