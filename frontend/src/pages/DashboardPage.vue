<template>
  <section class="page dashboard-page">
    <PageHeader
      title="LeetPrep-SQL"
      subtitle="A focused SQL practice workspace for preparing for LeetCode-style database problems."
    />

    <div class="dashboard-overview">
      <section class="about-panel">
        <p class="eyebrow-line">About the app</p>
        <h2>Practice the SQL thinking patterns behind interview problems.</h2>
        <p>
          LeetPrep-SQL is built for learners who already understand SQL syntax and
          want a structured path toward harder LeetCode database questions. The
          lessons focus on pattern recognition, query organization, joins,
          aggregations, window functions, CTEs, and result-checking discipline.
        </p>
        <p>
          This is not a beginner-first SQL course yet. You should already be
          comfortable writing basic <code>SELECT</code>, <code>WHERE</code>,
          <code>JOIN</code>, and <code>GROUP BY</code> queries before attempting
          the modules here.
        </p>
        <div class="notice-row">
          <strong>In development:</strong>
          <span>
            beginner-friendly zero-to-hero modules for SQL syntax, fundamentals,
            and guided basics are planned for a future version.
          </span>
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

      <aside class="progress-panel" aria-label="Local progress summary">
        <div class="progress-heading">
          <div>
            <p class="eyebrow-line">Your status</p>
            <h2>Local progress</h2>
          </div>
          <span class="badge">browser only</span>
        </div>
        <p class="progress-note">{{ continueDescription }}</p>
        <div class="stat-strip compact">
          <StatCard label="Lessons" :value="lessonProgressLabel" helper="completed" />
          <StatCard label="Modules" :value="moduleProgressLabel" helper="completed" />
          <StatCard label="Streak" :value="`${progressSummary.currentStreak}d`" helper="current" />
          <StatCard label="Problems" :value="problemCount" helper="available" />
        </div>
      </aside>
    </div>

    <div class="dashboard-layout">
      <section class="module-panel">
        <div class="card-header">
          <h2 class="card-title">What you will practice</h2>
          <p class="card-description">
            Modules are ordered to build toward advanced SQL problem patterns.
          </p>
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

      <section class="learning-notes">
        <h2>How to use this workspace</h2>
        <ul>
          <li>Read the pattern explanation before writing the query.</li>
          <li>Use Run Query to inspect your output before submitting.</li>
          <li>Finish lessons in order to unlock later practice and boss problems.</li>
          <li>Treat boss problems as LeetCode preparation, not copy-paste answers.</li>
        </ul>
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
.dashboard-overview {
  display: grid;
  grid-template-columns: minmax(0, 1.35fr) minmax(300px, 0.65fr);
  gap: var(--space-3);
  align-items: start;
}

.about-panel {
  display: grid;
  gap: var(--space-2);
}

.about-panel h2,
.progress-heading h2,
.learning-notes h2 {
  margin: 0;
  color: var(--color-text);
  font-size: 18px;
  line-height: 1.25;
}

.about-panel p,
.progress-note,
.learning-notes li {
  margin: 0;
  color: var(--color-text-muted);
  font-size: var(--font-sm);
  line-height: 1.55;
}

.eyebrow-line {
  margin: 0;
  color: var(--color-primary);
  font-size: var(--font-xs);
  font-weight: 850;
  text-transform: uppercase;
}

.notice-row {
  display: flex;
  gap: var(--space-2);
  align-items: flex-start;
  border-left: 3px solid var(--color-warning);
  background: var(--color-warning-soft);
  color: var(--color-text);
  font-size: var(--font-sm);
  line-height: 1.45;
  padding: var(--space-2) var(--space-3);
}

.notice-row strong {
  flex: 0 0 auto;
  color: var(--color-warning);
}

.about-panel code {
  color: var(--color-text);
  font-size: var(--font-xs);
  font-weight: 750;
}

.progress-panel {
  display: grid;
  gap: var(--space-2);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  padding: var(--space-3);
}

.progress-heading {
  display: flex;
  justify-content: space-between;
  gap: var(--space-2);
  align-items: flex-start;
}

.stat-strip {
  display: grid;
  gap: var(--space-2);
}

.stat-strip.compact {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.dashboard-layout {
  display: grid;
  grid-template-columns: minmax(0, 1.1fr) minmax(300px, 0.7fr);
  gap: var(--space-3);
  align-items: start;
}

.module-panel {
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

.learning-notes {
  display: grid;
  gap: var(--space-2);
  border-top: 1px solid var(--color-border);
  padding-top: var(--space-3);
}

.learning-notes ul {
  display: grid;
  gap: var(--space-2);
  margin: 0;
  padding-left: 18px;
}

@media (max-width: 820px) {
  .dashboard-overview,
  .dashboard-layout {
    grid-template-columns: 1fr;
  }

  .notice-row {
    display: grid;
  }
}
</style>
