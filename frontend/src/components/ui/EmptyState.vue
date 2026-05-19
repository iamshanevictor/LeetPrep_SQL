<template>
  <section class="empty-state">
    <div>
      <h2>{{ title }}</h2>
      <p>{{ message }}</p>
    </div>
    <RouterLink v-if="actionLabel && actionTo" class="button button-primary" :to="actionTo">
      {{ actionLabel }}
    </RouterLink>
  </section>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  message: {
    type: String,
    required: true,
  },
  actionLabel: {
    type: String,
    default: "",
  },
  actionTo: {
    type: String,
    default: "",
  },
});
</script>

<style scoped>
h2,
p {
  margin: 0;
}

h2 {
  color: var(--color-text);
  font-size: var(--font-md);
  margin-bottom: var(--space-2);
}

p {
  color: var(--color-muted);
}
</style>
