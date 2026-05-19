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
    warning: "Check result",
  };
  return labels[currentStatus.value] || "Feedback";
});
</script>

<style scoped>
.feedback-panel {
  display: grid;
  gap: 3px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: var(--color-surface);
  padding: var(--space-2);
}

strong,
p {
  margin: 0;
}

strong {
  font-size: var(--font-sm);
}

p {
  color: var(--color-text-muted);
  font-size: var(--font-sm);
  line-height: 1.35;
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
  border-radius: var(--radius-sm);
  background: #3b1111;
  color: #ffe4e4;
  margin: var(--space-1) 0 0;
  padding: var(--space-2);
  white-space: pre-wrap;
}
</style>
