<template>
  <span class="badge" :class="badgeClass">{{ difficulty || "Not set" }}</span>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  difficulty: {
    type: String,
    default: "",
  },
});

const badgeClass = computed(() => {
  const value = props.difficulty.toLowerCase();
  if (value.includes("beginner") || value.includes("easy")) {
    return "badge-easy";
  }
  if (value.includes("advanced") || value.includes("hard")) {
    return "badge-hard";
  }
  return "badge-medium";
});
</script>
