<template>
  <article class="lc-description">
    <div class="tabs" aria-label="Problem sections">
      <span class="tab active">Description</span>
      <span v-if="tutorial" class="tab">Tutorial</span>
      <span v-if="hints.length" class="tab">Hints</span>
    </div>

    <div class="description-body">
      <header class="problem-header">
        <p class="problem-label">{{ label }}</p>
        <h1>{{ title }}</h1>
        <div class="concept-row">
          <span v-for="concept in concepts" :key="concept" class="concept-pill">
            {{ concept }}
          </span>
        </div>
      </header>

      <section v-if="tutorial" class="explain-box">
        <h2>Why this works</h2>
        <p>{{ tutorial.explanation }}</p>
        <div class="mental-model">
          <strong>Mental model:</strong>
          <span>{{ tutorial.mental_model }}</span>
        </div>
      </section>

      <section class="schema-section">
        <p class="schema-links">SQL Schema <span>›</span></p>
        <div v-for="table in normalizedTables" :key="table.name" class="lc-block">
          <p class="table-title">Table: <code>{{ table.name }}</code></p>
          <ResultTable
            :columns="['Column Name', 'Type']"
            :rows="table.columns.map((column) => [column.name, column.type])"
          />
        </div>
      </section>

      <section v-if="prerequisites.length" class="lc-block">
        <h2>Prerequisites</h2>
        <ul class="text-list">
          <li v-for="item in prerequisites" :key="item">{{ item }}</li>
        </ul>
      </section>

      <section class="prompt-section">
        <p>{{ prompt }}</p>
        <p v-if="!orderMatters">Return the result table in <strong>any order</strong>.</p>
        <p>The result format is in the following example.</p>
      </section>

      <section class="example-section">
        <h2>Example 1:</h2>

        <div class="example-block">
          <h3>Input:</h3>
          <div v-for="table in inputTables" :key="table.name" class="input-table">
            <p>{{ table.name }} table:</p>
            <ResultTable :columns="table.columns" :rows="table.rows" />
          </div>
        </div>

        <div class="example-block">
          <h3>Output:</h3>
          <ResultTable
            :result="expectedResult"
            empty-message="Expected output is not available yet."
          />
        </div>
      </section>

      <section v-if="guidedExample" class="lc-block">
        <h2>Guided Example</h2>
        <p>{{ guidedExample.prompt }}</p>
        <pre><code>{{ guidedExample.solution_query }}</code></pre>
        <p>{{ guidedExample.explanation }}</p>
      </section>

      <section v-if="tutorial" class="lc-block">
        <h2>Syntax Pattern</h2>
        <pre><code>{{ tutorial.syntax }}</code></pre>
      </section>

      <section v-if="hints.length" class="lc-block">
        <button class="hint-toggle" type="button" @click="showHints = !showHints">
          {{ showHints ? "Hide Hints" : "Show Hints" }}
        </button>
        <ol v-if="showHints" class="text-list">
          <li v-for="hint in hints" :key="hint">{{ hint }}</li>
        </ol>
      </section>

      <section v-if="commonMistakes.length" class="lc-block">
        <h2>Common Mistakes</h2>
        <ul class="text-list">
          <li v-for="mistake in commonMistakes" :key="mistake">{{ mistake }}</li>
        </ul>
      </section>
    </div>
  </article>
</template>

<script setup>
import { computed, ref } from "vue";

import ResultTable from "./ResultTable.vue";

const props = defineProps({
  label: {
    type: String,
    default: "Problem",
  },
  title: {
    type: String,
    required: true,
  },
  concepts: {
    type: Array,
    default: () => [],
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
  tutorial: {
    type: Object,
    default: null,
  },
  guidedExample: {
    type: Object,
    default: null,
  },
  hints: {
    type: Array,
    default: () => [],
  },
  prerequisites: {
    type: Array,
    default: () => [],
  },
  commonMistakes: {
    type: Array,
    default: () => [],
  },
});

const showHints = ref(false);

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
.lc-description {
  display: grid;
  grid-template-rows: auto minmax(0, 1fr);
  height: 100%;
  min-height: 0;
  overflow: hidden;
  border-radius: 8px;
  background: #242424;
  color: #f2f2f2;
}

.tabs {
  display: flex;
  align-items: center;
  gap: 18px;
  min-height: 38px;
  border-bottom: 1px solid #3a3a3a;
  background: #303030;
  padding: 0 16px;
}

.tab {
  color: #b7b7b7;
  font-size: 13px;
  font-weight: 700;
}

.tab.active {
  color: #ffffff;
}

.description-body {
  display: grid;
  align-content: start;
  gap: 28px;
  min-height: 0;
  overflow-y: auto;
  padding: 18px 22px 72px;
}

.problem-header {
  display: grid;
  gap: 10px;
}

.problem-label,
h1,
h2,
h3,
p {
  margin: 0;
}

.problem-label {
  color: #8c8c8c;
  font-size: 13px;
  font-weight: 800;
}

h1 {
  color: #ffffff;
  font-size: 22px;
  line-height: 1.25;
}

h2 {
  color: #ffffff;
  font-size: 15px;
}

h3 {
  color: #ffffff;
  font-size: 14px;
}

p,
li {
  color: #d6d6d6;
  line-height: 1.55;
}

strong {
  color: #ffffff;
}

code,
pre {
  font-family: "Cascadia Code", "Fira Code", Consolas, monospace;
}

pre {
  overflow-x: auto;
  border-radius: 6px;
  background: #171717;
  color: #f0f0f0;
  margin: 10px 0 0;
  padding: 12px;
}

.concept-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.concept-pill {
  border-radius: 999px;
  background: #333333;
  color: #bdbdbd;
  font-size: 12px;
  font-weight: 800;
  padding: 5px 8px;
}

.schema-links {
  color: #2f8cff;
  font-weight: 700;
}

.schema-links span {
  color: #8ebeff;
}

.schema-section,
.example-section,
.example-block,
.lc-block,
.prompt-section,
.explain-box,
.input-table {
  display: grid;
  gap: 12px;
}

.table-title {
  color: #ffffff;
  font-weight: 800;
}

.table-title code {
  border: 1px solid #4a4a4a;
  border-radius: 5px;
  background: #333333;
  color: #ffffff;
  padding: 2px 5px;
}

.prompt-section p {
  color: #ffffff;
  font-weight: 700;
}

.explain-box {
  border-left: 3px solid #2f8cff;
  background: #202d3f;
  padding: 12px;
}

.mental-model {
  display: grid;
  gap: 4px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding-top: 10px;
}

.text-list {
  display: grid;
  gap: 8px;
  margin: 0;
  padding-left: 20px;
}

.hint-toggle {
  justify-self: start;
  border: 1px solid #4a4a4a;
  border-radius: 6px;
  background: #333333;
  color: #ffffff;
  cursor: pointer;
  font-weight: 800;
  padding: 8px 12px;
}

:deep(.result-table) {
  border-color: #4a4a4a;
  background: #242424;
}

:deep(table) {
  background: #242424;
  color: #d6d6d6;
}

:deep(th) {
  background: #2f2f2f;
  color: #ffffff;
}

:deep(th),
:deep(td) {
  border-color: #4a4a4a;
}

:deep(.empty-result) {
  color: #bdbdbd;
}
</style>
