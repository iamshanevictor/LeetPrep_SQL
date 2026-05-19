<template>
  <section class="panel">
    <h2 class="section-title">Sample Data</h2>
    <div v-if="tables.length" class="sample-tables">
      <article v-for="table in tables" :key="table.name" class="sample-table">
        <h3>{{ table.name }}</h3>
        <ResultTable :columns="table.columns" :rows="table.rows" />
      </article>
    </div>
    <ResultTable v-else-if="columns.length && rows.length" :columns="columns" :rows="rows" />
    <p v-else class="muted">Sample rows will appear here later.</p>
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
  columns: {
    type: Array,
    default: () => [],
  },
  rows: {
    type: Array,
    default: () => [],
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
.sample-tables {
  display: grid;
  gap: 16px;
}

.sample-table {
  display: grid;
  gap: 8px;
}

h3 {
  margin: 0;
  color: #344054;
  font-size: 15px;
}
</style>
