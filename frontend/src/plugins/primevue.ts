// src/plugins/primevue.ts
import type { App } from 'vue'
import PrimeVue from 'primevue/config'

// Wybierz jeden preset: Aura, Lara, Material, Nora itp.
// (tu przykład z Aura)
import Aura from '@primeuix/themes/aura'

// Ikony + (opcjonalnie) PrimeFlex
import 'primeicons/primeicons.css'
import 'primeflex/primeflex.css'

export function installPrimeVue(app: App) {
  app.use(PrimeVue, {
    theme: {
      preset: Aura, // <- najważniejsze: preset z @primeuix/themes
      options: {
        prefix: 'p',
        darkModeSelector: 'system', // automatyczny dark, możesz zmienić na 'class'
        cssLayer: false,
      },
    },
    // opcjonalnie:
    // ripple: true,
    // inputVariant: 'filled'
  })
}
