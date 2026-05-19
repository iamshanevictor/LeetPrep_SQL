<template>
  <section class="panel">
    <h2 class="section-title">Sample Data</h2>
    <ResultTable v-if="columns.length && rows.length" :columns="columns" :rows="rows" />
    <p v-else class="muted">Sample rows will appear here later.</p>
  </section>
</template>

<script setup>
import ResultTable from "./ResultTable.vue";

defineProps({
  columns: {
    type: Array,
    default: () => [],
  },
  rows: {
    type: Array,
    default: () => [],
  },
});
</script>
