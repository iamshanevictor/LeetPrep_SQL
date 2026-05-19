<template>
  <section>
    <header class="page-header">
      <h1 class="page-title">LeetPrep-SQL</h1>
      <p class="page-subtitle">Practice SQL patterns before diving into LeetCode.</p>
    </header>

    <div class="stats-grid">
      <article v-for="stat in stats" :key="stat.label" class="stat-card">
        <p class="stat-label">{{ stat.label }}</p>
        <p class="stat-value">{{ stat.value }}</p>
      </article>
    </div>
  </section>
</template>

<script setup>
const stats = [
  { label: "Problems Available", value: "0" },
  { label: "Solved Problems", value: "0" },
  { label: "Current Streak", value: "0 days" },
];
</script>
