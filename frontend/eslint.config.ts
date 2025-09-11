// eslint.config.ts
import { defineConfig } from 'eslint/config'
import eslint from '@eslint/js'
import pluginVue from 'eslint-plugin-vue'
import tseslint from 'typescript-eslint'
import eslintConfigPrettier from 'eslint-config-prettier/flat'

export default defineConfig([
  { ignores: ['dist/**', 'node_modules/**'] },

  eslint.configs.recommended,
  ...pluginVue.configs['flat/recommended'],
  ...tseslint.configs.recommended,

  // ⬇️ JEDYNA potrzebna zmiana: użyj parserOptions.parser (NIE languageOptions.parser)
  {
    files: ['**/*.vue'],
    languageOptions: {
      parserOptions: {
        // ważne: tu wskazujemy parser TS, a parserem głównym dla .vue
        // nadal jest vue-eslint-parser z presetów pluginVue
        parser: tseslint.parser,
        ecmaVersion: 2024,
        sourceType: 'module',
      },
    },
    rules: {
      'vue/multi-word-component-names': 'off',
    },
  },

  // na końcu wyciszamy konflikty z Prettier
  eslintConfigPrettier,
])
