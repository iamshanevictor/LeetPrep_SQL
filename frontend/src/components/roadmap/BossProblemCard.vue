<template>
  <article class="boss-row" :class="{ 'is-locked': locked }">
    <div class="boss-main">
      <span class="badge badge-medium">Boss Problem</span>
      <h2>{{ bossProblem?.title || module?.boss_problem_title || "Final Challenge" }}</h2>
      <p>
        {{
          bossProblem
            ? locked
              ? "Complete every lesson in this module to reveal the final challenge."
              : "Final target-style challenge for this module."
            : "Boss problem content will be added later."
        }}
      </p>
    </div>

    <span
      v-if="bossProblem && status === 'Completed'"
      class="badge badge-easy"
    >
      Completed
    </span>
    <RouterLink
      v-if="bossProblem"
      class="button button-primary"
      :to="`/roadmap/${moduleId || bossProblem.module_id}/boss`"
    >
      {{ locked ? "Locked" : status === "Completed" ? "Review Boss" : "Start Boss" }}
    </RouterLink>
    <span v-else class="badge">Locked</span>
  </article>
</template>

<script setup>
defineProps({
  bossProblem: {
    type: Object,
    default: null,
  },
  module: {
    type: Object,
    default: null,
  },
  moduleId: {
    type: String,
    default: "",
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
</script>

<style scoped>
.boss-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-3);
  border: 1px solid #f1bf76;
  border-radius: var(--radius-md);
  background: var(--color-warning-soft);
  padding: var(--space-3);
}

.boss-main {
  display: grid;
  gap: 4px;
}

.boss-row.is-locked {
  opacity: 0.78;
}

h2,
p {
  margin: 0;
}

h2 {
  color: var(--color-text);
  font-size: var(--font-md);
}

p {
  color: var(--color-text-muted);
  font-size: var(--font-sm);
}

@media (max-width: 680px) {
  .boss-row {
    align-items: flex-start;
    flex-direction: column;
  }
}
</style>
