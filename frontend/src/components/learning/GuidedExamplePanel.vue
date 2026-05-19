<template>
  <section class="compact-panel">
    <header class="compact-header">
      <h2>Guided example</h2>
    </header>
    <p>{{ guidedExample.prompt }}</p>
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
.compact-panel {
  display: grid;
  gap: var(--space-2);
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
  line-height: 1.45;
}

pre {
  overflow-x: auto;
  border-radius: var(--radius-sm);
  background: #101827;
  color: #f8fafc;
  margin: 0;
  padding: var(--space-2);
}

code {
  font-size: var(--font-xs);
  line-height: 1.45;
}
</style>
