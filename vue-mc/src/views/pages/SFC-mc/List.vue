<script setup>
import { ref, computed, watch } from 'vue'
import RDKit from './RDKit-SVG.vue'
import Energy_data_json from '../data/energy_data.json'
// 引入 lodash 的 orderBy 函数用于排序
import { orderBy } from 'lodash-es'

const props = defineProps({
    energyData: {
        type: Object,
        default: () => ({ /* 默认对象 */ })
    }
});
const rawData = ref(
  Object.entries(props.energyData).map(([key, value]) => ({ fregment_id: key, mass: value[0], SMILES: value[1] }))
);

// 使用计算属性对 rawData 进行排序，依据 sortField 和 sortOrder
const dataviewValue = computed(() => {
  return orderBy(rawData.value, [sortField.value], [sortOrder.value === 1 ? 'asc' : 'desc']);
});

const molecules = ref('')

const layout = ref('grid');
const sortKey = ref(null);
const sortOrder = ref(1);
const sortField = ref('mass');
const sortOptions = ref([
    { label: 'Mass High to Low', value: '!mass' },
    { label: 'Mass Low to High', value: 'mass' }
]);

const onSortChange = (event) => {
    const value = event.value.value;
    const sortValue = event.value;

    if (value.indexOf('!') === 0) {
        sortOrder.value = -1;
        sortField.value = value.substring(1, value.length).toLowerCase();
        sortKey.value = sortValue;
    } else {
        sortOrder.value = 1;
        sortField.value = value.toLowerCase();
        sortKey.value = sortValue;
    }
};

// 监听 sortOrder 和 sortField 的变化，并更新 dataviewValue
watch([sortOrder, sortField], () => {
  dataviewValue.value = orderBy(rawData.value, [sortField.value], [sortOrder.value === 1 ? 'asc' : 'desc']);
});
</script>

<template>
    <div class="grid">
        <div class="col-12">
            <div class="card">
                <h5>DataView</h5>
                <DataView :value="dataviewValue" :layout="layout" :paginator="true" :rows="8" :sortOrder="sortOrder" :sortField="sortField">
                    <template #header>
                        <div class="grid grid-nogutter">
                            <div class="col-6 text-left">
                                <Dropdown v-model="sortKey" :options="sortOptions" optionLabel="label" placeholder="Sort By Mass" @change="onSortChange($event)" />
                            </div>
                        </div>
                    </template>
                    <template #grid="slotProps">
                        <div class="grid grid-nogutter">
                            <div v-for="(item, index) in slotProps.items" :key="index" class="col-12 sm:col-6 md:col-6 p-2">
                                <div class="p-4 border-1 surface-border surface-card border-round flex flex-column">
                                    <div class="surface-50 flex justify-content-center border-round p-3">
                                        <div class="relative mx-auto">
                                            <RDKit :molecules="item.SMILES" />
                                        </div>
                                    </div>
                                    <div class="pt-4">
                                        <div class="flex flex-row justify-content-between align-items-start gap-2">
                                            <div>
                                                <div class="text-lg font-medium text-900 mt-1">{{ item.mass }}</div>
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
