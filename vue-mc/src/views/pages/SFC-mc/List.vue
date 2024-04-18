<script setup>
import { ref } from 'vue'
import RDKit from './RDKit-Vue/ExampleSVG.vue'
import Energy_data_json from '../data/energy_data.json'

const props = defineProps({
    energyData: {
        type: Object,
        default: () => ({ /* 默认对象 */ })
    }
});

const dataviewValue = ref(props.energyData)
const molecules = ref('')

const layout = ref('grid');
const sortKey = ref(null);
const sortOrder = ref(null);
const sortField = ref(null);
const sortOptions = ref([
    { label: 'Price High to Low', value: '!price' },
    { label: 'Price Low to High', value: 'price' }
]);

const onSortChange = (event) => {
    const value = event.value.value;
    const sortValue = event.value;

    if (value.indexOf('!') === 0) {
        sortOrder.value = -1;
        sortField.value = value.substring(1, value.length);
        sortKey.value = sortValue;
    } else {
        sortOrder.value = 1;
        sortField.value = value;
        sortKey.value = sortValue;
    }
};

</script>

<template>
    <div class="grid">
        <div class="col-12">
            <div class="card">
                <h5>DataView</h5>
                <DataView :value="dataviewValue" :layout="layout" :paginator="true" :rows="8" :sortOrder="sortOrder" :sortField="sortField">
                    <template #grid="slotProps">
                        <div class="grid grid-nogutter">
                            <div v-for="(item, index) in slotProps.items" :key="index" class="col-12 sm:col-6 md:col-6 p-2">
                                <div class="p-4 border-1 surface-border surface-card border-round flex flex-column">
                                    <div class="surface-50 flex justify-content-center border-round p-3">
                                        <div class="relative mx-auto">
                                            <RDKit :molecules=item.SMILES />
                                        </div>
                                    </div>
                                    <div class="pt-4">
                                        <div class="flex flex-row justify-content-between align-items-start gap-2">
                                            <div>
                                                <div class="text-lg font-medium text-900 mt-1">{{ item.molecular_weight }}</div>
                                            </div>
                                        </div>
                                        <div class="flex flex-column gap-4 mt-4">
                                            <span class="text-2xl font-semibold text-900">{{ item.SMILES }}</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </template>
                </DataView>
            </div>
        </div>
    </div>
</template>
