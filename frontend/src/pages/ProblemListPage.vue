<template>
  <section>
    <header class="page-header">
      <h1 class="page-title">Problems</h1>
      <p class="page-subtitle">
        SQL practice problems will be listed here when you add problem files.
      </p>
    </header>

    <div v-if="isLoading" class="empty-state">Loading problems...</div>
    <div v-else-if="errorMessage" class="empty-state">{{ errorMessage }}</div>
    <div v-else-if="problems.length" class="problem-grid">
      <ProblemCard
        v-for="problem in problems"
        :id="problem.id"
        :key="problem.id"
        :description="problem.description"
        :difficulty="problem.difficulty"
        :title="problem.title"
      />
    </div>
    <div v-else class="empty-state">
      No practice problems yet. Add problem instructions later to start practicing.
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from "vue";

import { fetchProblems } from "../api/problems";
import ProblemCard from "../components/ProblemCard.vue";

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
