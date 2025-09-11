type CountMap = Record<string, number>;

function pickCssVar(name: string, fallback: string) {
  const v = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  return v || fallback;
}

function theme() {
  const text   = pickCssVar('--text',   '#0b0c0d');
  const muted  = pickCssVar('--muted',  '#6b7280');
  const ring   = pickCssVar('--ring',   '#e5e7eb');
  const accent = pickCssVar('--accent', '#f5c400');
  const card   = pickCssVar('--card',   '#ffffff');
  const bg     = pickCssVar('--bg',     '#fafbfc');

  const accentSoft = 'rgba(245,196,0,0.35)';
  return { text, muted, ring, accent, accentSoft, card, bg };
}

function baseOption(title: string) {
  const t = theme();
  return {
    backgroundColor: 'transparent',
    textStyle: { fontFamily: 'ui-sans-serif, -apple-system, Segoe UI, Roboto, Arial' },
    title: {
      text: title,
      left: 8,
      top: 6,
      textStyle: { color: t.muted, fontSize: 14, fontWeight: 600, letterSpacing: 0.3 },
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: t.card,
      borderColor: t.ring,
      borderWidth: 1,
      padding: [8, 10],
      textStyle: { color: t.text, fontSize: 12 },
      extraCssText: 'box-shadow:0 12px 28px rgba(0,0,0,.12); border-radius:10px;',
    },
    grid: { left: 12, right: 12, top: 48, bottom: 40, containLabel: true },
    xAxis: {
      type: 'category',
      axisLine: { lineStyle: { color: t.ring } },
      axisTick: { show: false },
      axisLabel: { color: t.muted, fontSize: 12, margin: 12 },
      splitLine: { show: false },
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: { color: t.muted, fontSize: 12, margin: 8 },
      splitLine: { show: true, lineStyle: { color: t.ring, width: 1 } },
    },
    dataZoom: [
      { type: 'inside', zoomOnMouseWheel: true, moveOnMouseMove: true },
      {
        type: 'slider',
        height: 12,
        bottom: 8,
        handleSize: 0,
        borderColor: 'transparent',
        backgroundColor: 'transparent',
        fillerColor: theme().accentSoft,
      },
    ],
    animation: true,
    animationDuration: 600,
    animationEasing: 'cubicOut',
    media: [
      {
        query: { maxWidth: 520 },
        option: {
          grid: { left: 8, right: 8, top: 44, bottom: 48, containLabel: true },
          xAxis: { axisLabel: { rotate: 35 } },
        },
      },
      {
        query: { minWidth: 521 },
        option: {
          xAxis: { axisLabel: { rotate: 20 } },
        },
      },
    ],
  } as const;
}

function barSeries(values: number[]) {
  const t = theme();
  return [
    {
      name: 'Count',
      type: 'bar',
      data: values,
      barWidth: '52%',
      itemStyle: {
        borderRadius: [8, 8, 6, 6],
        color: {
          type: 'linear',
          x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: t.accent },
            { offset: 1, color: t.accentSoft },
          ],
        },
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 16,
          shadowColor: 'rgba(0,0,0,0.18)',
          opacity: 0.95,
        },
      },
      label: {
        show: true,
        position: 'top',
        formatter: ({ value }: any) => (value ?? ''),
        color: theme().muted,
        fontSize: 11,
      },
    },
  ];
}

function toBarOption(
  title: string,
  map: CountMap,
  sort: 'desc' | 'alpha' | 'none' = 'desc'
) {
  let entries = Object.entries(map);
  if (sort === 'desc') entries = entries.sort((a, b) => b[1] - a[1]);
  if (sort === 'alpha') entries = entries.sort((a, b) => a[0].localeCompare(b[0]));

  const categories = entries.map(([k]) => k);
  const values = entries.map(([, v]) => v);

  const opt = baseOption(title);
  return {
    ...opt,
    xAxis: { ...opt.xAxis, data: categories },
    series: barSeries(values),
  };
}

export const buildTypeOption = (m: CountMap) =>
  toBarOption('Pokémon by Type', m, 'desc');

export const buildGenOption = (m: CountMap) =>
  toBarOption('Pokémon by Generation', m, 'desc');
