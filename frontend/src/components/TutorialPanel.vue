<template>
  <section class="panel tutorial-panel">
    <h2 class="section-title">Concept Tutorial</h2>
    <p>{{ tutorial.explanation }}</p>

    <div class="syntax-block">
      <h3>Syntax Pattern</h3>
      <pre><code>{{ tutorial.syntax }}</code></pre>
    </div>

    <div class="mental-model">
      <h3>Mental Model</h3>
      <p>{{ tutorial.mental_model }}</p>
    </div>
  </section>
</template>

<script setup>
defineProps({
  tutorial: {
    type: Object,
    required: true,
  },
});
</script>

<style scoped>
.tutorial-panel {
  display: grid;
  gap: 14px;
}

p {
  margin: 0;
  color: #526070;
  line-height: 1.6;
}

h3 {
  margin: 0 0 8px;
  color: #344054;
  font-size: 14px;
}

pre {
  overflow-x: auto;
  border-radius: 8px;
  background: #0f172a;
  color: #f8fafc;
  margin: 0;
  padding: 14px;
}

code {
  font-family: "Cascadia Code", "Fira Code", Consolas, monospace;
  font-size: 13px;
}

.mental-model {
  border-left: 4px solid #4f9d69;
  background: #f2fbf5;
  padding: 12px;
}
</style>
