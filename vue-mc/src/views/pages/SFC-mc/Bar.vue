<script setup>
import { ref, watch } from 'vue';
import { useLayout } from '@/layout/composables/layout';


const props = defineProps({
    energyData: {
        type: Object,
        default: () => ({ /* 默认对象 */ })
    },
    Bar_percentage: {
        type: Number,
        default: 0.5
    },
    Cateory_percentage: {
        type: Number,
        default: 1
    },
    Energy_level: {
        type: Text,
        default: "Energy"
    }
});

const { layoutConfig } = useLayout();
let documentStyle = getComputedStyle(document.documentElement);
let textColor = documentStyle.getPropertyValue('--text-color');
let textColorSecondary = documentStyle.getPropertyValue('--text-color-secondary');
let surfaceBorder = documentStyle.getPropertyValue('--surface-border');


const barData = ref(null);
const barOptions = ref(null);

const setColorOptions = () => {
    documentStyle = getComputedStyle(document.documentElement);
    textColor = documentStyle.getPropertyValue('--text-color');
    textColorSecondary = documentStyle.getPropertyValue('--text-color-secondary');
    surfaceBorder = documentStyle.getPropertyValue('--surface-border');
};

const setChart = () => {

    const mzValues = props.energyData.map(data => data["m/z"].toFixed(2));
    const intensityValues = props.energyData.map(data => data.intensity);

    barData.value = {
        labels: mzValues,
        datasets: [
            {
                label: 'Intensity',
                backgroundColor: documentStyle.getPropertyValue('--primary-500'),
                borderColor: documentStyle.getPropertyValue('--primary-500'),
                data: intensityValues,
                barPercentage: props.Bar_percentage, // 50%的理论宽度
                categoryPercentage: props.Cateory_percentage // 80%的类别宽度
            }
        ]
    };
    barOptions.value = {

        plugins: {
            legend: {
                labels: {
                    fontColor: textColor
                }
            }
        },
        scales: {
            x: {
                beginAtZero: true, // 在0开始
                type: 'linear', // 线性类型
                position: 'bottom', // 位置
                min: 0, // 最小值
                max: 200, // 最大值
               
                ticks: {
                    stepSize: 10,
                    color: textColorSecondary,
                    font: {
                        weight: 500
                    }
                },
                grid: {
                    display: false,
                    drawBorder: false
                },
            },
            y: {
                ticks: {
                    color: textColorSecondary
                },
                grid: {
                    color: surfaceBorder,
                    drawBorder: false
                }
            }
        }
    };
};

watch(
    layoutConfig.theme,
    () => {
        setColorOptions();
        setChart();
    },
    { immediate: true }
);
</script>

<template>
    <div class="grid p-fluid">
        <div class="col-12 xl:col-12">
            <div class="card">
                <h5>{{ props.Energy_level }}</h5>
                <Chart type="bar" :data="barData" :options="barOptions"></Chart>
            </div>
        </div>
    </div>
    <pre>{{ msg }}</pre> 
</template>
