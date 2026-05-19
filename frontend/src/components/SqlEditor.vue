<template>
  <label class="editor">
    <span>{{ label }}</span>
    <textarea
      :value="modelValue"
      :placeholder="placeholder"
      rows="10"
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
    default: "SQL Query",
  },
  placeholder: {
    type: String,
    default: "SELECT * FROM table_name;",
  },
});

defineEmits(["update:modelValue"]);
</script>

<style scoped>
.editor {
  display: grid;
  gap: 8px;
  color: #101828;
  font-weight: 700;
}

textarea {
  width: 100%;
  min-height: 220px;
  resize: vertical;
  border: 1px solid #cfd8e6;
  border-radius: 8px;
  background: #0f172a;
  color: #f8fafc;
  line-height: 1.5;
  padding: 14px;
}

textarea:focus {
  border-color: #3b82f6;
  outline: 3px solid rgba(59, 130, 246, 0.18);
}
</style>
