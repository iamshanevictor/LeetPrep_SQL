<template>
  <section class="page">
    <PageHeader
      eyebrow="Practice library"
      title="Problems"
      subtitle="Standalone SQL practice problems will appear here after the learning roadmap content is expanded."
    />

    <LoadingState v-if="isLoading" message="Loading problems..." />
    <ErrorState v-else-if="errorMessage" title="Could not load problems" :message="errorMessage" />
    <div v-else-if="problems.length" class="problem-grid">
      <article v-for="problem in problems" :key="problem.id" class="card problem-card">
        <div class="card-header">
          <h2 class="card-title">{{ problem.title }}</h2>
          <p class="card-description">{{ problem.description }}</p>
        </div>
        <RouterLink class="button button-secondary" :to="`/problems/${problem.id}`">
          Open Problem
        </RouterLink>
      </article>
    </div>
    <EmptyState
      v-else
      title="No practice problems yet."
      message="Add standalone problem instructions later. For now, use the roadmap to learn the SQL patterns step by step."
      action-label="Open Roadmap"
      action-to="/roadmap"
    />
  </section>
</template>

<script setup>
import { onMounted, ref } from "vue";

import { fetchProblems } from "../api/problems";
import PageHeader from "../components/layout/PageHeader.vue";
import EmptyState from "../components/ui/EmptyState.vue";
import ErrorState from "../components/ui/ErrorState.vue";
import LoadingState from "../components/ui/LoadingState.vue";

const problems = ref([]);
const isLoading = ref(true);
const errorMessage = ref("");

onMounted(async () => {
  try {
    const data = await fetchProblems();
    problems.value = data.problems || [];
  } catch (error) {
    errorMessage.value = error.message;
  } finally {
    isLoading.value = false;
  }
});
</script>

<style scoped>
.problem-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: var(--space-4);
}

.problem-card {
  display: grid;
  align-content: space-between;
  gap: var(--space-4);
}
</style>
