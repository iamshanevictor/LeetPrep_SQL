<template>
  <div class="table-wrap">
    <table v-if="columns.length">
      <thead>
        <tr>
          <th v-for="column in columns" :key="column">{{ column }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, rowIndex) in rows" :key="rowIndex">
          <td v-for="(column, columnIndex) in columns" :key="column">
            {{ readCell(row, column, columnIndex) }}
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else class="muted">Query results will appear here later.</p>
  </div>
</template>

<script setup>
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

function readCell(row, column, columnIndex) {
  if (Array.isArray(row)) {
    return row[columnIndex] ?? "";
  }

  return row?.[column] ?? "";
}
</script>

<style scoped>
.table-wrap {
  width: 100%;
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

th,
td {
  border-bottom: 1px solid #e4e9f2;
  padding: 10px;
  text-align: left;
  white-space: nowrap;
}

th {
  color: #344054;
  font-weight: 800;
}
</style>
