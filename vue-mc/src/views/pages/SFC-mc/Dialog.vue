<script setup>
import { ref } from 'vue';
import JSME from './JSME.vue'

const display = ref(false);

const open = () => {
    display.value = true;
};
const close = () => {
    display.value = false;
};

</script>

<template>
    <div class="grid">
        <div class="col-12 lg:col-6">
            <div class="card p-fluid">
                <h5>Dialog</h5>
                <Dialog header="Dialog" v-model:visible="display" :breakpoints="{ '960px': '75vw' }" :modal="true">
                    <div  class="responsive-container">
                        <JSME />
                    </div>
                    <template #footer>
                        <Button label="Ok" @click="close" icon="pi pi-check" class="p-button-outlined" />
                    </template>
                </Dialog>
                <Button label="Show" icon="pi pi-external-link" style="width: auto" @click="open" />
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