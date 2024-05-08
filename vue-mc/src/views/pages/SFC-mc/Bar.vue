<script setup>
import { ref, watch } from 'vue';
import { createApp, h } from 'vue';
import { useLayout } from '@/layout/composables/layout';
import RDKit from './RDKit-SVG.vue'

const props = defineProps({
    energyData: {
        type: Object,
        default: () => ({ })
    },
    Energy_level: {
        type: String,
        default: "Energy"
    }
});

const getOrCreateTooltip = (chart) => {
    let tooltipEl = chart.canvas.parentNode.querySelector('div');

    if (!tooltipEl) {
        tooltipEl = document.createElement('div');
        tooltipEl.style.opacity = 0;
        tooltipEl.style.position = 'absolute';
        tooltipEl.style.pointerEvents = 'none';
        tooltipEl.style.transition = 'all .1s ease';

        chart.canvas.parentNode.appendChild(tooltipEl);
    }

    return tooltipEl;
};

const externalTooltipHandler = (context) => {
    const { chart, tooltip } = context;
    const tooltipEl = getOrCreateTooltip(chart);

    if (tooltip.opacity === 0) {
        tooltipEl.style.opacity = 0;
        return;
    }
  
    let tooltipMolecule = '';
    if (tooltip.dataPoints && tooltip.dataPoints.length) {
        const dataPoint = tooltip.dataPoints[0];
        const mzValue = dataPoint.label;
        tooltipMolecule = props.energyData[mzValue][1][1];
    }

    const RDKitApp = createApp({
        render() {
            return h(RDKit, { molecules: tooltipMolecule });
        },
    });

    const rdkitContainer = document.createElement('div');
    RDKitApp.mount(rdkitContainer);

    tooltipEl.innerHTML = '';
    tooltipEl.appendChild(rdkitContainer);

    const { offsetLeft: positionX, offsetTop: positionY } = chart.canvas;

    tooltipEl.style.opacity = 1;
    const canvasWidth = chart.canvas.offsetWidth;
    const canvasCenter = canvasWidth / 2;
    
    const tooltipX = tooltip.caretX;
    
    const xOffset = tooltipX < canvasCenter ? 0 : -250; 
    const yOffset = tooltipX < canvasCenter ? -200 : -180; 

    tooltipEl.style.left = positionX + tooltipX + xOffset + 'px';
    tooltipEl.style.top = positionY + tooltip.caretY + yOffset + 'px'; 
    tooltipEl.style.pointerEvents = 'none'; 
};

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

    //const mzValues = Object.keys(props.energyData).map(key => parseFloat(key));
    const mzValues = Object.keys(props.energyData);
    const intensityValues = Object.keys(props.energyData).map(key => parseFloat(props.energyData[key][0]));
    barData.value = {
        labels: mzValues,
        datasets: [
            {
                label: 'Intensity',
                backgroundColor: documentStyle.getPropertyValue('--primary-500'),
                borderColor: documentStyle.getPropertyValue('--primary-500'),
                data: intensityValues,
                barThickness: 7,
                //barPercentage: 0.7
                //categoryPercentage: 0.6
            }
        ]
    };
    barOptions.value = {

        plugins: {
            tooltip: {
                enabled: true, 
                external: externalTooltipHandler,
                position: 'nearest'
            },
            legend: {
                labels: {
                    fontColor: textColor
                }
            }
        },
        scales: {
            x: {
                beginAtZero: true,
                type: 'linear', 
                position: 'bottom', 
                //min: 0,
                //max: 200, 
               
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
</template>
