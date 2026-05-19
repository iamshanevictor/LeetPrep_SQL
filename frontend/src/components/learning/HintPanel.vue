<template>
  <section class="card hint-panel">
    <button class="button button-secondary" type="button" @click="isOpen = !isOpen">
      {{ isOpen ? "Hide Hints" : "Show Hints" }}
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
.hint-panel {
  display: grid;
  justify-items: start;
  gap: var(--space-4);
}

.hint-list {
  display: grid;
  gap: var(--space-2);
  margin: 0;
  padding-left: 22px;
  color: var(--color-muted);
  line-height: 1.55;
}
</style>
