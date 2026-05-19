<template>
  <section class="workspace-page">
    <LoadingState v-if="isLoading" class="workspace-state" message="Loading boss problem..." />
    <ErrorState
      v-else-if="errorMessage"
      class="workspace-state"
      title="Could not load boss problem"
      :message="errorMessage"
    />

    <div v-else class="dense-workspace">
      <header class="workspace-topbar">
        <div class="crumbs">
          <RouterLink :to="`/roadmap/${route.params.moduleId}`">Module</RouterLink>
          <span>/</span>
          <strong>{{ bossProblem.title }}</strong>
        </div>
        <div class="topbar-actions">
          <span class="badge badge-medium">Boss Problem</span>
          <RouterLink class="button button-secondary" to="/roadmap">Roadmap</RouterLink>
        </div>
      </header>

      <div class="workspace-columns">
        <aside class="workspace-panel left-panel">
          <section class="boss-prompt">
            <span class="badge badge-medium">Final challenge</span>
            <h1>{{ bossProblem.title }}</h1>
            <p>{{ bossProblem.prompt }}</p>
          </section>

          <section class="panel-section">
            <h2>Required concepts</h2>
            <div class="concept-list">
              <ConceptBadge
                v-for="concept in bossProblem.concepts"
                :key="concept"
                :concept="concept"
              />
            </div>
          </section>

          <section class="panel-section">
            <h2>Prerequisites</h2>
            <ul class="compact-list">
              <li v-for="lessonId in bossProblem.prerequisites" :key="lessonId">
                {{ lessonId }}
              </li>
            </ul>
          </section>
        </aside>

        <main class="workspace-panel center-panel">
          <section class="editor-section">
            <SqlEditor
              v-model="query"
              :disabled="isRunning || isSubmitting"
              placeholder="WITH ... AS (...)&#10;SELECT ...;"
            />
            <div class="actions">
              <button
                class="button button-secondary"
                type="button"
                :disabled="isRunning || isSubmitting"
                @click="runQuery"
              >
                {{ isRunning ? "Running..." : "Run Query" }}
              </button>
              <button
                class="button button-primary"
                type="button"
                :disabled="isRunning || isSubmitting"
                @click="submitQuery"
              >
                {{ isSubmitting ? "Submitting..." : "Submit Answer" }}
              </button>
            </div>
          </section>

          <FeedbackPanel :feedback="feedback" />

          <section class="result-section">
            <div class="result-header">
              <h2>Your result</h2>
              <span class="badge">DuckDB</span>
            </div>
            <ResultTable :result="userResult" empty-message="Run your query to see results." />
          </section>

          <section v-if="expectedResult" class="result-section">
            <div class="result-header">
              <h2>Expected result</h2>
            </div>
            <ResultTable :result="expectedResult" />
          </section>
        </main>

        <aside class="workspace-panel right-panel">
          <SchemaViewer :schema="bossProblem.schema" />
          <SampleDataViewer
            :schema="bossProblem.schema"
            :seed-data="bossProblem.seed_data"
          />

          <section class="panel-section">
            <div class="result-header">
              <h2>Expected output</h2>
            </div>
            <ResultTable
              :result="bossProblem.expected_result"
              empty-message="Expected output is not available."
            />
          </section>

          <HintPanel :hints="bossProblem.hints" />

          <section class="panel-section">
            <h2>Common mistakes</h2>
            <ul class="compact-list">
              <li v-for="mistake in bossProblem.common_mistakes" :key="mistake">
                {{ mistake }}
              </li>
            </ul>
          </section>
        </aside>
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";

import { fetchBossProblem, runBossQuery, submitBossQuery } from "../api/roadmap";
import FeedbackPanel from "../components/learning/FeedbackPanel.vue";
import HintPanel from "../components/learning/HintPanel.vue";
import ResultTable from "../components/learning/ResultTable.vue";
import SampleDataViewer from "../components/learning/SampleDataViewer.vue";
import SchemaViewer from "../components/learning/SchemaViewer.vue";
import SqlEditor from "../components/learning/SqlEditor.vue";
import ConceptBadge from "../components/ui/ConceptBadge.vue";
import ErrorState from "../components/ui/ErrorState.vue";
import LoadingState from "../components/ui/LoadingState.vue";

const route = useRoute();
const bossProblem = ref(null);
const query = ref("");
const userResult = ref(null);
const expectedResult = ref(null);
const feedback = ref({ status: "neutral", message: "" });
const isLoading = ref(true);
const isRunning = ref(false);
const isSubmitting = ref(false);
const errorMessage = ref("");

