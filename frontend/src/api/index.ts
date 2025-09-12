// src/api/index.ts
import { request } from './http'

export interface Summary {
  total_pokemon: number
  count_by_type: Record<string, number>
  count_by_generation: Record<string, number>
}

export const getSummary = () => request<Summary>('/api/v1/summary/')

// Pokemon Table row
export interface PokemonRow {
  number: number
  name: string
  generation: string
  height: number
  weight: number
  type_one: string
  type_two?: string | null
  moves_count: number
}

// Dopuszczalne wartości sortowania (dopasuj do backendu, tu najbezpieczniejsze kolumny liczbowe/tekstowe):
export type SortBy =
  | 'number'
  | 'name'
  | 'generation'
  | 'height'
  | 'weight'
  | 'moves_count'

export type SortOrder = 'asc' | 'desc'

export interface PokemonQuery {
  limit?: number // domyślnie 25
  offset?: number // domyślnie 0
  number?: number | null // filtr po number
  name?: string | null // filtr po name
  move?: string | null // filtr po move
  type?: string | null // filtr po type
  generation?: string | null // filtr po generation
  sort_by?: SortBy
  sort_order?: SortOrder
}

// Helper do budowania query string – ignoruje puste/undefined/null
function toQuery(params: Partial<PokemonQuery> = {}): string {
  const search = new URLSearchParams()

  // doprecyzowanie krotek, żeby TS wiedział co iterujemy
  for (const [k, v] of Object.entries(params) as [keyof PokemonQuery, unknown][]) {
    if (v === undefined || v === null || v === '') continue
    search.append(String(k), String(v))
  }

  const s = search.toString()
  return s ? `?${s}` : ''
}

// Główna funkcja pobierająca wiersze tabeli
export function getPokemonTable(
  params: PokemonQuery = {
    limit: 25,
    offset: 0,
    sort_by: 'number',
    sort_order: 'asc',
  },
  init?: RequestInit,
) {
  const qs = toQuery(params)
  return request<PokemonRow[]>(`/api/v1/pokemon/${qs}`, init)
}

export interface PokemonDetails {
  number: number
  name: string
  generation: string
  height: number
  weight: number
  types: string[]
  stats: Record<string, number>
  moves: string[]
  abilities: string[]
  evolution: { from: string[]; to: string[] } // <-- zmiana
  image: string
}

export const getPokemonDetails = (name: string) =>
  request<PokemonDetails>(`/api/v1/details/${encodeURIComponent(name)}`)
