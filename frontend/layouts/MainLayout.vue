<template>
  <header>
    <div class="container">
      <nav class="nav">
        <RouterLink to="/">Dashboard</RouterLink>
      </nav>
    </div>
  </header>

  <main>
    <div class="container">
      <slot />
    </div>
  </main>
</template>

<script setup lang="ts"></script>

<style scoped>
header {
  position: sticky; top: 0;
  border-bottom: 1px solid var(--line);
  background: var(--bg); z-index: 10;
}
.nav { display: flex; gap: 16px; padding: 12px 0; }
main { padding: 32px 0; }
</style>
