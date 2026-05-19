<template>
  <span class="concept-badge">{{ concept }}</span>
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
  display: inline-flex;
  align-items: center;
  border: 1px solid #c8dcff;
  border-radius: 999px;
  background: #edf5ff;
  color: #1459b8;
  font-size: 12px;
  font-weight: 800;
  line-height: 1;
  padding: 6px 9px;
}
</style>
