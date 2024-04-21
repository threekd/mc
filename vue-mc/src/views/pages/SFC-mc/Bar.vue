<script setup>
import { ref, watch } from 'vue';
import { createApp, h } from 'vue';
import { useLayout } from '@/layout/composables/layout';
import RDKit from './RDKit-SVG.vue'

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
        type: String,
        default: "Energy"
    }
});


const getOrCreateTooltip = (chart) => {
  let tooltipEl = chart.canvas.parentNode.querySelector('div');

  if (!tooltipEl) {
    tooltipEl = document.createElement('div');
    tooltipEl.style.background = 'rgba(0, 0, 0, 0)';
    tooltipEl.style.borderRadius = '3px';
    tooltipEl.style.color = 'white';
    tooltipEl.style.opacity = 1;
    tooltipEl.style.pointerEvents = 'none';
    tooltipEl.style.position = 'absolute';
    tooltipEl.style.transform = 'translate(-50%, 0)';
    tooltipEl.style.transition = 'all .1s ease';

    const table = document.createElement('table');
    table.style.margin = '0px';

    tooltipEl.appendChild(table);
    chart.canvas.parentNode.appendChild(tooltipEl);
  }

  return tooltipEl;
};

const externalTooltipHandler = (context) => {
    const { chart, tooltip } = context;
  const tooltipEl = getOrCreateTooltip(chart);

  // Hide if no tooltip
  if (tooltip.opacity === 0) {
    tooltipEl.style.opacity = 0;
    return;
  }

   let tooltipMolecule = 'CNCCC1=CNC2=CC=CC=C21'; // 通过 tooltip 获取分子数据


   if (tooltip.dataPoints && tooltip.dataPoints.length) {
    const dataPoint = tooltip.dataPoints[0];
    const mzValue = dataPoint.label; 
    console.log(mzValue)

    tooltipMolecule = props.energyData[mzValue][1][1]; // Now it is safe to set the molecule data
}

  const RDKitApp = createApp({
    render() {
      // 确保你在这里传递正确的分子字符串
      return h(RDKit, { molecules: tooltipMolecule }); 
    },
  });

  // 创建包装容器来挂载我们的 RDKit 组件
  const rdkitContainer = document.createElement('div');
  
  // 将 RDKit Vue 应用挂载到创建的 div 容器上
  RDKitApp.mount(rdkitContainer);

  // Set Text
  if (tooltip.body) {
    const titleLines = tooltip.title || [];
    const bodyLines = tooltip.body.map(b => b.lines);

    const tableHead = document.createElement('thead');

    titleLines.forEach(title => {
      // ...
    });

    const tableBody = document.createElement('tbody');
    bodyLines.forEach((body, i) => {
      // ...
    });

    const rdkitWrapperTr = document.createElement('tr');
    const rdkitWrapperTd = document.createElement('td');
    rdkitWrapperTd.colSpan = '2'; // 让 RDKit 组件占据整个宽度
    rdkitWrapperTd.appendChild(rdkitContainer); // 把 RDKit 组件附加到单元格
    rdkitWrapperTr.appendChild(rdkitWrapperTd);
    tableBody.appendChild(rdkitWrapperTr); // 将 RDKit 的行添加到表格主体

    const tableRoot = tooltipEl.querySelector('table');

    // Remove old children
    while (tableRoot.firstChild) {
      tableRoot.firstChild.remove();
    }

    // Add new children
    tableRoot.appendChild(tableHead);
    tableRoot.appendChild(tableBody);
  }

  const {offsetLeft: positionX, offsetTop: positionY} = chart.canvas;

  // Display, position, and set styles for font

  const topoffset = -100
  const leftoffset = 180
  tooltipEl.style.opacity = 1;
  tooltipEl.style.left = leftoffset + positionX + tooltip.caretX + 'px';
  tooltipEl.style.top = topoffset + positionY + tooltip.caretY + 'px';
  tooltipEl.style.font = tooltip.options.bodyFont.string;
  tooltipEl.style.padding = tooltip.options.padding + 'px ' + tooltip.options.padding + 'px';
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
                barPercentage: props.Bar_percentage,
                categoryPercentage: props.Cateory_percentage
            }
        ]
    };
    barOptions.value = {

        plugins: {
            tooltip: {
                enabled: true, // 正确地禁用默认工具提示
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
    <pre>{{ props.energyData['144.081'][1][1]}}</pre>
    <div class="grid p-fluid">
        <div class="col-12 xl:col-12">
            <div class="card">
                <h5>{{ props.Energy_level }}</h5>
                <Chart type="bar" :data="barData" :options="barOptions"></Chart>
            </div>
        </div>
    </div>
</template>
