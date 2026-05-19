<template>
  <div class="app-shell">
    <AppNavbar />
    <main class="page-container">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import AppNavbar from "./components/layout/AppNavbar.vue";
</script>
