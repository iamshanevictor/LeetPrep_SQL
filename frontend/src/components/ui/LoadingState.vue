<template>
  <section class="loading-state" role="status" aria-live="polite">
    <strong>{{ message }}</strong>
  </section>
</template>

<script setup>
defineProps({
  message: {
    type: String,
    default: "Loading...",
  },
});
</script>
