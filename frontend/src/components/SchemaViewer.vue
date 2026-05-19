<template>
  <section class="panel">
    <h2 class="section-title">Schema</h2>
    <div v-if="tables.length" class="schema-list">
      <article v-for="table in tables" :key="table.name" class="schema-table">
        <h3>{{ table.name }}</h3>
        <ul>
          <li v-for="column in table.columns" :key="column.name">
            <span>{{ column.name }}</span>
            <code>{{ column.type }}</code>
          </li>
        </ul>
      </article>
    </div>
    <p v-else class="muted">Schema details will appear here later.</p>
  </section>
</template>

<script setup>
defineProps({
  tables: {
    type: Array,
    default: () => [],
  },
});
</script>

<style scoped>
.schema-list {
  display: grid;
  gap: 12px;
}

.schema-table {
  border: 1px solid #e4e9f2;
  border-radius: 8px;
  padding: 12px;
}

h3 {
  margin: 0 0 8px;
  font-size: 16px;
}

ul {
  display: grid;
  gap: 6px;
  list-style: none;
  margin: 0;
  padding: 0;
}

li {
  display: flex;
  justify-content: space-between;
  gap: 12px;
}

code {
  color: #1459b8;
}
</style>
