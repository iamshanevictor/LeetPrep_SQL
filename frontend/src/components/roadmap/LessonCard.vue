<template>
  <component
    :is="locked ? 'div' : RouterLink"
    class="lesson-row"
    :class="{ 'is-locked': locked }"
    v-bind="linkAttrs"
  >
    <span class="lesson-index">{{ index + 1 }}</span>
    <div class="lesson-main">
      <div class="lesson-title-line">
        <h3>{{ lesson.title }}</h3>
        <span class="badge">{{ lesson.estimated_minutes || 10 }} min</span>
        <span class="badge" :class="{ 'badge-easy': status === 'Completed' }">
          {{ locked ? "Locked" : status }}
        </span>
      </div>
      <p>{{ lesson.learning_objective }}</p>
      <div class="concept-list">
        <ConceptBadge
          v-for="concept in lesson.concepts || []"
          :key="concept"
          :concept="concept"
        />
      </div>
    </div>
    <span class="button button-secondary">{{ locked ? "Locked" : "Start" }}</span>
  </component>
</template>

<script setup>
import { computed } from "vue";
import { RouterLink } from "vue-router";

import ConceptBadge from "../ui/ConceptBadge.vue";

const props = defineProps({
  lesson: {
    type: Object,
    required: true,
  },
  index: {
    type: Number,
    default: 0,
  },
  status: {
    type: String,
    default: "Not Started",
  },
  locked: {
    type: Boolean,
    default: false,
  },
});

const linkAttrs = computed(() => {
  if (props.locked) {
    return {
      role: "listitem",
      "aria-disabled": "true",
    };
  }

  return {
    to: `/roadmap/${props.lesson.module_id}/lessons/${props.lesson.id}`,
  };
});
</script>

<style scoped>
.lesson-row {
  display: grid;
  grid-template-columns: 26px minmax(0, 1fr) auto;
  gap: var(--space-2);
  align-items: center;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  padding: var(--space-2);
}

.lesson-row:hover {
  border-color: var(--color-primary);
  background: var(--color-surface-muted);
}

.lesson-row.is-locked {
  cursor: not-allowed;
  opacity: 0.72;
}

.lesson-row.is-locked .lesson-index {
  background: var(--color-surface-muted);
  color: var(--color-text-muted);
}

.lesson-index {
  display: grid;
  place-items: center;
  width: 24px;
  height: 24px;
  border-radius: 999px;
  background: var(--color-primary-soft);
  color: var(--color-primary);
  font-size: var(--font-xs);
  font-weight: 850;
}

.lesson-main {
  display: grid;
  gap: 4px;
  min-width: 0;
}

.lesson-title-line,
.concept-list {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: var(--space-1);
}

h3,
p {
  margin: 0;
}

h3 {
  color: var(--color-text);
  font-size: var(--font-sm);
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

@media (max-width: 680px) {
  .lesson-row {
    grid-template-columns: 26px minmax(0, 1fr);
  }

  .lesson-row .button {
    grid-column: 2;
    justify-self: start;
  }
}
</style>
