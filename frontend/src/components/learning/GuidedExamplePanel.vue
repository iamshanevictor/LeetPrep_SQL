<template>
  <section class="card guided-panel">
    <div class="card-header">
      <h2 class="card-title">Guided Example</h2>
      <p class="card-description">{{ guidedExample.prompt }}</p>
    </div>

    <pre><code>{{ guidedExample.solution_query }}</code></pre>
    <p>{{ guidedExample.explanation }}</p>
  </section>
</template>

<script setup>
defineProps({
  guidedExample: {
    type: Object,
    required: true,
  },
});
</script>

<style scoped>
.guided-panel {
  display: grid;
  gap: var(--space-4);
}

pre {
  overflow-x: auto;
  border-radius: var(--radius-md);
  background: #111827;
  color: #f8fafc;
  margin: 0;
  padding: var(--space-4);
}

p {
  margin: 0;
  color: var(--color-muted);
  line-height: 1.55;
}
</style>
