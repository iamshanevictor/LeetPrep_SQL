<template>
  <section class="compact-panel">
    <header class="compact-header">
      <h2>Concept tutorial</h2>
    </header>
    <p>{{ tutorial.explanation }}</p>

    <div class="syntax-block">
      <h3>Syntax</h3>
      <pre><code>{{ formattedSyntax }}</code></pre>
    </div>

    <div class="mental-model">
      <h3>Mental model</h3>
      <p>{{ tutorial.mental_model }}</p>
    </div>
  </section>
</template>

<script setup>
import { computed } from "vue";

import { formatSqlForDisplay } from "../../utils/sqlFormatter";

const props = defineProps({
  tutorial: {
    type: Object,
    required: true,
  },
});

const formattedSyntax = computed(() => formatSqlForDisplay(props.tutorial.syntax));
</script>

<style scoped>
.compact-panel {
  display: grid;
  gap: var(--space-2);
}

.compact-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

h2,
h3,
p {
  margin: 0;
}

h2 {
  color: var(--color-text);
  font-size: var(--font-md);
}

h3 {
  color: var(--color-text);
  font-size: var(--font-sm);
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

.syntax-block,
.mental-model {
  display: grid;
  gap: var(--space-1);
}

.mental-model {
  border-radius: var(--radius-sm);
  background: var(--color-success-soft);
  padding: var(--space-2);
}

.mental-model p {
  color: var(--color-text);
}
</style>
