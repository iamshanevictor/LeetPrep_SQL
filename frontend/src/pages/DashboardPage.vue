<template>
  <section class="page">
    <PageHeader
      eyebrow="Learning dashboard"
      title="Welcome to LeetPrep-SQL"
      subtitle="Practice SQL patterns step by step before jumping into LeetCode-style problems."
    />

    <div class="grid grid-3">
      <StatCard label="Problems Available" :value="problemCount" helper="Standalone problem set" />
      <StatCard label="Lessons Available" :value="lessonCount" helper="Roadmap lessons ready now" />
      <StatCard label="Current Streak" value="0 days" helper="Progress tracking is planned" />
    </div>

    <section class="dashboard-grid">
      <article class="card continue-card">
        <div class="card-header">
          <h2 class="card-title">Continue Learning</h2>
          <p class="card-description">
            Start with Module 1 to learn aggregation, joins, CASE WHEN, and CTEs
            before solving the salary comparison boss problem.
          </p>
        </div>
        <RouterLink class="button button-primary" to="/roadmap/module_01_salary_comparison">
          Continue Module 1
        </RouterLink>
      </article>

      <article class="card action-card">
        <div class="card-header">
          <h2 class="card-title">Choose Your Path</h2>
          <p class="card-description">
            Use the roadmap for guided learning. Browse problems when standalone
            practice sets are added later.
          </p>
        </div>
        <div class="actions">
          <RouterLink class="button button-primary" to="/roadmap">
            Start Roadmap
          </RouterLink>
          <RouterLink class="button button-secondary" to="/problems">
            Browse Problems
          </RouterLink>
        </div>
      </article>
    </section>

    <ErrorState v-if="errorMessage" title="Dashboard data is partial" :message="errorMessage" />
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";

import { fetchProblems } from "../api/problems";
import { fetchRoadmap } from "../api/roadmap";
import PageHeader from "../components/layout/PageHeader.vue";
import ErrorState from "../components/ui/ErrorState.vue";
import StatCard from "../components/ui/StatCard.vue";

const roadmap = ref(null);
const problems = ref([]);
const errorMessage = ref("");

const lessonCount = computed(() =>
  (roadmap.value?.modules || []).reduce(
    (total, module) => total + (module.lessons_count || 0),
    0,
  ),
);
const problemCount = computed(() => problems.value.length);

onMounted(async () => {
  try {
    const [roadmapData, problemData] = await Promise.all([
      fetchRoadmap(),
      fetchProblems(),
    ]);
    roadmap.value = roadmapData;
    problems.value = problemData.problems || [];
  } catch (error) {
    errorMessage.value = error.message;
  }
});
</script>

<style scoped>
.dashboard-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.2fr) minmax(280px, 0.8fr);
  gap: var(--space-4);
}

.continue-card,
.action-card {
  display: grid;
  align-content: space-between;
  gap: var(--space-4);
}

@media (max-width: 820px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
}
</style>
