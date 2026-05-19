<template>
  <article class="lesson-card">
    <div>
      <p class="eyebrow">Lesson {{ lesson.order }}</p>
      <h2>{{ lesson.title }}</h2>
      <p>{{ lesson.learning_objective }}</p>
    </div>

    <div class="concepts">
      <ConceptBadge
        v-for="concept in lesson.concepts || []"
        :key="concept"
        :concept="concept"
      />
    </div>

    <RouterLink
      class="open-link"
      :to="`/roadmap/${lesson.module_id}/lessons/${lesson.id}`"
    >
      Start lesson
    </RouterLink>
  </article>
</template>

<script setup>
import ConceptBadge from "./ConceptBadge.vue";

defineProps({
  lesson: {
    type: Object,
    required: true,
  },
});
</script>

<style scoped>
.lesson-card {
  display: grid;
  gap: 12px;
  border: 1px solid #d9e1ec;
  border-radius: 8px;
  background: #ffffff;
  padding: 16px;
}

.eyebrow {
  margin: 0 0 6px;
  color: #667085;
  font-size: 13px;
  font-weight: 800;
  text-transform: uppercase;
}

h2 {
  margin: 0 0 8px;
  color: #101828;
  font-size: 20px;
}

p {
  margin: 0;
  color: #526070;
  line-height: 1.5;
}

.concepts {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.open-link {
  color: #1459b8;
  font-weight: 800;
}
</style>
