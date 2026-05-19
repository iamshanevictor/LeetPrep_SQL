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
    default: "No rows yet.",
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
  max-height: 220px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: var(--color-surface);
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--font-xs);
}

th,
td {
  border-bottom: 1px solid var(--color-border);
  padding: 6px 8px;
  text-align: left;
  white-space: nowrap;
}

th {
  position: sticky;
  top: 0;
  z-index: 1;
  background: var(--color-surface-muted);
  color: var(--color-text);
  font-weight: 800;
}

tr:last-child td {
  border-bottom: 0;
}

.empty-result {
  margin: 0;
  color: var(--color-text-muted);
  font-size: var(--font-sm);
  padding: var(--space-3);
}
</style>
