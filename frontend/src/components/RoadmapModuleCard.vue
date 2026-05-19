<template>
  <article class="module-card">
    <div class="module-header">
      <span class="module-order">Module {{ module.order }}</span>
      <span class="status">{{ status }}</span>
    </div>

    <h2>{{ module.title }}</h2>
    <p class="goal">{{ module.goal }}</p>

    <div class="concepts">
      <ConceptBadge
        v-for="concept in module.concepts || []"
        :key="concept"
        :concept="concept"
      />
    </div>

    <dl>
      <div>
        <dt>Difficulty</dt>
        <dd>{{ module.difficulty }}</dd>
      </div>
      <div>
        <dt>Lessons</dt>
        <dd>{{ module.lessons_count }}</dd>
      </div>
      <div>
        <dt>Boss</dt>
        <dd>{{ module.boss_problem_title }}</dd>
      </div>
    </dl>

    <RouterLink class="open-link" :to="`/roadmap/${module.id}`">
      Open module
    </RouterLink>
  </article>
</template>

<script setup>
import ConceptBadge from "./ConceptBadge.vue";

defineProps({
  module: {
    type: Object,
    required: true,
  },
  status: {
    type: String,
    default: "Not started",
  },
});
</script>

<style scoped>
.module-card {
  display: grid;
  gap: 14px;
  border: 1px solid #d9e1ec;
  border-radius: 8px;
  background: #ffffff;
  padding: 18px;
  box-shadow: 0 12px 28px rgba(16, 24, 40, 0.06);
}

.module-header,
dl,
dl div {
  display: flex;
  align-items: center;
  gap: 10px;
}

.module-header {
  justify-content: space-between;
}

.module-order,
.status {
  color: #526070;
  font-size: 13px;
  font-weight: 800;
}

.status {
  border: 1px solid #e4e9f2;
  border-radius: 999px;
  padding: 5px 8px;
}

h2 {
  margin: 0;
  color: #101828;
  font-size: 22px;
}

.goal {
  margin: 0;
  color: #526070;
  line-height: 1.5;
}

.concepts {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

dl {
  align-items: stretch;
  flex-direction: column;
  margin: 0;
}

dl div {
  justify-content: space-between;
  border-top: 1px solid #eef2f7;
  padding-top: 9px;
}

dt {
  color: #667085;
  font-size: 13px;
  font-weight: 800;
}

dd {
  margin: 0;
  color: #101828;
  font-size: 13px;
  font-weight: 700;
  text-align: right;
}

.open-link {
  color: #1459b8;
  font-weight: 800;
}
</style>
