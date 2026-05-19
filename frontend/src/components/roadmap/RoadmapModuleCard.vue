<template>
  <RouterLink class="module-row" :to="`/roadmap/${module.id}`">
    <span class="module-number">{{ String(module.order).padStart(2, "0") }}</span>

    <div class="module-main">
      <div class="module-title-line">
        <h2>{{ module.title }}</h2>
        <DifficultyBadge :difficulty="module.difficulty" />
        <span class="badge">{{ status }}</span>
      </div>
      <p>{{ module.goal }}</p>
      <div class="concept-list">
        <ConceptBadge
          v-for="concept in visibleConcepts"
          :key="concept"
          :concept="concept"
        />
        <span v-if="hiddenConceptCount" class="badge">+{{ hiddenConceptCount }}</span>
      </div>
    </div>

    <div class="module-meta">
      <span>{{ module.lessons_count || 0 }} lessons</span>
      <span>Boss</span>
    </div>
  </RouterLink>
</template>

<script setup>
import { computed } from "vue";

import ConceptBadge from "../ui/ConceptBadge.vue";
import DifficultyBadge from "../ui/DifficultyBadge.vue";

const props = defineProps({
  module: {
    type: Object,
    required: true,
  },
  status: {
    type: String,
    default: "Not Started",
  },
});

const visibleConcepts = computed(() => (props.module.concepts || []).slice(0, 4));
const hiddenConceptCount = computed(() =>
  Math.max((props.module.concepts || []).length - visibleConcepts.value.length, 0),
);
</script>

<style scoped>
.module-row {
  display: grid;
  grid-template-columns: 42px minmax(0, 1fr) 96px;
  gap: var(--space-3);
  align-items: center;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  padding: var(--space-2) var(--space-3);
}

.module-row:hover {
  border-color: var(--color-primary);
  background: var(--color-surface-muted);
}

.module-number {
  color: var(--color-primary);
  font-family: "Cascadia Code", Consolas, monospace;
  font-size: var(--font-sm);
  font-weight: 850;
}

.module-main {
  display: grid;
  gap: 5px;
  min-width: 0;
}

.module-title-line,
.concept-list,
.module-meta {
  display: flex;
  align-items: center;
  gap: var(--space-1);
}

.module-title-line {
  flex-wrap: wrap;
}

h2,
p {
  margin: 0;
}

h2 {
  color: var(--color-text);
  font-size: var(--font-md);
  line-height: 1.25;
}

p {
  overflow: hidden;
  color: var(--color-text-muted);
  font-size: var(--font-xs);
  line-height: 1.35;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.concept-list {
  flex-wrap: wrap;
}

.module-meta {
  align-items: flex-end;
  flex-direction: column;
  color: var(--color-text-muted);
  font-size: var(--font-xs);
  font-weight: 750;
}

@media (max-width: 720px) {
  .module-row {
    grid-template-columns: 32px minmax(0, 1fr);
  }

  .module-meta {
    align-items: flex-start;
    grid-column: 2;
  }
}
</style>
