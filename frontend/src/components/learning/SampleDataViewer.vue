<template>
  <section class="card sample-viewer">
    <div class="card-header">
      <h2 class="card-title">Sample Data</h2>
      <p class="card-description">These rows are loaded into DuckDB for this exercise.</p>
    </div>

    <div v-if="tables.length" class="sample-list">
      <article v-for="table in tables" :key="table.name" class="sample-table">
        <h3>{{ table.name }} table</h3>
        <ResultTable :columns="table.columns" :rows="table.rows" />
      </article>
    </div>
    <p v-else class="muted">Sample rows are not available yet.</p>
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
});

const tables = computed(() =>
  props.schema
    .map((table) => {
      const name = table.table_name || table.name;
      return {
        name,
        columns: Object.keys(table.columns || {}),
        rows: props.seedData[name] || [],
      };
    })
    .filter((table) => table.rows.length),
);
</script>

<style scoped>
.sample-list,
.sample-table {
  display: grid;
  gap: var(--space-4);
}

.sample-table {
  gap: var(--space-2);
}

h3 {
  margin: 0;
  color: var(--color-text);
  font-size: 15px;
}
</style>
