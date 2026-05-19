<template>
  <section>
    <header class="page-header">
      <RouterLink class="back-link" to="/roadmap">Back to roadmap</RouterLink>
      <h1 class="page-title">{{ module?.title || "Module" }}</h1>
      <p class="page-subtitle">{{ module?.goal }}</p>
    </header>

    <div v-if="isLoading" class="empty-state">Loading module...</div>
    <div v-else-if="errorMessage" class="empty-state">{{ errorMessage }}</div>
    <div v-else>
      <section class="panel progress-panel">
        <div>
          <h2 class="section-title">Progress</h2>
          <p class="muted">Progress tracking will be added later.</p>
        </div>
        <span class="progress-status">Not started</span>
      </section>

      <div v-if="module.lessons.length" class="lesson-grid">
        <LessonCard
          v-for="lesson in module.lessons"
          :key="lesson.id"
          :lesson="lesson"
        />
      </div>

      <div v-else class="empty-state">
        Lessons for this module will be added later.
      </div>

      <BossProblemCard
        class="boss-section"
        :module="module"
        :boss-problem="module.boss_problem"
      />
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";

import { fetchModule } from "../api/roadmap";
import BossProblemCard from "../components/BossProblemCard.vue";
import LessonCard from "../components/LessonCard.vue";

const route = useRoute();
const module = ref(null);
const isLoading = ref(true);
const errorMessage = ref("");

onMounted(async () => {
  try {
    const data = await fetchModule(route.params.moduleId);
    module.value = data.module;
  } catch (error) {
    errorMessage.value = error.message;
  } finally {
    isLoading.value = false;
  }
});
</script>

<style scoped>
.back-link {
  color: #1459b8;
  font-weight: 800;
}

.progress-panel {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 16px;
}

.progress-status {
  border: 1px solid #d9e1ec;
  border-radius: 999px;
  color: #526070;
  font-size: 13px;
  font-weight: 800;
  padding: 6px 10px;
}

.lesson-grid {
  display: grid;
  gap: 14px;
}

.boss-section {
  margin-top: 16px;
}
</style>
