// src/plugins/echarts.ts
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { BarChart } from 'echarts/charts';
import { GridComponent, TooltipComponent, TitleComponent, LegendComponent } from 'echarts/components';

use([CanvasRenderer, BarChart, GridComponent, TooltipComponent, TitleComponent, LegendComponent]);
