<template>
  <section class="panel guided-panel">
    <h2 class="section-title">Guided Example</h2>
    <p class="prompt">{{ example.prompt }}</p>
    <pre><code>{{ example.solution_query }}</code></pre>
    <p>{{ example.explanation }}</p>
  </section>
</template>

<script setup>
defineProps({
  example: {
    type: Object,
    required: true,
  },
});
</script>

<style scoped>
.guided-panel {
  display: grid;
  gap: 12px;
}

p {
  margin: 0;
  color: #526070;
  line-height: 1.6;
}

.prompt {
  color: #101828;
  font-weight: 700;
}

pre {
  overflow-x: auto;
  border-radius: 8px;
  background: #111827;
  color: #f9fafb;
  margin: 0;
  padding: 14px;
}
</style>
