<template>
  <section class="card schema-viewer">
    <div class="card-header">
      <h2 class="card-title">Schema</h2>
      <p class="card-description">Reference the available tables and column types.</p>
    </div>

    <div v-if="normalizedTables.length" class="schema-list">
      <article v-for="table in normalizedTables" :key="table.name" class="schema-table">
        <h3>{{ table.name }}</h3>
        <ResultTable
          :columns="['Column', 'Type']"
          :rows="table.columns.map((column) => [column.name, column.type])"
        />
      </article>
    </div>
    <p v-else class="muted">Schema details are not available yet.</p>
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
  tables: {
    type: Array,
    default: () => [],
  },
});

const normalizedTables = computed(() =>
  (props.schema.length ? props.schema : props.tables).map((table) => ({
    name: table.name || table.table_name,
    columns: Array.isArray(table.columns)
      ? table.columns
      : Object.entries(table.columns || {}).map(([name, type]) => ({ name, type })),
  })),
);
</script>

<style scoped>
.schema-list {
  display: grid;
  gap: var(--space-4);
}

.schema-table {
  display: grid;
  gap: var(--space-2);
}

h3 {
  margin: 0;
  color: var(--color-text);
  font-size: 15px;
}
</style>
