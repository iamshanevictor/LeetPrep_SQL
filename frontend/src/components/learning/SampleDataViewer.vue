<template>
  <section class="compact-panel">
    <header class="compact-header">
      <h2>Sample data</h2>
      <span v-if="tables.length" class="badge">{{ tables.length }} tables</span>
    </header>

    <div v-if="tables.length" class="sample-list">
      <article v-for="table in tables" :key="table.name" class="sample-table">
        <h3>{{ table.name }}</h3>
        <ResultTable :columns="table.columns" :rows="table.rows" />
      </article>
    </div>
    <p v-else class="muted compact-empty">Sample rows are not available.</p>
  </section>
</template>

<script setup>
import { computed } from "vue";

import ResultTable from "./ResultTable.vue";

const props = defineProps({
  schema: {
    type: Array,
    default: () => [],
  },
  seedData: {
    type: Object,
    default: () => ({}),
  },
  maxRows: {
    type: Number,
    default: 6,
  },
});

const tables = computed(() =>
  props.schema
    .map((table) => {
      const name = table.table_name || table.name;
      return {
        name,
        columns: Object.keys(table.columns || {}),
        rows: (props.seedData[name] || []).slice(0, props.maxRows),
      };
    })
    .filter((table) => table.rows.length),
);
</script>

<style scoped>
.compact-panel,
.sample-list,
.sample-table {
  display: grid;
  gap: var(--space-2);
}

.compact-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-2);
}

h2,
h3 {
  margin: 0;
  color: var(--color-text);
  font-size: var(--font-sm);
}

h3 {
  color: var(--color-text-muted);
  font-size: var(--font-xs);
  text-transform: uppercase;
}

.compact-empty {
  margin: 0;
  font-size: var(--font-sm);
}
</style>
