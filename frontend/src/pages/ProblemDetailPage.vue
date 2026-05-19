<template>
  <section class="detail-layout">
    <header class="page-header">
      <h1 class="page-title">Problem Workspace</h1>
      <p class="page-subtitle">
        Problem details will appear here once practice problems are added.
      </p>
    </header>

    <div class="workspace-grid">
      <div class="left-column">
        <SchemaViewer />
        <SampleDataViewer />
      </div>

      <div class="right-column">
        <section class="panel">
          <SqlEditor v-model="query" />
        </section>
        <FeedbackPanel />
        <section class="panel">
          <h2 class="section-title">Results</h2>
          <ResultTable />
        </section>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from "vue";

import FeedbackPanel from "../components/FeedbackPanel.vue";
import ResultTable from "../components/ResultTable.vue";
import SampleDataViewer from "../components/SampleDataViewer.vue";
import SchemaViewer from "../components/SchemaViewer.vue";
import SqlEditor from "../components/SqlEditor.vue";

const query = ref("");
</script>

<style scoped>
.workspace-grid {
  display: grid;
  grid-template-columns: minmax(0, 360px) minmax(0, 1fr);
  gap: 16px;
}

.left-column,
.right-column {
  display: grid;
  align-content: start;
  gap: 16px;
}

@media (max-width: 860px) {
  .workspace-grid {
    grid-template-columns: 1fr;
  }
}
</style>
