<template>
  <article class="card module-card">
    <div class="module-topline">
      <span class="module-number">Module {{ module.order }}</span>
      <span class="badge">{{ status }}</span>
    </div>

    <div class="module-heading">
      <h2>{{ module.title }}</h2>
      <DifficultyBadge :difficulty="module.difficulty" />
    </div>

    <p class="module-goal">{{ module.goal }}</p>

    <div class="concept-list" aria-label="Concepts covered">
      <ConceptBadge
        v-for="concept in module.concepts || []"
        :key="concept"
        :concept="concept"
      />
    </div>

    <div class="module-meta">
      <span>{{ module.lessons_count || 0 }} lessons</span>
      <span>{{ module.boss_problem_title || "Boss problem" }}</span>
    </div>

    <RouterLink class="button button-primary" :to="`/roadmap/${module.id}`">
      Open Module
    </RouterLink>
  </article>
</template>

<script setup>
import ConceptBadge from "../ui/ConceptBadge.vue";
import DifficultyBadge from "../ui/DifficultyBadge.vue";

defineProps({
  module: {
    type: Object,
    required: true,
  },
  status: {
    type: String,
    default: "Not Started",
  },
});
</script>

<style scoped>
.module-card {
  display: grid;
  gap: var(--space-4);
}

.module-topline,
.module-heading,
.module-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-3);
}

.module-number {
  color: var(--color-primary);
  font-size: 13px;
  font-weight: 900;
  text-transform: uppercase;
}

.module-heading {
  align-items: flex-start;
}

h2,
p {
  margin: 0;
}

h2 {
  color: var(--color-text);
  font-size: 22px;
  line-height: 1.25;
}

.module-goal {
  color: var(--color-muted);
  line-height: 1.55;
}

.concept-list {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
}

.module-meta {
  align-items: flex-start;
  border-top: 1px solid var(--color-border);
  color: var(--color-muted);
  font-size: 13px;
  font-weight: 800;
  padding-top: var(--space-3);
}

@media (max-width: 520px) {
  .module-heading,
  .module-meta {
    align-items: flex-start;
    flex-direction: column;
  }
}
</style>
