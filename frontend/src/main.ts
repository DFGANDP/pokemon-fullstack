import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";
import router from './router';


import './plugins/echarts';      // <-- rejestracja typów wykresów
import VChart from 'vue-echarts'; // <-- komponent wykresu

import { installPrimeVue } from './plugins/primevue';

createApp(App)
  .use(router)
  .use(installPrimeVue) // ładny, czysty main
  .component('VChart', VChart)   // <-- globalny komponent
  .mount('#app');