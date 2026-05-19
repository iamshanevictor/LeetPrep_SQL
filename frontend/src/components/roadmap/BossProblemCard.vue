<template>
  <article class="boss-card">
    <div class="boss-copy">
      <p class="boss-label">Boss Problem</p>
      <h2>{{ bossProblem?.title || module?.boss_problem_title || "Final Challenge" }}</h2>
      <p>
        {{
          bossProblem
            ? "Use the concepts from this module to solve the final target-style problem."
            : "Boss problem content will be added later."
        }}
      </p>
    </div>

    <RouterLink
      v-if="bossProblem"
      class="button button-primary"
      :to="`/roadmap/${moduleId || bossProblem.module_id}/boss`"
    >
      Start Boss Problem
    </RouterLink>
    <span v-else class="badge">Locked Placeholder</span>
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
});
</script>

<style scoped>
.boss-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-5);
  border: 1px solid #f2c078;
  border-radius: var(--radius-lg);
  background: linear-gradient(180deg, #fffaf0, #ffffff);
  box-shadow: var(--shadow-card);
  padding: var(--space-5);
}

.boss-copy {
  display: grid;
  gap: var(--space-2);
}

.boss-label,
h2,
p {
  margin: 0;
}

.boss-label {
  color: var(--color-warning);
  font-size: 13px;
  font-weight: 900;
  text-transform: uppercase;
}

h2 {
  color: var(--color-text);
  font-size: 22px;
}

p {
  color: var(--color-muted);
  line-height: 1.55;
}

@media (max-width: 680px) {
  .boss-card {
    align-items: flex-start;
    flex-direction: column;
  }
}
</style>
