<template>
  <section class="compact-panel">
    <header class="compact-header">
      <h2>Schema</h2>
    </header>

    <ResultTable
      v-if="schemaRows.length"
      :columns="['Table', 'Column', 'Type']"
      :rows="schemaRows"
    />
    <p v-else class="muted compact-empty">Schema details are not available.</p>
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

const sourceTables = computed(() => (props.schema.length ? props.schema : props.tables));

const schemaRows = computed(() =>
  sourceTables.value.flatMap((table) => {
    const tableName = table.table_name || table.name;
    const columns = Array.isArray(table.columns)
      ? table.columns
      : Object.entries(table.columns || {}).map(([name, type]) => ({ name, type }));

    return columns.map((column) => [tableName, column.name, column.type]);
  }),
);
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

h2 {
  margin: 0;
  color: var(--color-text);
  font-size: var(--font-sm);
}

.compact-empty {
  margin: 0;
  font-size: var(--font-sm);
}
</style>
