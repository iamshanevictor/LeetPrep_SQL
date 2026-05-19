<template>
  <div class="table-scroll result-table">
    <table v-if="normalizedColumns.length">
      <thead>
        <tr>
          <th v-for="column in normalizedColumns" :key="column">{{ column }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, rowIndex) in normalizedRows" :key="rowIndex">
          <td v-for="(column, columnIndex) in normalizedColumns" :key="column">
            {{ readCell(row, column, columnIndex) }}
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else class="empty-result">{{ emptyMessage }}</p>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  result: {
    type: Object,
    default: null,
  },
  columns: {
    type: Array,
    default: () => [],
  },
  rows: {
    type: Array,
    default: () => [],
  },
  emptyMessage: {
    type: String,
    default: "No rows to display yet.",
  },
});

const normalizedColumns = computed(() => props.result?.columns || props.columns);
const normalizedRows = computed(() => props.result?.rows || props.rows);

function readCell(row, column, columnIndex) {
  if (Array.isArray(row)) {
    return row[columnIndex] ?? "";
  }

  return row?.[column] ?? "";
}
</script>

<style scoped>
.result-table {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
}

table {
  width: 100%;
  border-collapse: collapse;
  background: var(--color-surface);
  font-size: 14px;
}

th,
td {
  border-bottom: 1px solid var(--color-border);
  padding: 10px 12px;
  text-align: left;
  white-space: nowrap;
}

tr:last-child td {
  border-bottom: 0;
}

th {
  background: var(--color-surface-soft);
  color: var(--color-text);
  font-weight: 900;
}

.empty-result {
  margin: 0;
  color: var(--color-muted);
  padding: var(--space-4);
}
</style>
