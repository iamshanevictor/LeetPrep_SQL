<template>
  <section class="statement-panel">
    <div class="statement-header">
      <p class="eyebrow">{{ label }}</p>
      <h2>{{ title }}</h2>
    </div>

    <p class="prompt">{{ prompt }}</p>
    <p v-if="!orderMatters" class="result-note">
      Return the result table in any order.
    </p>

    <div class="schema-section">
      <article v-for="table in normalizedTables" :key="table.name" class="statement-block">
        <h3>Table: <code>{{ table.name }}</code></h3>
        <ResultTable
          :columns="['Column Name', 'Type']"
          :rows="table.columns.map((column) => [column.name, column.type])"
        />
      </article>
    </div>

    <div class="example-section">
      <h3>Example 1:</h3>

      <div class="example-block">
        <h4>Input:</h4>
        <article v-for="table in inputTables" :key="table.name" class="input-table">
          <p>{{ table.name }} table:</p>
          <ResultTable :columns="table.columns" :rows="table.rows" />
        </article>
      </div>

      <div class="example-block">
        <h4>Output:</h4>
        <ResultTable
          v-if="expectedResult?.columns?.length"
          :columns="expectedResult.columns"
          :rows="expectedResult.rows"
        />
        <p v-else class="muted">Expected output is not available yet.</p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed } from "vue";

import ResultTable from "./ResultTable.vue";

const props = defineProps({
  label: {
    type: String,
    default: "Practice Problem",
  },
  title: {
    type: String,
    required: true,
  },
  prompt: {
    type: String,
    required: true,
  },
  schema: {
    type: Array,
    default: () => [],
  },
  seedData: {
    type: Object,
    default: () => ({}),
  },
  expectedResult: {
    type: Object,
    default: null,
  },
  orderMatters: {
    type: Boolean,
    default: false,
  },
});

const normalizedTables = computed(() =>
  props.schema.map((table) => ({
    name: table.table_name || table.name,
    columns: Object.entries(table.columns || {}).map(([name, type]) => ({
      name,
      type,
    })),
  })),
);

const inputTables = computed(() =>
  normalizedTables.value
    .map((table) => ({
      name: table.name,
      columns: table.columns.map((column) => column.name),
      rows: props.seedData[table.name] || [],
    }))
    .filter((table) => table.rows.length),
);
</script>

<style scoped>
.statement-panel {
  display: grid;
  gap: 18px;
  border: 1px solid #d9e1ec;
  border-radius: 8px;
  background: #ffffff;
  padding: 22px;
  box-shadow: 0 12px 28px rgba(16, 24, 40, 0.06);
}

.statement-header {
  display: grid;
  gap: 6px;
}

.eyebrow {
  margin: 0;
  color: #1459b8;
  font-size: 13px;
  font-weight: 900;
  text-transform: uppercase;
}

h2,
h3,
h4,
p {
  margin: 0;
}

h2 {
  color: #101828;
  font-size: 22px;
  line-height: 1.25;
}

h3 {
  color: #101828;
  font-size: 16px;
}

h4 {
  color: #344054;
  font-size: 14px;
}

code {
  color: #1459b8;
  font-family: "Cascadia Code", "Fira Code", Consolas, monospace;
}

.prompt,
.result-note,
.input-table p {
  color: #526070;
  line-height: 1.6;
}

.prompt {
  color: #101828;
  font-weight: 700;
}

.schema-section,
.example-section,
.example-block {
  display: grid;
  gap: 12px;
}

.statement-block,
.input-table {
  display: grid;
  gap: 8px;
}

.example-section {
  border-top: 1px solid #eef2f7;
  padding-top: 18px;
}
</style>
