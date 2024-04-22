<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';

const value = ref(0);
let interval = null;

const startProgress = () => {
    interval = setInterval(() => {
        let newValue = value.value + Math.floor(Math.random() * 10) + 1;
        if (newValue >= 90) {
            newValue = 90;
        }
        value.value = newValue;
    }, 2000);
};
const endProgress = () => {
    clearInterval(interval);
    interval = null;
};

onMounted(() => {
    startProgress();
});

onBeforeUnmount(() => {
    endProgress();
});
</script>

<template>
    <div class="grid">
        <div class="col-12">
            <div class="card">
                <h5>Calculating</h5>
                <div class="grid">
                    <div class="col">
                        <ProgressBar :value="value"></ProgressBar>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