onMounted(async () => {
  try {
    const data = await fetchBossProblem(route.params.moduleId);
    bossProblem.value = data.boss_problem;
  } catch (error) {
    errorMessage.value = error.message;
  } finally {
    isLoading.value = false;
  }
});

async function runQuery() {
  isRunning.value = true;
  expectedResult.value = null;
  feedback.value = { status: "neutral", message: "Running your query..." };

  try {
    const data = await runBossQuery(route.params.moduleId, query.value);
    userResult.value = data.result;
    feedback.value = {
      status: "success",
      message: "Query ran successfully. Review your output before submitting.",
    };
  } catch (error) {
    feedback.value = {
      status: "error",
      message: "The query could not run.",
      error: error.message,
    };
  } finally {
    isRunning.value = false;
  }
}

async function submitQuery() {
  isSubmitting.value = true;
  feedback.value = { status: "neutral", message: "Checking your answer..." };

  try {
    const data = await submitBossQuery(route.params.moduleId, query.value);
    userResult.value = data.user_result;
    expectedResult.value = data.expected_result;
    feedback.value = {
      status: data.is_correct ? "success" : "incorrect",
      message: data.feedback,
      error: data.error || "",
    };
  } catch (error) {
    feedback.value = {
      status: "error",
      message: "The submission could not be checked.",
      error: error.message,
    };
  } finally {
    isSubmitting.value = false;
  }
}
</script>

<style scoped>
.workspace-page {
  height: 100%;
  min-height: 0;
  padding: var(--space-2);
}

.workspace-state {
  margin: var(--space-3);
}

.dense-workspace {
  display: grid;
  grid-template-rows: 38px minmax(0, 1fr);
  gap: var(--space-2);
  height: 100%;
  min-height: 0;
}

.workspace-topbar,
.workspace-panel {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
}

.workspace-topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-2);
  padding: 0 var(--space-2);
}

.crumbs,
.topbar-actions,
.concept-list,
.result-header {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: var(--space-1);
}

.crumbs {
  min-width: 0;
  color: var(--color-text-muted);
  font-size: var(--font-sm);
}

.crumbs a {
  color: var(--color-primary);
}

.crumbs strong {
  overflow: hidden;
  color: var(--color-text);
  text-overflow: ellipsis;
  white-space: nowrap;
}

.workspace-columns {
  display: grid;
  grid-template-columns: minmax(260px, 30%) minmax(360px, 42%) minmax(260px, 28%);
  gap: var(--space-2);
  min-height: 0;
}

.workspace-panel {
  display: grid;
  align-content: start;
  gap: var(--space-2);
  min-height: 0;
  overflow-y: auto;
  padding: var(--space-3);
}

.panel-section,
.editor-section,
.result-section,
.boss-prompt {
  display: grid;
  gap: var(--space-2);
  border-bottom: 1px solid var(--color-border);
  padding-bottom: var(--space-2);
}

.panel-section:last-child,
.result-section:last-child {
  border-bottom: 0;
}

h1,
h2,
p {
  margin: 0;
}

h1 {
  color: var(--color-text);
  font-size: 19px;
  line-height: 1.25;
}

h2 {
  color: var(--color-text);
  font-size: var(--font-md);
}

p,
.compact-list {
  color: var(--color-text-muted);
  font-size: var(--font-sm);
  line-height: 1.45;
}

.compact-list {
  display: grid;
  gap: var(--space-1);
  margin: 0;
  padding-left: 18px;
}

.boss-prompt {
  border-left: 3px solid var(--color-warning);
  border-bottom: 1px solid var(--color-border);
  background: var(--color-warning-soft);
  padding: var(--space-2);
}

.result-header {
  justify-content: space-between;
}

.center-panel :deep(.result-table) {
  max-height: 190px;
}

@media (max-width: 1100px) {
  .workspace-columns {
    grid-template-columns: minmax(260px, 34%) minmax(360px, 66%);
  }

  .right-panel {
    grid-column: 1 / -1;
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 760px) {
  .workspace-page {
    height: auto;
  }

  .dense-workspace,
  .workspace-columns {
    height: auto;
  }

  .workspace-columns,
  .right-panel {
    grid-template-columns: 1fr;
  }

  .workspace-panel {
    overflow: visible;
  }
}
</style>
