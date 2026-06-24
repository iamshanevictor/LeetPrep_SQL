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
        <div class="about-points" aria-label="App positioning">
          <div>
            <strong>Built for</strong>
            <span>Intermediate SQL practice and LeetCode preparation.</span>
          </div>
          <div>
            <strong>Focus</strong>
            <span>Joins, grouping, CTEs, windows, ranking, and query patterns.</span>
          </div>
          <div>
            <strong>Not yet</strong>
            <span>A beginner syntax course, though beginner modules are planned.</span>
          </div>
        </div>
        <div class="notice-row">
          <strong>In development:</strong>
          <span>
            beginner-friendly zero-to-hero modules for SQL syntax, fundamentals,
            and guided basics are planned for a future version.
          </span>
        </div>
        <div class="actions">
          <RouterLink class="button button-primary" :to="continueTo" :aria-label="continueAriaLabel">
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

      <div class="dashboard-side">
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

        <section class="learning-notes">
          <p class="eyebrow-line">Workflow</p>
          <h2>How to use this workspace</h2>
          <ol>
            <li>
              <strong>Study the pattern</strong>
              <span>Read the explanation before writing SQL.</span>
            </li>
            <li>
              <strong>Run before submit</strong>
              <span>Inspect your output, then submit when it matches the prompt.</span>
            </li>
            <li>
              <strong>Finish in order</strong>
              <span>Complete lessons to unlock later practice and boss problems.</span>
            </li>
          </ol>
        </section>
      </div>
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
  return getContinuePath(progressSummary.value.lastVisited);
});
const continueLabel = computed(() =>
  progressSummary.value.lastVisited ? "Continue Learning" : "Start Module 1",
);
const continueAriaLabel = computed(() =>
  progressSummary.value.lastVisited
    ? `Continue learning: ${progressSummary.value.lastVisited.title || "last opened lesson"}`
    : "Start Module 1 Lesson 1",
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

function getContinuePath(lastVisited) {
  if (lastVisited?.type === "lesson" && lastVisited.moduleId && lastVisited.lessonId) {
    return `/roadmap/${lastVisited.moduleId}/lessons/${lastVisited.lessonId}`;
  }

  if (lastVisited?.type === "boss" && lastVisited.moduleId) {
    return `/roadmap/${lastVisited.moduleId}/boss`;
  }

  if (isValidLearningPath(lastVisited?.path)) {
    return lastVisited.path;
  }

  return "/roadmap/module_01_salary_comparison/lessons/lesson_01_group_by_avg";
}

function isValidLearningPath(path) {
  return typeof path === "string" && /^\/roadmap\/[^/]+(\/lessons\/[^/]+|\/boss)?$/.test(path);
}
</script>

<style scoped>
.dashboard-overview {
  display: grid;
  grid-template-columns: minmax(0, 1.55fr) minmax(320px, 0.7fr);
  gap: var(--space-4);
  align-items: stretch;
}

.about-panel {
  display: grid;
  align-content: start;
  gap: var(--space-3);
  max-width: 920px;
  padding: var(--space-1) 0;
}

.about-panel h2,
.progress-heading h2,
.learning-notes h2 {
  margin: 0;
  color: var(--color-text);
  font-size: 18px;
  line-height: 1.25;
}

.about-panel h2 {
  max-width: 780px;
  font-size: 26px;
  letter-spacing: 0;
}

.about-panel p,
.progress-note,
.learning-notes span {
  margin: 0;
  color: var(--color-text-muted);
  font-size: var(--font-sm);
  line-height: 1.55;
}

.about-panel > p {
  max-width: 860px;
  font-size: 14px;
}

.eyebrow-line {
  margin: 0;
  color: var(--color-primary);
  font-size: var(--font-xs);
  font-weight: 850;
  text-transform: uppercase;
}

.about-points {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--space-2);
}

.about-points div {
  display: grid;
  gap: var(--space-1);
  border-top: 1px solid var(--color-border);
  padding-top: var(--space-2);
}

.about-points strong,
.learning-notes strong {
  color: var(--color-text);
  font-size: var(--font-sm);
}

.about-points span {
  color: var(--color-text-muted);
  font-size: var(--font-xs);
  line-height: 1.45;
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

.dashboard-side {
  display: grid;
  gap: var(--space-3);
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
  gap: var(--space-3);
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
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  padding: var(--space-3);
}

.learning-notes ol {
  display: grid;
  gap: var(--space-2);
  margin: 0;
  padding: 0;
  list-style: none;
  counter-reset: workflow-step;
}

.learning-notes li {
  position: relative;
  display: grid;
  gap: 2px;
  padding-left: 28px;
  counter-increment: workflow-step;
}

.learning-notes li::before {
  position: absolute;
  top: 1px;
  left: 0;
  display: inline-grid;
  place-items: center;
  width: 18px;
  height: 18px;
  border: 1px solid var(--color-border-strong);
  border-radius: 999px;
  color: var(--color-primary);
  content: counter(workflow-step);
  font-size: 11px;
  font-weight: 850;
}

@media (max-width: 820px) {
  .dashboard-overview,
  .dashboard-layout {
    grid-template-columns: 1fr;
  }

  .notice-row {
    display: grid;
  }

  .about-panel h2 {
    font-size: 22px;
  }

  .about-points {
    grid-template-columns: 1fr;
  }
}
</style>
