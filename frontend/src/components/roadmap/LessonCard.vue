<template>
  <article class="card lesson-card">
    <div class="lesson-index">{{ index + 1 }}</div>
    <div class="lesson-body">
      <div class="lesson-heading">
        <div>
          <h2>{{ lesson.title }}</h2>
          <p>{{ lesson.learning_objective }}</p>
        </div>
        <span class="badge">Not Started</span>
      </div>

      <div class="concept-list">
        <ConceptBadge
          v-for="concept in lesson.concepts || []"
          :key="concept"
          :concept="concept"
        />
      </div>

      <div class="lesson-footer">
        <span>{{ lesson.estimated_minutes || 10 }} min</span>
        <RouterLink
          class="button button-secondary"
          :to="`/roadmap/${lesson.module_id}/lessons/${lesson.id}`"
        >
          Start Lesson
        </RouterLink>
      </div>
    </div>
  </article>
</template>

<script setup>
import ConceptBadge from "../ui/ConceptBadge.vue";

defineProps({
  lesson: {
    type: Object,
    required: true,
  },
  index: {
    type: Number,
    default: 0,
  },
});
</script>

<style scoped>
.lesson-card {
  display: grid;
  grid-template-columns: 42px minmax(0, 1fr);
  gap: var(--space-4);
}

.lesson-index {
  display: grid;
  place-items: center;
  width: 42px;
  height: 42px;
  border-radius: 999px;
  background: var(--color-primary-soft);
  color: var(--color-primary);
  font-weight: 900;
}

.lesson-body,
.lesson-heading {
  display: grid;
  gap: var(--space-3);
}

.lesson-heading {
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: start;
}

h2,
p {
  margin: 0;
}

h2 {
  color: var(--color-text);
  font-size: 19px;
}

p {
  color: var(--color-muted);
  line-height: 1.5;
}

.concept-list,
.lesson-footer {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: var(--space-2);
}

.lesson-footer {
  justify-content: space-between;
  color: var(--color-muted);
  font-size: 13px;
  font-weight: 850;
}

@media (max-width: 620px) {
  .lesson-card,
  .lesson-heading {
    grid-template-columns: 1fr;
  }
}
</style>
