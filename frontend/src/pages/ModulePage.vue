<template>
  <section class="page">
    <RouterLink class="back-link" to="/roadmap">Back to Roadmap</RouterLink>

    <PageHeader
      eyebrow="Roadmap module"
      :title="moduleData?.title || 'Module'"
      :subtitle="moduleData?.goal || ''"
    />

    <LoadingState v-if="isLoading" message="Loading module..." />
    <ErrorState v-else-if="errorMessage" title="Could not load module" :message="errorMessage" />
    <div v-else class="stack-lg">
      <section class="card module-summary">
        <div class="summary-copy">
          <DifficultyBadge :difficulty="moduleData.difficulty" />
          <div class="concept-list">
            <ConceptBadge
              v-for="concept in moduleData.concepts || []"
              :key="concept"
              :concept="concept"
            />
          </div>
        </div>
        <span class="badge">Not Started</span>
      </section>

      <section class="stack">
        <h2 class="section-title">Lessons</h2>
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
          message="This module is already planned in the roadmap, but its tutorial content has not been written yet."
        />
      </section>

      <BossProblemCard
        :module="moduleData"
        :module-id="moduleData.id"
        :boss-problem="moduleData.boss_problem"
      />
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";

import { fetchModule } from "../api/roadmap";
import PageHeader from "../components/layout/PageHeader.vue";
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
</script>

<style scoped>
.module-summary {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-4);
}

.summary-copy {
  display: grid;
  gap: var(--space-3);
}

.concept-list {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
}

.lesson-list {
  display: grid;
  gap: var(--space-3);
}

@media (max-width: 680px) {
  .module-summary {
    flex-direction: column;
  }
}
</style>
