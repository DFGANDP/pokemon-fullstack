<template>
  <section class="shell">
    <!-- NAV/HEADER STRIP (statyczny pasek info o aktualnym Pokemonie) -->
    <header class="nav">
      <div class="brand">
        <span class="dot" aria-hidden="true"></span>
        <h1>Pokédex</h1>
      </div>
      <div class="nav-tools">
        <span class="chip" v-if="data">#{{ String(data.number).padStart(3, '0') }} • {{ data.name }}</span>
        <span class="chip" v-if="data">{{ data.generation }}</span>
      </div>
    </header>

    <div v-if="loading" class="loading">Ładowanie…</div>
    <div v-else-if="error" class="error">Błąd: {{ error }}</div>

    <div v-else-if="data" class="content">
      <!-- LEFT: HERO / GŁÓWNA KARTA -->
      <section class="hero" aria-labelledby="poke-name">
        <span class="badge">
          {{ (data.types?.[0] || '—') }} • {{ data.generation }}
        </span>

        <div class="name">
          <h2 id="poke-name" class="truncate">
            {{ data.name.charAt(0).toUpperCase() + data.name.slice(1) }}
          </h2>
          <span class="muted">#{{ String(data.number).padStart(3, '0') }}</span>
        </div>

        <figure class="artwrap" aria-label="Sprite wybranego Pokémona">
          <img
            :src="data.image"
            :alt="data.name"
            width="320"
            height="320"
            fetchpriority="high"
          />
        </figure>

        <div class="meta" aria-label="Parametry podstawowe">
          <div class="kv">
            <div class="k">Wzrost</div>
            <div class="v">{{ data.height }}</div>
          </div>
          <div class="kv">
            <div class="k">Waga</div>
            <div class="v">{{ data.weight }}</div>
          </div>
          <div class="kv">
            <div class="k">Generacja</div>
            <div class="v">{{ data.generation }}</div>
          </div>
        </div>
      </section>

      <!-- RIGHT: KARTY SZCZEGÓŁÓW -->
      <aside class="stack">
        <!-- Types -->
        <article class="card">
          <h3>Typy</h3>
          <div class="types">
            <span
              v-for="t in data.types"
              :key="t"
              class="type"
            >
              {{ t }}
            </span>
          </div>
        </article>

        <!-- Abilities -->
        <article class="card">
          <h3>Zdolności</h3>
          <div class="types">
            <span
              v-for="ab in data.abilities"
              :key="ab"
              class="type"
            >
              {{ ab }}
            </span>
          </div>
        </article>

        <!-- Stats -->
        <article class="card" aria-labelledby="stats">
          <h3 id="stats">Statystyki bazowe</h3>
          <div class="stats">
            <div
              class="row"
              v-for="(val, key) in orderedStats"
              :key="key"
            >
              <div class="label">{{ key.replace('-', ' ') }}</div>
              <div class="bar" role="meter" aria-valuemin="0" aria-valuemax="255" :aria-valuenow="val">
                <div class="fill" :style="{ width: Math.min(100, Math.round((val / 255) * 100)) + '%' }"></div>
              </div>
              <div class="val">{{ val }}</div>
            </div>
          </div>
        </article>

        <!-- Evolution -->
        <article class="card">
          <h3>Ewolucja</h3>
          <div class="evo">
            <div class="evo-seg">
              <span class="muted">Z:</span>
              <template v-if="data.evolution.from.length">
                <RouterLink
                  v-for="prev in data.evolution.from"
                  :key="'from-' + prev"
                  :to="`/pokemon/${prev}`"
                  class="evo-link"
                >
                  {{ prev }}
                </RouterLink>
              </template>
              <span v-else class="muted-weak">Brak</span>
            </div>

            <div class="divider" aria-hidden="true"></div>

            <div class="evo-seg">
              <span class="muted">Do:</span>
              <template v-if="data.evolution.to.length">
                <RouterLink
                  v-for="nxt in data.evolution.to"
                  :key="'to-' + nxt"
                  :to="`/pokemon/${nxt}`"
                  class="evo-link"
                >
                  {{ nxt }}
                </RouterLink>
              </template>
              <span v-else class="muted-weak">Brak</span>
            </div>
          </div>
        </article>

        <!-- Moves -->
        <article class="card">
          <div class="card-head">
            <h3>Ruchy ({{ filteredMoves.length }})</h3>
            <input
              v-model="movesQuery"
              type="text"
              placeholder="Filtruj ruchy…"
              class="input"
              aria-label="Filtr ruchów"
            />
          </div>
          <div class="moves">
            <ul class="moves-grid">
              <li
                v-for="m in filteredMoves"
                :key="m"
                class="move"
              >
                {{ m }}
              </li>
            </ul>
          </div>
        </article>
      </aside>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { getPokemonDetails, type PokemonDetails } from '@/api';

