<template>
  <div class="sql-editor">
    <label v-if="label">{{ label }}</label>
    <div class="editor-wrapper">
      <div class="editor-container">
        <textarea
          ref="editorInput"
          :value="modelValue"
          :placeholder="placeholder"
          :disabled="disabled"
          rows="9"
          aria-label="SQL query editor"
          @input="handleInput"
          @keydown="handleKeydown"
          @scroll="syncScroll"
        />
        <div class="syntax-highlighter" :key="highlightKey">
          <div v-for="(line, idx) in highlightedLines" :key="idx" class="highlight-line">
            <span v-for="(token, tIdx) in line" :key="tIdx" :class="token.class">{{ token.text }}</span>
          </div>
        </div>
      </div>
      <div 
        v-if="showAutocomplete" 
        class="autocomplete-menu"
        :style="{ top: menuTop + 'px', left: menuLeft + 'px' }"
      >
        <div
          v-for="(keyword, idx) in filteredKeywords"
          :key="keyword"
          :class="['autocomplete-item', { active: idx === selectedKeywordIdx }]"
          @click="selectKeyword(keyword)"
          @mouseenter="selectedKeywordIdx = idx"
        >
          {{ keyword }}
        </div>
      </div>
    </div>
    <small>Only SELECT and WITH queries are allowed.</small>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick } from "vue";

