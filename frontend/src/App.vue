<template>
  <div class="app-shell">
    <AppNavbar :workspace="isWorkspaceRoute" />
    <main :class="mainClass">
      <RouterView />
    </main>
    <footer class="app-footer" :class="{ 'is-workspace-footer': isWorkspaceRoute }">
      <a
        href="https://svictor.vercel.app"
        target="_blank"
        rel="noopener noreferrer"
      >
        LeetPrep-SQL by Shane Victor
      </a>
      <span>Local progress. No account required.</span>
    </footer>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";

import AppNavbar from "./components/layout/AppNavbar.vue";

const route = useRoute();
const workspaceRoutes = ["roadmap-lesson", "roadmap-boss"];

const isWorkspaceRoute = computed(() => workspaceRoutes.includes(route.name));
const mainClass = computed(() =>
  isWorkspaceRoute.value ? "workspace-container" : "page-container",
);
</script>
