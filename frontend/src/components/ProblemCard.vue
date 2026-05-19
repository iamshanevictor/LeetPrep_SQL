<template>
  <article class="problem-card">
    <div>
      <p class="difficulty">{{ difficulty || "Uncategorized" }}</p>
      <h2>{{ title || "Untitled problem" }}</h2>
    </div>
    <p class="description">
      {{ description || "Problem instructions will be added later." }}
    </p>
    <RouterLink v-if="id" class="card-link" :to="`/problems/${id}`">
      Open problem
    </RouterLink>
  </article>
</template>

<script setup>
defineProps({
  id: {
    type: String,
    default: "",
  },
  title: {
    type: String,
    default: "",
  },
  difficulty: {
    type: String,
    default: "",
  },
  description: {
    type: String,
    default: "",
  },
});
</script>

<style scoped>
.problem-card {
  display: grid;
  gap: 12px;
  border: 1px solid #d9e1ec;
  border-radius: 8px;
  background: #ffffff;
  padding: 18px;
}

.difficulty {
  margin: 0 0 6px;
  color: #667085;
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
}

h2 {
  margin: 0;
  color: #101828;
  font-size: 20px;
  line-height: 1.3;
}

.description {
  margin: 0;
  color: #526070;
  line-height: 1.5;
}

.card-link {
  color: #1459b8;
  font-weight: 700;
}
</style>
