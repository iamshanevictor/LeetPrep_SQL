<template>
  <section class="page roadmap-page">
    <PageHeader
      title="SQL Learning Roadmap"
      :subtitle="roadmap?.description || 'Build SQL skills one pattern at a time.'"
    />

    <LoadingState v-if="isLoading" message="Loading roadmap..." />
    <ErrorState v-else-if="errorMessage" title="Could not load roadmap" :message="errorMessage" />
    <div v-else-if="modules.length" class="roadmap-layout">
      <aside class="card side-list">
        <h2>Modules</h2>
        <RouterLink
          v-for="module in modules"
          :key="module.id"
          class="side-link"
          :to="`/roadmap/${module.id}`"
          @mouseenter="prefetchModule(module.id)"
          @focus="prefetchModule(module.id)"
        >
          <span>{{ String(module.order).padStart(2, "0") }}</span>
          <strong>{{ module.title }}</strong>
        </RouterLink>
      </aside>

      <main class="roadmap-list">
        <RoadmapModuleCard
          v-for="module in modules"
          :key="module.id"
          :module="module"
          :status="getRoadmapModuleStatus(module, progress)"
          @mouseenter="prefetchModule(module.id)"
          @focus="prefetchModule(module.id)"
        />
      </main>

      <aside class="card summary-panel">
        <h2>Summary</h2>
        <dl>
          <div>
            <dt>Modules</dt>
            <dd>{{ modules.length }}</dd>
          </div>
          <div>
            <dt>Lessons ready</dt>
            <dd>{{ lessonCount }}</dd>
          </div>
          <div>
            <dt>Status</dt>
            <dd>{{ progressSummary.completedModules }} complete</dd>
          </div>
        </dl>
        <p>
          Progress is saved in this browser with no account required.
        </p>
      </aside>
    </div>
    <EmptyState
      v-else
      title="Roadmap modules have not been added yet."
      message="Add module metadata in the backend roadmap JSON to start building the path."
    />
  </section>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from "vue";

import { fetchRoadmap } from "../api/roadmap";
import { prefetchModule } from "../api/roadmap";
import PageHeader from "../components/layout/PageHeader.vue";
import RoadmapModuleCard from "../components/roadmap/RoadmapModuleCard.vue";
import EmptyState from "../components/ui/EmptyState.vue";
import ErrorState from "../components/ui/ErrorState.vue";
import LoadingState from "../components/ui/LoadingState.vue";
import {
  getProgressSummary,
  getRoadmapModuleStatus,
  loadProgress,
  subscribeProgress,
} from "../services/progressStorage";

const roadmap = ref(null);
const isLoading = ref(true);
const errorMessage = ref("");
const progress = ref(loadProgress());
let unsubscribeProgress = null;

const modules = computed(() => roadmap.value?.modules || []);
const lessonCount = computed(() =>
  modules.value.reduce((total, module) => total + (module.lessons_count || 0), 0),
);
const progressSummary = computed(() => getProgressSummary(modules.value, progress.value));

onMounted(async () => {
  unsubscribeProgress = subscribeProgress((nextProgress) => {
    progress.value = nextProgress;
  });

  try {
    roadmap.value = await fetchRoadmap();
    modules.value.forEach((module) => prefetchModule(module.id));
  } catch (error) {
    errorMessage.value = error.message;
  } finally {
    isLoading.value = false;
  }
});

onUnmounted(() => {
  unsubscribeProgress?.();
});
</script>

<style scoped>
.roadmap-layout {
  display: grid;
  grid-template-columns: 220px minmax(0, 1fr) 230px;
  gap: var(--space-2);
  align-items: start;
}

.side-list,
.summary-panel {
  position: sticky;
  top: 57px;
  display: grid;
  gap: var(--space-2);
}

.side-list h2,
.summary-panel h2 {
  margin: 0;
  font-size: var(--font-md);
}

.side-link {
  display: grid;
  grid-template-columns: 28px minmax(0, 1fr);
  gap: var(--space-1);
  align-items: center;
  color: var(--color-text-muted);
  font-size: var(--font-xs);
}

.side-link strong {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.side-link.router-link-active {
  color: var(--color-primary);
}

.roadmap-list {
  display: grid;
  gap: var(--space-2);
}

dl {
  display: grid;
  gap: var(--space-1);
  margin: 0;
}

dl div {
  display: flex;
  justify-content: space-between;
  gap: var(--space-2);
  border-top: 1px solid var(--color-border);
  padding-top: var(--space-1);
}

dt,
dd,
.summary-panel p {
  margin: 0;
  color: var(--color-text-muted);
  font-size: var(--font-xs);
}

dd {
  color: var(--color-text);
  font-weight: 800;
}

@media (max-width: 1080px) {
  .roadmap-layout {
    grid-template-columns: 1fr;
  }

  .side-list,
  .summary-panel {
    position: static;
  }
}
</style>