const props = defineProps<{ name: string }>();

const loading = ref(true);
const error = ref<string | null>(null);
const data = ref<PokemonDetails | null>(null);
const movesQuery = ref('');

const orderedStats = computed(() => {
  if (!data.value) return {};
  const order = ['hp', 'attack', 'defense', 'special-attack', 'special-defense', 'speed'];
  const s = data.value.stats;
  const result: Record<string, number> = {};
  for (const k of order) if (k in s) result[k] = s[k];
  for (const k of Object.keys(s)) if (!(k in result)) result[k] = s[k];
  return result;
});

const filteredMoves = computed(() => {
  if (!data.value) return [];
  const q = movesQuery.value.trim().toLowerCase();
  if (!q) return data.value.moves;
  return data.value.moves.filter((m) => m.toLowerCase().includes(q));
});

async function load(name: string) {
  loading.value = true;
  error.value = null;
  try {
    const res = await getPokemonDetails(name.toLowerCase());
    data.value = res;
    document.title = `Pokédex — ${res.name.charAt(0).toUpperCase() + res.name.slice(1)}`;
  } catch (e: any) {
    error.value = e?.message ?? 'Nie znaleziono';
    data.value = null;
  } finally {
    loading.value = false;
  }
}

onMounted(() => load(props.name));
watch(() => props.name, (n) => load(n));
</script>

<style scoped>
:root{
  --bg: #0b0c0d; --surface:#111315; --text:#e7ebee; --muted:#a9b0b7;
  --accent:#f5c400; --card:#0f1113; --border:#1b1f23; --ring:#2a3137;
  --radius:16px; --shadow:0 16px 40px rgba(0,0,0,.35);
  --font: ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI","SF Pro Text",Roboto,"Helvetica Neue",Arial;
}

/* Layout */
.shell{
  width:min(1120px,100%);
  margin-inline:auto;
  padding:24px;
  font-family:var(--font);
  color:var(--text);
  background:
    radial-gradient(1200px 800px at 80% -10%, rgba(245,196,0,.10), transparent 60%),
    radial-gradient(1000px 600px at -10% 110%, rgba(255,255,255,.06), transparent 60%),
    var(--bg);
  display:grid;
  gap:20px;
  grid-template-columns: 1.15fr .85fr;
}
@media (max-width: 980px){ .shell{ grid-template-columns:1fr } }

.nav{
  grid-column:1/-1;
  display:flex; align-items:center; justify-content:space-between;
  background:color-mix(in oklab, var(--surface) 70%, transparent);
  border:1px solid var(--border);
  border-radius:calc(var(--radius)+4px);
  padding:12px 16px;
  box-shadow:var(--shadow);
  backdrop-filter:saturate(180%) blur(12px);
}
.brand{display:flex; gap:10px; align-items:center}
.dot{width:10px; height:10px; border-radius:50%; background:var(--accent); box-shadow:0 0 16px rgba(245,196,0,.45)}
.brand h1{margin:0; font-size:14px; letter-spacing:.22em; text-transform:uppercase; color:var(--muted)}
.nav-tools{display:flex; gap:10px; align-items:center}
.chip{border:1px solid var(--border); border-radius:999px; padding:6px 10px; font-size:12px; color:var(--muted)}

