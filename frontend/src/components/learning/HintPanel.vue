<template>
  <section class="compact-panel">
    <button class="hint-toggle" type="button" @click="isOpen = !isOpen">
      {{ isOpen ? "Hide hints" : `Show hints (${hints.length})` }}
    </button>

    <ol v-if="isOpen" class="hint-list">
      <li v-for="hint in hints" :key="hint">{{ hint }}</li>
    </ol>
  </section>
</template>

<script setup>
import { ref } from "vue";

defineProps({
  hints: {
    type: Array,
    default: () => [],
  },
});

const isOpen = ref(false);
</script>

<style scoped>
.compact-panel {
  display: grid;
  justify-items: start;
  gap: var(--space-2);
}

.hint-toggle {
  border: 1px solid var(--color-border-strong);
  border-radius: var(--radius-sm);
  background: var(--color-surface);
  color: var(--color-primary);
  cursor: pointer;
  font-size: var(--font-sm);
  font-weight: 750;
  padding: 6px 9px;
}

.hint-list {
  display: grid;
  gap: var(--space-1);
  margin: 0;
  padding-left: 20px;
  color: var(--color-text-muted);
  font-size: var(--font-sm);
  line-height: 1.4;
}
</style>
