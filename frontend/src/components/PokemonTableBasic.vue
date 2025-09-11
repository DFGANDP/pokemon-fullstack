<template>
  <section class="p-6">
    <h1 class="mb-3">Pokémon Table</h1>
    <!-- FILTRY -->
    <div class="filters mb-3">
      <label>
        # Number:
        <input type="number" v-model.number="fNumber" placeholder="np. 25" />
      </label>
      <label>
        Name:
        <input type="text" v-model.trim="fName" placeholder="np. char" />
      </label>
      <label>
        Generation:
        <select v-model="fGeneration">
          <option value="">All</option>
          <option v-for="g in GENERATIONS" :key="g" :value="g">{{ g }}</option>
        </select>
      </label>
      <label>
        Type:
        <select v-model="fType">
          <option value="">All</option>
          <option v-for="t in TYPES" :key="t" :value="t">{{ t }}</option>
        </select>
      </label>
      <label>
        Move:
        <input type="text" v-model.trim="fMove" placeholder="np. tackle" />
      </label>
    </div>
    <div v-if="loading">Ładowanie…</div>
    <div v-else-if="error">Błąd: {{ error }}</div>

    <DataTable
      v-else
      :value="rows"
      dataKey="number"
      class="w-full custom-table"
      scrollable
      scrollHeight="384px"
      size="small"
      :sortField="sortBy"
      :sortOrder="primeSortOrder"
      @sort="onSort"
    >
      <Column field="number" header="#" :sortable="true"/>
      <Column field="name" header="Name" :sortable="true">
      <template #body="{ data }">
        <RouterLink
          class="name-link"
          :to="{ name: 'pokemon-by-name', params: { name: data.name } }"
        >
          {{ data.name }}
        </RouterLink>
      </template>
      </Column>
      <Column field="generation" header="Generation" :sortable="true"/>
      <Column field="height" header="Height" :sortable="true"/>
      <Column field="weight" header="Weight" :sortable="true"/>
      <Column header="Types">
        <template #body="{ data }">
          <span>{{ data.type_one }}</span>
          <span v-if="data.type_two"> / {{ data.type_two }}</span>
        </template>
      </Column>
      <Column field="moves_count" header="Moves" :sortable="true"/>
    </DataTable>

    <!-- NAWIGACJA -->
    <div class="flex justify-between mt-4">
      <button
        class="p-button p-button-outlined"
        :disabled="offset === 0"
        @click="prevPage"
      >
        ← Prev
      </button>
      <button
        class="p-button p-button-outlined"
        @click="nextPage"
      >
        Next →
      </button>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue';
import { getPokemonTable, type PokemonRow } from '@/api';

import DataTable from 'primevue/datatable';
import Column from 'primevue/column';

const rows = ref<PokemonRow[]>([]);
const loading = ref(true);
const error = ref<string | null>(null);

const limit = 25;
const offset = ref(0);

// --- SORT (stan frontu, mapowany na backend) ---
const sortBy = ref<'number' | 'name' | 'generation' | 'height' | 'weight' | 'moves_count'>('number');
const sortOrder = ref<'asc' | 'desc'>('asc'); // backendowe wartości
// PrimeVue używa 1 dla asc i -1 dla desc:
const primeSortOrder = computed(() => (sortOrder.value === 'asc' ? 1 : -1));

// --- FILTRY (mapują się 1:1 na paramy w backendzie) ---
const GENERATIONS = [
  'Generation I','Generation II','Generation III','Generation IV','Generation V',
  'Generation VI','Generation VII','Generation VIII','Generation IX',
] as const;
const TYPES = [
  'normal','fire','water','electric','grass','ice','fighting','poison','ground',
  'flying','psychic','bug','rock','ghost','dragon','dark','steel','fairy',
] as const;

const fNumber = ref<number | null>(null);
const fName = ref('');
const fGeneration = ref<string>('');
const fType = ref<string>('');
const fMove = ref<string>(''); // jeśli chcesz po nazwie ruchu (API: move?: string)

// AbortController do przerywania poprzednich requestów przy szybkim wpisywaniu
let controller: AbortController | null = null;
// prosty debounce (300 ms) dla inputów tekstowych
let debounceTimer: number | undefined;

async function loadData() {
  loading.value = true;
  try {
    // jeśli poprzedni request jeszcze leci – anuluj go
    controller?.abort();
    controller = new AbortController();

    rows.value = await getPokemonTable(
      {
        limit,
        offset: offset.value,
        sort_by: sortBy.value,
        sort_order: sortOrder.value,
        number: fNumber.value ?? null,
        name: fName.value || null,
        generation: fGeneration.value || null,
        type: fType.value || null,
        move: fMove.value || null,
      },
      { signal: controller.signal }
    );
  } catch (e: unknown) {
    if ((e as Error).name !== 'AbortError') {
      error.value = e instanceof Error ? e.message : String(e);
    }
  } finally {
    loading.value = false;
  }
}


// --- Reakcja na zmiany filtrów ---
function triggerReloadDebounced() {
  // zmiana filtra cofamy na początek:
  offset.value = 0;
  // debounce: czekamy 300 ms od ostatniego wpisu
  clearTimeout(debounceTimer);
  // @ts-expect-error: w DOM typ timera to number
  debounceTimer = setTimeout(() => {
    loadData();
  }, 300);
}

// number – bez debounce (enter/zmiana wartości)
watch(fNumber, () => {
  offset.value = 0;
  loadData();
});
// tekstowe – z debounce
watch([fName, fMove], () => {
  triggerReloadDebounced();
});
// selecty – bez debounce
watch([fGeneration, fType], () => {
  offset.value = 0;
  loadData();
});

function onSort(e: { sortField?: string; sortOrder?: 1 | -1 }) {
  if (e.sortField) {
    // pole z atrybutu `field` w Column (np. 'height', 'name' itd.)
    sortBy.value = e.sortField as typeof sortBy.value;
  }
  if (e.sortOrder === 1) sortOrder.value = 'asc';
  else if (e.sortOrder === -1) sortOrder.value = 'desc';
  // po zmianie sortowania wracamy na początek
  offset.value = 0;
  loadData();
}

function nextPage() {
  offset.value += limit;
  loadData();
}

function prevPage() {
  if (offset.value >= limit) {
    offset.value -= limit;
    loadData();
  }
}

onMounted(() => {
  loadData();
});
</script>

<style scoped>
.custom-table :deep(.p-datatable-thead > tr > th) {
  background-color: #777272;
  font-weight: 600;
}

/* styl linku w komórce Name */
.name-link {
  color: inherit;        /* niebieski znika, dziedziczy kolor */
  font-weight: 700;      /* pogrubienie */
  text-decoration: none; /* bez podkreślenia */
  text-transform: capitalize; /* <-- pierwsza litera duża */
}
.name-link:hover {
  text-decoration: underline; /* opcjonalny hover */
}

/* layout paska filtrów (prosto i czytelnie) */
.filters {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 12px;
}
.filters label {
  display: flex;
  flex-direction: column;
  font-size: 12px;
  gap: 6px;
}
.filters input, .filters select {
  padding: 6px 8px;
  border: 1px solid #ddd;
  border-radius: 6px;
}
</style>
