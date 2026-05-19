<template>
  <label class="sql-editor">
    <span>{{ label }}</span>
    <textarea
      :value="modelValue"
      :placeholder="placeholder"
      :disabled="disabled"
      rows="12"
      aria-label="SQL query editor"
      @input="$emit('update:modelValue', $event.target.value)"
    />
  </label>
</template>

<script setup>
defineProps({
  modelValue: {
    type: String,
    default: "",
  },
  label: {
    type: String,
    default: "Write your SQL",
  },
  placeholder: {
    type: String,
    default: "SELECT ...\nFROM ...;",
  },
  disabled: {
    type: Boolean,
    default: false,
  },
});

defineEmits(["update:modelValue"]);
</script>

<style scoped>
.sql-editor {
  display: grid;
  gap: var(--space-2);
  color: var(--color-text);
  font-weight: 900;
}

textarea {
  width: 100%;
  min-height: 260px;
  resize: vertical;
  border: 1px solid #253044;
  border-radius: var(--radius-md);
  background: #111827;
  color: #f8fafc;
  font-family: "Cascadia Code", "Fira Code", Consolas, monospace;
  font-size: 14px;
  line-height: 1.55;
  padding: 14px;
}

textarea:disabled {
  opacity: 0.7;
}
</style>
