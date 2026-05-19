<template>
  <section class="feedback" :class="statusClass" role="status">
    <strong>{{ statusLabel }}</strong>
    <p>{{ message || "Feedback will appear here after running or submitting SQL." }}</p>
  </section>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  status: {
    type: String,
    default: "idle",
  },
  message: {
    type: String,
    default: "",
  },
});

const statusClass = computed(() => `status-${props.status}`);

const statusLabel = computed(() => {
  const labels = {
    idle: "Ready",
    success: "Success",
    error: "Needs attention",
  };

  return labels[props.status] || "Status";
});
</script>

<style scoped>
.feedback {
  border: 1px solid #d9e1ec;
  border-radius: 8px;
  background: #ffffff;
  padding: 16px;
}

.feedback strong {
  display: block;
  margin-bottom: 6px;
}

.feedback p {
  margin: 0;
  color: #526070;
  line-height: 1.5;
}

.status-success {
  border-color: #98d9b6;
  background: #f0fff6;
}

.status-error {
  border-color: #f3a8a8;
  background: #fff5f5;
}
</style>
