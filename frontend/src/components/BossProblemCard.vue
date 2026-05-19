<template>
  <article class="boss-card">
    <div>
      <p class="eyebrow">Boss Problem</p>
      <h2>{{ bossProblem?.title || module.boss_problem_title }}</h2>
      <p>
        {{
          bossProblem
            ? "Unlocked placeholder: complete the lessons, then take on the final challenge."
            : "Boss problem content will be added later."
        }}
      </p>
    </div>

    <RouterLink
      v-if="bossProblem"
      class="open-link"
      :to="`/roadmap/${module.id}/boss`"
    >
      Open boss problem
    </RouterLink>
    <span v-else class="locked">Locked placeholder</span>
  </article>
</template>

<script setup>
defineProps({
  module: {
    type: Object,
    required: true,
  },
  bossProblem: {
    type: Object,
    default: null,
  },
});
</script>

<style scoped>
.boss-card {
  display: grid;
  gap: 12px;
  border: 1px solid #f5c97b;
  border-radius: 8px;
  background: #fffaf0;
  padding: 18px;
}

.eyebrow {
  margin: 0 0 6px;
  color: #9a5b00;
  font-size: 13px;
  font-weight: 900;
  text-transform: uppercase;
}

h2 {
  margin: 0 0 8px;
  color: #101828;
  font-size: 21px;
}

p {
  margin: 0;
  color: #526070;
  line-height: 1.5;
}

.open-link,
.locked {
  color: #9a5b00;
  font-weight: 800;
}
</style>
