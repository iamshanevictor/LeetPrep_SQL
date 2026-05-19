<template>
  <header class="page-header">
    <p v-if="eyebrow" class="page-eyebrow">{{ eyebrow }}</p>
    <h1 class="page-title">{{ title }}</h1>
    <p v-if="subtitle" class="page-subtitle">{{ subtitle }}</p>
  </header>
</template>

<script setup>
defineProps({
  eyebrow: {
    type: String,
    default: "",
  },
  title: {
    type: String,
    required: true,
  },
  subtitle: {
    type: String,
    default: "",
  },
});
</script>
