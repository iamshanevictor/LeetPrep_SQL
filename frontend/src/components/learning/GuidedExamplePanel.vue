<template>
  <section class="compact-panel">
    <header class="compact-header">
      <h2>Guided example</h2>
    </header>
    <p>{{ guidedExample.prompt }}</p>
    <pre><code>{{ formattedSolution }}</code></pre>
    <p>{{ guidedExample.explanation }}</p>
  </section>
</template>

<script setup>
import { computed } from "vue";

import { formatSqlForDisplay } from "../../utils/sqlFormatter";

const props = defineProps({
  guidedExample: {
    type: Object,
    required: true,
  },
});

const formattedSolution = computed(() =>
  formatSqlForDisplay(props.guidedExample.solution_query),
);
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
  overflow-x: hidden;
  border: 1px solid var(--color-code-border);
  border-radius: var(--radius-sm);
  background: var(--color-code-bg);
  color: var(--color-code-text);
  margin: 0;
  padding: var(--space-2);
  white-space: pre-wrap;
  word-break: break-word;
}

code {
  font-size: var(--font-xs);
  line-height: 1.45;
}
</style>
