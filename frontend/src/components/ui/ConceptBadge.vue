<template>
  <span class="badge concept-badge">{{ concept }}</span>
</template>

<script setup>
defineProps({
  concept: {
    type: String,
    required: true,
  },
});
</script>

<style scoped>
.concept-badge {
  border-color: #c8dcff;
  background: var(--color-primary-soft);
  color: var(--color-primary);
}
</style>
