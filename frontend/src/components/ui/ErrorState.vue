<template>
  <section class="error-state" role="alert">
    <div>
      <h2>{{ title }}</h2>
      <p>{{ message }}</p>
    </div>
  </section>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    default: "Something went wrong",
  },
  message: {
    type: String,
    required: true,
  },
});
</script>

<style scoped>
h2,
p {
  margin: 0;
}

h2 {
  font-size: 18px;
  margin-bottom: var(--space-2);
}
</style>
