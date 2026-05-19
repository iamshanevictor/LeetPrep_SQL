<template>
  <section class="panel">
    <button class="hint-toggle" type="button" @click="isOpen = !isOpen">
      {{ isOpen ? "Hide hints" : "Show hints" }}
    </button>
    <ol v-if="isOpen" class="hints">
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
.hint-toggle {
  border: 1px solid #cfd8e6;
  border-radius: 8px;
  background: #ffffff;
  color: #1459b8;
  cursor: pointer;
  font-weight: 800;
  padding: 9px 12px;
}

.hints {
  display: grid;
  gap: 8px;
  margin: 14px 0 0;
  padding-left: 22px;
  color: #526070;
  line-height: 1.5;
}
</style>
