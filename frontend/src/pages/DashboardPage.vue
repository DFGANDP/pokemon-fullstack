<template>
  <section>
    <h1>Dashboard</h1>
    <div v-if="loading">Ładowanie…</div>
    <div v-else-if="error">Błąd: {{ error }}</div>

    <div v-else class="grid">
      <VChart class="chart" :option="typeOption" autoresize />
      <VChart class="chart" :option="genOption" autoresize />
    </div>

    <PokemonTableBasic />
  </section>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { getSummary, type Summary } from '@/api'
import { buildTypeOption, buildGenOption } from '@/composables/useSummaryCharts'
import PokemonTableBasic from '@/components/PokemonTableBasic.vue'

const loading = ref(true)
const error = ref<string | null>(null)
const data = ref<Summary | null>(null)

const typeOption = computed(() =>
  data.value ? buildTypeOption(data.value.count_by_type) : null,
)
const genOption = computed(() =>
  data.value ? buildGenOption(data.value.count_by_generation) : null,
)

onMounted(async () => {
  try {
    data.value = await getSummary()
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Nieznany błąd'
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.grid {
  display: grid;
  gap: 15px;
}

@media (width >= 900px) {
  .grid {
    grid-template-columns: 1fr 1fr;
  }
}

.chart {
  width: 100%;
  height: 390px; /* dostosuj jak wolisz */
}
</style>
