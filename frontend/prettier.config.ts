// eslint.config.ts
import eslint from '@eslint/js'
import tseslint from 'typescript-eslint'
import pluginVue from 'eslint-plugin-vue'
import globals from 'globals'

// Uwaga: flat config = eksport tablicy configów
export default tseslint.config(
  // 1) Ignory i ogólne opcje
  {
    ignores: ['dist/**', 'node_modules/**'],
    languageOptions: {
      ecmaVersion: 2024,
      globals: { ...globals.browser },
    },
  },

  // 2) Podstawowe reguły JS od ESLint
  eslint.configs.recommended,

  // 3) Vue (flat/recommended) — ustawia vue-eslint-parser dla .vue
  ...pluginVue.configs['flat/recommended'],

  // 4) TypeScript dla plików .ts/.tsx
  {
    files: ['**/*.ts', '**/*.tsx'],
    plugins: { '@typescript-eslint': tseslint.plugin },
    languageOptions: {
      parser: tseslint.parser,
      parserOptions: {
        // jeśli chcesz "type-aware rules", ustaw project: true i dodaj tsconfig(es)
        // project: true,
      },
    },
    rules: {
      // tu ewentualne TS-specyficzne reguły
    },
  },

  // 5) TS wewnątrz <script lang="ts"> w .vue
  {
    files: ['**/*.vue'],
    languageOptions: {
      parserOptions: {
        // vue-eslint-parser zostaje; TS parser wskazujemy jako "wewnętrzny"
        parser: tseslint.parser,
        ecmaVersion: 2024,
      },
    },
    rules: {
      // Twoje reguły dla Vue
      'vue/multi-word-component-names': 'off',
    },
  },

  // 6) Wyłącz stylistyczne konflikty z Prettier
  // (zalecane przez Prettiera i ESLint przy wspólnym użyciu)
  // Można też użyć `import eslintConfigPrettier from 'eslint-config-prettier/flat'`
  // i dodać go na końcu — efekt identyczny.
)
