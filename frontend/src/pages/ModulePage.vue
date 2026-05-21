<template>
  <section class="page module-page">
    <RouterLink class="back-link" to="/roadmap">Back to Roadmap</RouterLink>

    <LoadingState v-if="isLoading" message="Loading module..." />
    <ErrorState v-else-if="errorMessage" title="Could not load module" :message="errorMessage" />
    <div v-else class="module-layout">
      <main class="module-main">
        <header class="module-header card">
          <div>
            <p class="page-eyebrow">Roadmap module</p>
            <h1>{{ moduleData.title }}</h1>
            <p>{{ moduleData.goal }}</p>
          </div>
          <div class="header-meta">
            <DifficultyBadge :difficulty="moduleData.difficulty" />
            <span class="badge">Not Started</span>
          </div>
        </header>

        <section class="card concept-panel">
          <h2>Concepts</h2>
          <div class="concept-list">
            <ConceptBadge
              v-for="concept in moduleData.concepts || []"
              :key="concept"
              :concept="concept"
            />
          </div>
        </section>

        <section class="lesson-section">
          <div class="section-row">
            <h2>Lessons</h2>
            <span class="badge">{{ moduleData.lessons.length }} ready</span>
          </div>
          <div v-if="moduleData.lessons.length" class="lesson-list">
            <LessonCard
              v-for="(lesson, index) in moduleData.lessons"
              :key="lesson.id"
              :lesson="lesson"
              :index="index"
            />
          </div>
          <EmptyState
            v-else
            title="Lessons for this module will be added later."
            message="This module is planned, but its tutorial content has not been written yet."
          />
        </section>
      </main>

      <aside class="module-side">
        <section class="card">
          <h2>Module summary</h2>
          <dl>
            <div>
              <dt>Lessons</dt>
              <dd>{{ moduleData.lessons.length }}</dd>
            </div>
            <div>
              <dt>Difficulty</dt>
              <dd>{{ moduleData.difficulty }}</dd>
            </div>
            <div>
              <dt>Progress</dt>
              <dd>0%</dd>
            </div>
          </dl>
        </section>

        <section v-if="buildsOnModules.length" class="card builds-on-panel">
          <h2>Builds on</h2>
          <ul>
            <li v-for="moduleName in buildsOnModules" :key="moduleName">
              {{ moduleName }}
            </li>
          </ul>
        </section>

        <BossProblemCard
          :module="moduleData"
          :module-id="moduleData.id"
          :boss-problem="moduleData.boss_problem"
        />
      </aside>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { useRoute } from "vue-router";

import { fetchModule } from "../api/roadmap";
import BossProblemCard from "../components/roadmap/BossProblemCard.vue";
import LessonCard from "../components/roadmap/LessonCard.vue";
import ConceptBadge from "../components/ui/ConceptBadge.vue";
import DifficultyBadge from "../components/ui/DifficultyBadge.vue";
import EmptyState from "../components/ui/EmptyState.vue";
import ErrorState from "../components/ui/ErrorState.vue";
import LoadingState from "../components/ui/LoadingState.vue";

const route = useRoute();
const moduleData = ref(null);
const isLoading = ref(true);
const errorMessage = ref("");

const buildsOnModules = computed(() =>
  (moduleData.value?.builds_on_modules || []).map((moduleId) => formatModuleName(moduleId)),
);

onMounted(async () => {
  try {
    const data = await fetchModule(route.params.moduleId);
    moduleData.value = data.module;
  } catch (error) {
    errorMessage.value = error.message;
  } finally {
    isLoading.value = false;
  }
});

function formatModuleName(moduleId) {
  return moduleId
    .replace(/^module_/, "")
    .replace(/_/g, " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}
</script>

<style scoped>
.module-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 310px;
  gap: var(--space-2);
  align-items: start;
}

.module-main,
.module-side,
.lesson-list {
  display: grid;
  gap: var(--space-2);
}

.module-side {
  position: sticky;
  top: 57px;
}

.module-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-3);
}

.module-header h1,
.module-header p,
.concept-panel h2,
.section-row h2,
.module-side h2,
.builds-on-panel ul {
  margin: 0;
}

.module-header h1 {
  color: var(--color-text);
  font-size: var(--font-lg);
  line-height: 1.2;
}

.module-header p:not(.page-eyebrow) {
  color: var(--color-text-muted);
  font-size: var(--font-sm);
  line-height: 1.4;
}

.header-meta,
.concept-list,
.section-row {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: var(--space-1);
}

.header-meta {
  justify-content: flex-end;
}

.concept-panel {
  display: grid;
  gap: var(--space-2);
}

.section-row {
  justify-content: space-between;
}

.section-row h2,
.concept-panel h2,
.module-side h2 {
  font-size: var(--font-md);
}

.builds-on-panel {
  display: grid;
  gap: var(--space-2);
}

.builds-on-panel ul {
  display: grid;
  gap: var(--space-1);
  padding: 0;
  list-style: none;
}

.builds-on-panel li {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: var(--color-surface-muted);
  color: var(--color-text-muted);
  font-size: var(--font-xs);
  font-weight: 700;
  padding: 5px 7px;
}

dl {
  display: grid;
  gap: var(--space-1);
  margin: var(--space-2) 0 0;
}

dl div {
  display: flex;
  justify-content: space-between;
  gap: var(--space-2);
  border-top: 1px solid var(--color-border);
  padding-top: var(--space-1);
}

dt,
dd {
  margin: 0;
  font-size: var(--font-xs);
}

dt {
  color: var(--color-text-muted);
}

dd {
  color: var(--color-text);
  font-weight: 800;
  text-align: right;
}

@media (max-width: 920px) {
  .module-layout {
    grid-template-columns: 1fr;
  }

  .module-side {
    position: static;
  }
}
</style>