.loading, .error{
  grid-column:1/-1;
  border:1px solid var(--border);
  border-radius:var(--radius);
  background:var(--card);
  box-shadow:var(--shadow);
  padding:16px;
  font-size:14px;
}
.error{ color:#ff5959; border-color:#522; }

.content{
  display:contents;
}

/* Left: hero */
.hero{
  position:relative; overflow:hidden;
  border:1px solid var(--border); border-radius:var(--radius);
  background:linear-gradient(180deg, color-mix(in oklab, var(--card) 88%, transparent) 0%, var(--card) 100%);
  box-shadow:var(--shadow); padding:24px; display:grid; gap:16px; align-content:start;
  min-height: 520px;
}
.badge{
  display:inline-flex; align-items:center; gap:8px; font-size:12px; color:var(--muted);
  border:1px solid var(--ring); padding:6px 10px; border-radius:999px;
  background:color-mix(in oklab, var(--surface) 75%, transparent);
  width:max-content;
}
.name{display:flex; align-items:baseline; gap:12px}
.name h2{font-size:34px; margin:8px 0 0; line-height:1.1}
.muted{font-size:14px; color:var(--muted)}
.muted-weak{color:color-mix(in oklab, var(--muted) 70%, #ffffff 0%)}

.artwrap{
  position:relative; aspect-ratio: 1.4/1; border-radius:12px; border:1px dashed var(--ring);
  display:grid; place-items:center;
  background:
    radial-gradient(700px 300px at 50% 0%, rgba(245,196,0,.20), transparent 65%),
    linear-gradient(180deg, color-mix(in oklab, var(--surface) 90%, transparent) 0%, transparent 100%);
  overflow:hidden;
}
.artwrap img{
  width:min(320px, 60%);
  height:auto;
  image-rendering:pixelated;
  transform:translateY(6px)
}

.meta{
  display:grid; grid-template-columns:repeat(3,1fr); gap:10px; margin-top:4px
}
.kv{
  border:1px solid var(--ring); border-radius:12px; padding:10px 12px;
  background:color-mix(in oklab, var(--surface) 85%, transparent)
}
.kv .k{font-size:11px; color:var(--muted); letter-spacing:.08em; text-transform:uppercase}
.kv .v{font-size:16px; margin-top:4px}

/* Right: cards */
.stack{ display:grid; gap:12px }
.card{
  border:1px solid var(--border);
  border-radius:var(--radius);
  background:var(--card);
  box-shadow:var(--shadow);
  padding:18px;
}
.card h3{
  margin:0 0 12px;
  font-size:16px;
  letter-spacing:.06em;
  text-transform:uppercase;
  color:var(--muted);
}

.types{display:flex; gap:8px; flex-wrap:wrap}
.type{
  border:1px solid var(--ring); border-radius:999px; padding:6px 10px; font-weight:600;
  background:linear-gradient(180deg, rgba(245,196,0,.15), transparent);
  font-size:12px;
}

/* Stats */
.stats{display:grid; gap:12px}
.row{display:grid; grid-template-columns:140px 1fr 52px; gap:10px; align-items:center}
.label{color:var(--muted); font-size:13px; text-transform:capitalize}
.bar{height:10px; border-radius:999px; background:color-mix(in oklab, var(--ring) 90%, transparent); overflow:hidden; position:relative}
.fill{
  position:absolute; inset:0 auto 0 0; width:0%;
  background:linear-gradient(90deg, var(--accent), #ffd84b);
  border-radius:inherit;
  transition:width 600ms cubic-bezier(.2,.7,.2,1);
}
.val{font-variant-numeric:tabular-nums; text-align:right; color:var(--muted)}

/* Evolution */
.evo{ display:flex; align-items:center; gap:12px; flex-wrap:wrap }
.evo-seg{ display:flex; align-items:center; gap:8px; flex-wrap:wrap }
.evo-link{
  text-decoration: underline;
  text-underline-offset: 3px;
  text-transform: capitalize;
  color:var(--text);
}
.evo-link:hover{ opacity:.85 }
.divider{ width:1px; height:20px; background:var(--ring) }

/* Moves */
.card-head{ display:flex; gap:12px; align-items:center; justify-content:space-between; flex-wrap:wrap }
.input{
  flex:0 1 260px;
  border:1px solid var(--ring);
  border-radius:12px;
  padding:10px 12px;
  background:transparent;
  color:var(--text);
  outline:none;
}
.input:focus{ box-shadow:0 0 0 3px color-mix(in oklab, var(--accent) 20%, transparent) }
.moves{ max-height:300px; overflow:auto; border-top:1px solid var(--ring); margin-top:10px; padding-top:10px }
.moves-grid{ display:grid; gap:8px; grid-template-columns:repeat(2,1fr) }
@media (max-width: 520px){ .moves-grid{ grid-template-columns:1fr } }
.move{
  text-transform:capitalize;
  padding:10px 12px;
  border:1px solid var(--ring);
  border-radius:12px;
  background:color-mix(in oklab, var(--surface) 85%, transparent);
  font-size:13px;
  white-space:nowrap; overflow:hidden; text-overflow:ellipsis;
}

/* Utilities */
.truncate{overflow:hidden; text-overflow:ellipsis; white-space:nowrap}
</style>
