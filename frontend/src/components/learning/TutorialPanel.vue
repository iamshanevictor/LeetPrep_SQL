<template>
  <section class="card tutorial-panel">
    <div class="card-header">
      <h2 class="card-title">Concept Tutorial</h2>
      <p class="card-description">{{ tutorial.explanation }}</p>
    </div>

    <div class="syntax-block">
      <h3>Syntax Example</h3>
      <pre><code>{{ tutorial.syntax }}</code></pre>
    </div>

    <div class="mental-model">
      <h3>Mental Model</h3>
      <p>{{ tutorial.mental_model }}</p>
    </div>
  </section>
</template>

<script setup>
defineProps({
  tutorial: {
    type: Object,
    required: true,
  },
});
</script>

<style scoped>
.tutorial-panel {
  display: grid;
  gap: var(--space-4);
}

h3,
p {
  margin: 0;
}

h3 {
  color: var(--color-text);
  font-size: 15px;
  margin-bottom: var(--space-2);
}

pre {
  overflow-x: auto;
  border-radius: var(--radius-md);
  background: #111827;
  color: #f8fafc;
  margin: 0;
  padding: var(--space-4);
}

code {
  font-size: 13px;
  line-height: 1.55;
}

.mental-model {
  border-left: 4px solid var(--color-success);
  border-radius: var(--radius-sm);
  background: var(--color-success-soft);
  padding: var(--space-4);
}

.mental-model p {
  color: var(--color-text);
  line-height: 1.55;
}
</style>
