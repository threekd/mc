<script setup>
import { ref, watch } from 'vue';
import { useLayout } from '@/layout/composables/layout';
import RDKit from './RDKit-Vue/ExampleSVG.vue'


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

const showToolTip = ref(false);
const toolTipPosition = ref({x: 0, y: 0});
const scrollX = window.scrollX;
const scrollY = window.scrollY;
const molecules = ref('CNCCC1=CNC2=CC=CC=C21')


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
                barPercentage: props.Bar_percentage,
                categoryPercentage: props.Cateory_percentage
            }
        ]
    };
    barOptions.value = {

        plugins: {
            tooltip: {
                enabled: false, // 正确地禁用默认工具提示
                external: function(context) {
                    // 使用context.tooltip而不是tooltipModel访问工具提示模型
                    const tooltip = context.tooltip;
                    if (tooltip.opacity === 0) {
                        showToolTip.value = false;
                        return;
                    }
                    showToolTip.value = true;
                    // 使用context.chart.canvas而不是this._chart.canvas
                    const position = context.chart.canvas.getBoundingClientRect();
                    toolTipPosition.value = {
                        x: position.left + scrollX,
                        y: position.top + scrollY
                    };
                }
            },
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
    <div v-show="showToolTip" :style="{position: 'absolute', left: toolTipPosition.x + 'px', top: toolTipPosition.y + 'px'}">
        <RDKit :molecules="molecules"/>
    </div>
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
