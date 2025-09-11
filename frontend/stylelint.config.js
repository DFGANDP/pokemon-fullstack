// stylelint.config.js
/** @type {import('stylelint').Config} */
export default {
  extends: [
    // SCSS standard (zawiera reguły + plugin scss)
    'stylelint-config-standard-scss',

    // jeśli chcesz lżejszy zestaw, zamiast "standard-scss" możesz dać:
    // 'stylelint-config-recommended-scss',

    // ⬇️ na końcu: Vue + SCSS preset
    'stylelint-config-recommended-vue/scss',
  ],
  // opcjonalnie własne reguły
  rules: {
    // 'scss/at-rule-no-unknown': true,
    'selector-class-pattern': '^[a-z0-9]+(?:[-_]{1,2}[a-z0-9]+)*$',
  },
}
