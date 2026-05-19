<template>
  <section>
    <header class="page-header">
      <h1 class="page-title">{{ roadmap?.title || "SQL Learning Roadmap" }}</h1>
      <p class="page-subtitle">
        {{ roadmap?.description || "Build SQL skills one pattern at a time." }}
      </p>
    </header>

    <div v-if="isLoading" class="empty-state">Loading roadmap...</div>
    <div v-else-if="errorMessage" class="empty-state">{{ errorMessage }}</div>
    <div v-else class="roadmap-grid">
      <RoadmapModuleCard
        v-for="module in roadmap.modules"
        :key="module.id"
        :module="module"
      />
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from "vue";

import { fetchRoadmap } from "../api/roadmap";
import RoadmapModuleCard from "../components/RoadmapModuleCard.vue";

const roadmap = ref(null);
const isLoading = ref(true);
const errorMessage = ref("");

onMounted(async () => {
  try {
    roadmap.value = await fetchRoadmap();
  } catch (error) {
    errorMessage.value = error.message;
  } finally {
    isLoading.value = false;
  }
});
</script>

<style scoped>
.roadmap-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 16px;
}
</style>
