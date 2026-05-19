<template>
  <section class="feedback-panel" :class="statusClass" role="status" aria-live="polite">
    <strong>{{ statusLabel }}</strong>
    <p>{{ message }}</p>
    <pre v-if="error" class="error-detail">{{ error }}</pre>
  </section>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  feedback: {
    type: Object,
    default: null,
  },
  status: {
    type: String,
    default: "neutral",
  },
  message: {
    type: String,
    default: "",
  },
  error: {
    type: String,
    default: "",
  },
});

const currentStatus = computed(() => props.feedback?.status || props.status);
const message = computed(
  () =>
    props.feedback?.message ||
    props.message ||
    "Run a query or submit an answer to see feedback.",
);
const error = computed(() => props.feedback?.error || props.error);

const statusClass = computed(() => `is-${currentStatus.value}`);
const statusLabel = computed(() => {
  const labels = {
    neutral: "Ready",
    success: "Correct",
    incorrect: "Not quite",
    error: "Query error",
    warning: "Check your result",
  };
  return labels[currentStatus.value] || "Feedback";
});
</script>

<style scoped>
.feedback-panel {
  display: grid;
  gap: var(--space-2);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  box-shadow: var(--shadow-card);
  padding: var(--space-4);
}

strong,
p {
  margin: 0;
}

p {
  color: var(--color-muted);
  line-height: 1.5;
}

.is-success {
  border-color: #a7d8b8;
  background: var(--color-success-soft);
}

.is-success strong {
  color: var(--color-success);
}

.is-incorrect,
.is-warning {
  border-color: #f2c078;
  background: var(--color-warning-soft);
}

.is-incorrect strong,
.is-warning strong {
  color: var(--color-warning);
}

.is-error {
  border-color: #f2b8b5;
  background: var(--color-danger-soft);
}

.is-error strong {
  color: var(--color-danger);
}

.error-detail {
  overflow-x: auto;
  border-radius: var(--radius-md);
  background: #3b1111;
  color: #ffe4e4;
  margin: var(--space-2) 0 0;
  padding: var(--space-3);
  white-space: pre-wrap;
}
</style>
