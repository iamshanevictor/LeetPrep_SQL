<template>
  <article class="card stat-card">
    <p class="stat-label">{{ label }}</p>
    <p class="stat-value">{{ value }}</p>
    <p v-if="helper" class="stat-helper">{{ helper }}</p>
  </article>
</template>

<script setup>
defineProps({
  label: {
    type: String,
    required: true,
  },
  value: {
    type: [String, Number],
    required: true,
  },
  helper: {
    type: String,
    default: "",
  },
});
</script>

<style scoped>
.stat-card {
  display: grid;
  gap: var(--space-1);
}

.stat-label,
.stat-value,
.stat-helper {
  margin: 0;
}

.stat-label {
  color: var(--color-muted);
  font-size: var(--font-xs);
  font-weight: 800;
  text-transform: uppercase;
}

.stat-value {
  color: var(--color-text);
  font-size: 20px;
  font-weight: 850;
  letter-spacing: 0;
}

.stat-helper {
  color: var(--color-muted);
  font-size: var(--font-xs);
  line-height: 1.45;
}
</style>
