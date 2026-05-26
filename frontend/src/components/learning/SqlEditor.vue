<template>
  <label class="sql-editor">
    <span v-if="label">{{ label }}</span>
    <textarea
      :value="modelValue"
      :placeholder="placeholder"
      :disabled="disabled"
      rows="9"
      aria-label="SQL query editor"
      @input="$emit('update:modelValue', $event.target.value)"
    />
    <small>Only SELECT and WITH queries are allowed.</small>
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
    default: "SQL editor",
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
  gap: var(--space-1);
  min-height: 0;
  color: var(--color-text);
  font-size: var(--font-sm);
  font-weight: 800;
}

textarea {
  width: 100%;
  min-height: 190px;
  resize: vertical;
  border: 1px solid var(--color-code-border);
  border-radius: var(--radius-sm);
  background: var(--color-code-bg);
  color: var(--color-code-text);
  font-family: "Cascadia Code", "Fira Code", Consolas, monospace;
  font-size: 13px;
  line-height: 1.5;
  padding: var(--space-2);
}

textarea::placeholder {
  color: var(--color-code-placeholder);
}

textarea:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 2px color-mix(in srgb, var(--color-primary) 22%, transparent);
  outline: none;
}

textarea:disabled {
  opacity: 0.7;
}

small {
  color: var(--color-text-muted);
  font-size: var(--font-xs);
  font-weight: 600;
}
</style>
