<template>
  <section class="page">
    <PageHeader
      eyebrow="Learning path"
      title="SQL Learning Roadmap"
      :subtitle="roadmap?.description || 'Build SQL skills one pattern at a time.'"
    />

    <LoadingState v-if="isLoading" message="Loading roadmap..." />
    <ErrorState v-else-if="errorMessage" title="Could not load roadmap" :message="errorMessage" />
    <div v-else-if="modules.length" class="roadmap-grid">
      <RoadmapModuleCard
        v-for="module in modules"
        :key="module.id"
        :module="module"
      />
    </div>
    <EmptyState
      v-else
      title="Roadmap modules have not been added yet."
      message="Add module metadata in the backend roadmap JSON to start building the path."
    />
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";

import { fetchRoadmap } from "../api/roadmap";
import PageHeader from "../components/layout/PageHeader.vue";
import RoadmapModuleCard from "../components/roadmap/RoadmapModuleCard.vue";
import EmptyState from "../components/ui/EmptyState.vue";
import ErrorState from "../components/ui/ErrorState.vue";
import LoadingState from "../components/ui/LoadingState.vue";

const roadmap = ref(null);
const isLoading = ref(true);
const errorMessage = ref("");

const modules = computed(() => roadmap.value?.modules || []);

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
  gap: var(--space-4);
}
</style>
