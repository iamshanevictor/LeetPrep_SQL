<template>
  <section class="page dashboard-page">
    <PageHeader
      title="LeetPrep-SQL"
      subtitle="Compact SQL learning paths, practice workspaces, and problem-solving drills."
    />

    <div class="stat-strip">
      <StatCard label="Problems" :value="problemCount" helper="available" />
      <StatCard label="Lessons" :value="lessonProgressLabel" helper="completed / authored" />
      <StatCard label="Streak" :value="`${progressSummary.currentStreak}d`" helper="local browser" />
      <StatCard label="Modules" :value="moduleProgressLabel" helper="completed / available" />
    </div>

    <div class="dashboard-layout">
      <section class="card continue-panel">
        <div class="card-header">
          <h2 class="card-title">Continue learning</h2>
          <p class="card-description">{{ continueDescription }}</p>
        </div>
        <div class="actions">
          <RouterLink class="button button-primary" :to="continueTo">
            {{ continueLabel }}
          </RouterLink>
          <RouterLink class="button button-secondary" to="/roadmap">
            Roadmap
          </RouterLink>
          <RouterLink class="button button-secondary" to="/problems">
            Problems
          </RouterLink>
        </div>
      </section>

      <section class="card module-panel">
        <div class="card-header">
          <h2 class="card-title">Available modules</h2>
        </div>
        <div v-if="modules.length" class="module-list">
          <RouterLink
            v-for="module in modules"
            :key="module.id"
            class="module-link"
            :to="`/roadmap/${module.id}`"
          >
            <span>{{ String(module.order).padStart(2, "0") }}</span>
            <strong>{{ module.title }}</strong>
            <small>{{ module.lessons_count || 0 }} lessons</small>
          </RouterLink>
        </div>
        <p v-else class="muted compact-note">Roadmap modules are not loaded yet.</p>
      </section>

      <ErrorState v-if="errorMessage" title="Dashboard data is partial" :message="errorMessage" />
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from "vue";

import { fetchProblems } from "../api/problems";
import { fetchRoadmap } from "../api/roadmap";
import PageHeader from "../components/layout/PageHeader.vue";
import ErrorState from "../components/ui/ErrorState.vue";
import StatCard from "../components/ui/StatCard.vue";
import {
  getProgressSummary,
  loadProgress,
  subscribeProgress,
} from "../services/progressStorage";

const roadmap = ref(null);
const problems = ref([]);
const errorMessage = ref("");
const progress = ref(loadProgress());
let unsubscribeProgress = null;

const modules = computed(() => roadmap.value?.modules || []);
const moduleCount = computed(() => modules.value.length);
const lessonCount = computed(() =>
  modules.value.reduce((total, module) => total + (module.lessons_count || 0), 0),
);
const problemCount = computed(() => problems.value.length);
const progressSummary = computed(() => getProgressSummary(modules.value, progress.value));
const lessonProgressLabel = computed(
  () => `${progressSummary.value.completedLessons}/${lessonCount.value}`,
);
const moduleProgressLabel = computed(
  () => `${progressSummary.value.completedModules}/${moduleCount.value}`,
);
const continueTo = computed(() => {
  const lastVisited = progressSummary.value.lastVisited;
  if (lastVisited?.path) {
    return lastVisited.path;
  }

  return "/roadmap/module_01_salary_comparison";
});
const continueLabel = computed(() =>
  progressSummary.value.lastVisited ? "Continue Learning" : "Start Module 1",
);
const continueDescription = computed(() => {
  const lastVisited = progressSummary.value.lastVisited;
  if (lastVisited?.title) {
    return `Last opened: ${lastVisited.title}`;
  }

  return "Start with Module 1: aggregation, joins, CASE WHEN, and CTEs.";
});

onMounted(async () => {
  unsubscribeProgress = subscribeProgress((nextProgress) => {
    progress.value = nextProgress;
  });

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

onUnmounted(() => {
  unsubscribeProgress?.();
});
</script>

<style scoped>
.stat-strip {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: var(--space-2);
}

.dashboard-layout {
  display: grid;
  grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.1fr);
  gap: var(--space-2);
}

.continue-panel {
  align-content: start;
  display: grid;
  gap: var(--space-2);
}

.module-list {
  display: grid;
}

.module-link {
  display: grid;
  grid-template-columns: 32px minmax(0, 1fr) auto;
  gap: var(--space-2);
  align-items: center;
  border-top: 1px solid var(--color-border);
  padding: 7px 0;
}

.module-link:first-child {
  border-top: 0;
}

.module-link span {
  color: var(--color-primary);
  font-family: "Cascadia Code", Consolas, monospace;
  font-size: var(--font-xs);
  font-weight: 850;
}

.module-link strong {
  overflow: hidden;
  color: var(--color-text);
  font-size: var(--font-sm);
  text-overflow: ellipsis;
  white-space: nowrap;
}

.module-link small,
.compact-note {
  color: var(--color-text-muted);
  font-size: var(--font-xs);
}

@media (max-width: 820px) {
  .stat-strip,
  .dashboard-layout {
    grid-template-columns: 1fr;
  }
}
</style>