const props = defineProps({
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

const emit = defineEmits(["update:modelValue"]);

const editorInput = ref(null);
const showAutocomplete = ref(false);
const selectedKeywordIdx = ref(0);
const highlightKey = ref(0);
const currentWord = ref("");
const menuTop = ref(0);
const menuLeft = ref(0);

const SQL_KEYWORDS = [
  // Clauses
  "SELECT", "FROM", "WHERE", "GROUP BY", "HAVING", "ORDER BY", "LIMIT", "OFFSET",
  "WITH",
  // Joins
  "INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL JOIN", "CROSS JOIN", "ON",
  // Operators
  "AND", "OR", "NOT", "IN", "BETWEEN", "LIKE", "IS", "NULL",
  // Functions
  "COUNT", "SUM", "AVG", "MIN", "MAX", "DISTINCT",
  // Case
  "CASE", "WHEN", "THEN", "ELSE", "END",
  // CTE
  "AS",
  // Other
  "DESC", "ASC", "UNION", "UNION ALL",
];

const filteredKeywords = computed(() => {
  if (!currentWord.value) return SQL_KEYWORDS;
  return SQL_KEYWORDS.filter(keyword =>
    keyword.toUpperCase().startsWith(currentWord.value.toUpperCase())
  );
});

const highlightedLines = computed(() => {
  return (props.modelValue || "").split("\n").map(line => highlightLine(line));
});

function highlightLine(line) {
  const tokens = [];
  const regex = /(\s+)|([A-Za-z_]+)|([0-9]+)|([^\s\w])/g;
  let match;

  while ((match = regex.exec(line)) !== null) {
    const [fullMatch, whitespace, word, number, symbol] = match;

    if (whitespace) {
      tokens.push({ text: whitespace, class: "" });
    } else if (word) {
      const upperWord = word.toUpperCase();
      const isKeyword = SQL_KEYWORDS.some(kw => 
        kw.toUpperCase() === upperWord
      );
      tokens.push({
        text: word,
        class: isKeyword ? "keyword" : "",
      });
    } else if (number) {
      tokens.push({ text: number, class: "number" });
    } else if (symbol) {
      tokens.push({ text: symbol, class: "symbol" });
    }
  }

  return tokens;
}

function handleInput(event) {
  emit("update:modelValue", event.target.value);
  highlightKey.value++;
  updateAutocomplete(event);
}

function handleKeydown(event) {
  if (!showAutocomplete.value) return;

  if (event.key === "ArrowDown") {
    event.preventDefault();
    selectedKeywordIdx.value = Math.min(
      selectedKeywordIdx.value + 1,
      filteredKeywords.value.length - 1
    );
  } else if (event.key === "ArrowUp") {
    event.preventDefault();
    selectedKeywordIdx.value = Math.max(selectedKeywordIdx.value - 1, 0);
  } else if (event.key === "Enter") {
    event.preventDefault();
    selectKeyword(filteredKeywords.value[selectedKeywordIdx.value]);
  } else if (event.key === "Escape") {
    showAutocomplete.value = false;
  }
}

function calculateMenuPosition(textarea, wordStart, cursorPos) {
  const textBeforeCursor = textarea.value.substring(0, cursorPos);
  const lines = textBeforeCursor.split('\n');
  const currentLine = lines[lines.length - 1];
  const lineIndex = lines.length - 1;
  
  // Calculate position based on font metrics
  const charWidth = 7.8; // approximate width of monospace char at 13px
  const lineHeight = 19.5; // 1.5em * 13px font-size
  const padding = 8; // textarea padding
  
  menuLeft.value = Math.max(padding, Math.min(currentLine.length * charWidth + padding, textarea.clientWidth - 160));
  menuTop.value = (lineIndex + 1) * lineHeight + padding + 4;
}

function updateAutocomplete(event) {
  const textarea = event.target;
  const text = textarea.value;
  const cursorPos = textarea.selectionStart;

  // Get the word before cursor
  let start = cursorPos - 1;
  while (start >= 0 && /[A-Za-z0-9_]/.test(text[start])) {
    start--;
  }
  start++;

  currentWord.value = text.substring(start, cursorPos);

  // Trigger autocomplete only if there are matching keywords
  if (currentWord.value.length > 0 && filteredKeywords.value.length > 0) {
    showAutocomplete.value = true;
    selectedKeywordIdx.value = 0;
    calculateMenuPosition(textarea, start, cursorPos);
  } else {
    showAutocomplete.value = false;
  }
}

function selectKeyword(keyword) {
  const textarea = editorInput.value;
  const text = textarea.value;
  const cursorPos = textarea.selectionStart;

  // Find start of current word
  let start = cursorPos - 1;
  while (start >= 0 && /[A-Za-z0-9_]/.test(text[start])) {
    start--;
  }
  start++;

  // Replace word with selected keyword
  const newText =
    text.substring(0, start) +
    keyword +
    text.substring(cursorPos);

  emit("update:modelValue", newText);
  showAutocomplete.value = false;
  currentWord.value = "";

  nextTick(() => {
    textarea.focus();
    const newCursorPos = start + keyword.length;
    textarea.setSelectionRange(newCursorPos, newCursorPos);
  });
}

function syncScroll(event) {
  const highlighter = event.target
    .closest(".editor-container")
    ?.querySelector(".syntax-highlighter");
  if (highlighter) {
    highlighter.scrollTop = event.target.scrollTop;
    highlighter.scrollLeft = event.target.scrollLeft;
  }
}

watch(
  () => props.modelValue,
  () => {
    highlightKey.value++;
  }
);
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

label {
  display: block;
  color: var(--color-text);
  font-size: var(--font-sm);
  font-weight: 800;
}

.editor-wrapper {
  position: relative;
  display: grid;
  gap: var(--space-1);
}

.editor-container {
  position: relative;
  display: grid;
  min-height: 190px;
  border: 1px solid var(--color-code-border);
  border-radius: var(--radius-sm);
  background: var(--color-code-bg);
  overflow: hidden;
  grid-template-columns: 1fr;
  grid-template-rows: 1fr;
}

textarea {
  grid-column: 1;
  grid-row: 1;
  width: 100%;
  min-height: 190px;
  resize: vertical;
  border: none;
  background: transparent;
  color: transparent;
  caret-color: #0066cc;
  font-family: "Cascadia Code", "Fira Code", Consolas, monospace;
  font-size: 13px;
  line-height: 1.5;
  padding: var(--space-2);
  margin: 0;
  z-index: 2;
  position: relative;
}

textarea::placeholder {
  color: var(--color-code-placeholder);
}

textarea:focus {
  outline: none;
}

textarea:disabled {
  opacity: 0.7;
}

.syntax-highlighter {
  grid-column: 1;
  grid-row: 1;
  width: 100%;
  min-height: 190px;
  overflow: hidden;
  font-family: "Cascadia Code", "Fira Code", Consolas, monospace;
  font-size: 13px;
  line-height: 1.5;
  padding: var(--space-2);
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
  pointer-events: none;
  color: var(--color-code-text);
}

.highlight-line {
  display: block;
  height: 1.5em;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.keyword {
    color: #0066cc;
    font-weight: 600;
  }

  .number {
    color: #cc6600;
  }

  .symbol {
    color: #333333;
  }

.autocomplete-menu {
  position: absolute;
  background: var(--color-code-bg);
  border: 1px solid var(--color-code-border);
  border-radius: var(--radius-sm);
  max-height: 200px;
  overflow-y: auto;
  z-index: 10;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  min-width: 150px;
}

.autocomplete-item {
  padding: var(--space-1) var(--space-2);
  cursor: pointer;
  color: var(--color-code-text);
  font-family: "Cascadia Code", "Fira Code", Consolas, monospace;
  font-size: 13px;
  white-space: nowrap;
  user-select: none;
  transition: background-color 0.15s ease;
}

.autocomplete-item:hover,
.autocomplete-item.active {
  background-color: color-mix(in srgb, var(--color-primary) 15%, transparent);
  color: var(--color-primary);
  font-weight: 600;
}

small {
  color: var(--color-text-muted);
  font-size: var(--font-xs);
  font-weight: 600;
}

.editor-container:focus-within {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 2px color-mix(in srgb, var(--color-primary) 22%, transparent);
}
</style>
