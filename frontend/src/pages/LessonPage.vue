<template>
  <section class="leetcode-workspace">
    <LoadingState v-if="isLoading" class="workspace-state" message="Loading lesson..." />
    <ErrorState
      v-else-if="errorMessage"
      class="workspace-state"
      title="Could not load lesson"
      :message="errorMessage"
    />

    <div v-else class="workspace-grid">
      <aside class="description-pane">
        <div class="pane-toolbar">
          <RouterLink class="back-link-dark" :to="`/roadmap/${route.params.moduleId}`">
            Back to Module
          </RouterLink>
          <span>{{ lesson.title }}</span>
        </div>
        <LeetCodeDescription
          label="Lesson"
          :title="lesson.title"
          :concepts="lesson.concepts"
          :prompt="lesson.practice.prompt"
          :schema="lesson.schema"
          :seed-data="lesson.seed_data"
          :expected-result="lesson.expected_result"
          :order-matters="lesson.practice.order_matters"
          :tutorial="lesson.tutorial"
          :guided-example="lesson.guided_example"
          :hints="lesson.hints"
        />
      </aside>

      <main class="code-pane">
        <header class="run-toolbar">
          <div class="toolbar-title">
            <span class="code-icon">SQL</span>
            <strong>Code</strong>
          </div>
          <div class="toolbar-actions">
            <button
              class="run-button"
              type="button"
              :disabled="isRunning || isSubmitting"
              @click="runQuery"
            >
              {{ isRunning ? "Running..." : "Run" }}
            </button>
            <button
              class="submit-button"
              type="button"
              :disabled="isRunning || isSubmitting"
              @click="submitQuery"
            >
              {{ isSubmitting ? "Submitting..." : "Submit" }}
            </button>
          </div>
        </header>

        <section class="editor-panel">
          <div class="editor-meta">
            <span>DuckDB SQL</span>
            <span>Auto</span>
          </div>
          <SqlEditor
            v-model="query"
            label=""
            :disabled="isRunning || isSubmitting"
            placeholder="-- Write your SQL query below&#10;SELECT ...&#10;FROM ...;"
          />
        </section>

        <section class="result-panel">
          <div class="result-tabs">
            <span class="tab active">Test Result</span>
            <span class="tab">Expected Output</span>
          </div>

          <div class="result-body">
            <FeedbackPanel :feedback="feedback" />

            <div class="result-grid">
              <section class="result-card">
                <h2>Your Result</h2>
                <ResultTable
                  :result="userResult"
                  empty-message="You must run your query first."
                />
              </section>

              <section v-if="expectedResult" class="result-card">
                <h2>Expected Result</h2>
                <ResultTable :result="expectedResult" />
              </section>
            </div>
          </div>
        </section>
      </main>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";

import { fetchLesson, runLessonQuery, submitLessonQuery } from "../api/roadmap";
import FeedbackPanel from "../components/learning/FeedbackPanel.vue";
import LeetCodeDescription from "../components/learning/LeetCodeDescription.vue";
import ResultTable from "../components/learning/ResultTable.vue";
import SqlEditor from "../components/learning/SqlEditor.vue";
import ErrorState from "../components/ui/ErrorState.vue";
import LoadingState from "../components/ui/LoadingState.vue";

const route = useRoute();
const lesson = ref(null);
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
    const data = await fetchLesson(route.params.moduleId, route.params.lessonId);
    lesson.value = data.lesson;
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
    const data = await runLessonQuery(
      route.params.moduleId,
      route.params.lessonId,
      query.value,
    );
    userResult.value = data.result;
    feedback.value = {
      status: "success",
      message: "Query ran successfully. Review your output, then submit when ready.",
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
    const data = await submitLessonQuery(
      route.params.moduleId,
      route.params.lessonId,
      query.value,
    );

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
.leetcode-workspace {
  height: 100%;
  min-height: 0;
  background: #111111;
  color: #f2f2f2;
  padding: 8px;
}

.workspace-state {
  margin: 24px;
}

.workspace-grid {
  display: grid;
  grid-template-columns: minmax(380px, 1fr) minmax(420px, 1fr);
  gap: 8px;
  height: 100%;
  min-height: 0;
}

.description-pane,
.code-pane {
  min-height: 0;
  overflow: hidden;
}

.description-pane {
  display: grid;
  grid-template-rows: 34px minmax(0, 1fr);
  gap: 8px;
}

.pane-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  border-radius: 8px;
  background: #1f1f1f;
  color: #bdbdbd;
  font-size: 13px;
  font-weight: 700;
  padding: 0 12px;
}

.back-link-dark {
  color: #8ebeff;
}

.code-pane {
  display: grid;
  grid-template-rows: 44px minmax(230px, 1fr) minmax(230px, 0.9fr);
  gap: 8px;
}

.run-toolbar,
.editor-panel,
.result-panel {
  border-radius: 8px;
  background: #242424;
}

.run-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 0 12px;
}

.toolbar-title,
.toolbar-actions,
.editor-meta,
.result-tabs {
  display: flex;
  align-items: center;
  gap: 10px;
}

.code-icon {
  color: #2ecc71;
  font-weight: 900;
}

.toolbar-actions button {
  border: 0;
  border-radius: 7px;
  cursor: pointer;
  font-weight: 900;
  padding: 8px 16px;
}

.toolbar-actions button:disabled {
  cursor: not-allowed;
  opacity: 0.62;
}

.run-button {
  background: #343434;
  color: #e8e8e8;
}

.submit-button {
  background: #1db954;
  color: #06210f;
}

.editor-panel {
  display: grid;
  grid-template-rows: 34px minmax(0, 1fr);
  min-height: 0;
  overflow: hidden;
}

.editor-meta {
  border-bottom: 1px solid #333333;
  color: #bdbdbd;
  font-size: 13px;
  padding: 0 12px;
}

.editor-panel :deep(.sql-editor) {
  min-height: 0;
}

.editor-panel :deep(textarea) {
  min-height: 0;
  border: 0;
  border-radius: 0;
  background: #242424;
  color: #f2f2f2;
  font-size: 14px;
  line-height: 1.6;
}

.result-panel {
  display: grid;
  grid-template-rows: 36px minmax(0, 1fr);
  min-height: 0;
  overflow: hidden;
}

.result-tabs {
  border-bottom: 1px solid #333333;
  padding: 0 12px;
}

.tab {
  color: #a7a7a7;
  font-size: 13px;
  font-weight: 800;
}

.tab.active {
  color: #ffffff;
}

.result-body {
  display: grid;
  grid-template-rows: auto minmax(0, 1fr);
  gap: 10px;
  min-height: 0;
  overflow-y: auto;
  padding: 12px;
}

.result-grid {
  display: grid;
  gap: 10px;
}

.result-card {
  display: grid;
  gap: 10px;
}

.result-card h2 {
  margin: 0;
  color: #ffffff;
  font-size: 14px;
}

.result-panel :deep(.feedback-panel) {
  box-shadow: none;
}

.result-panel :deep(.result-table) {
  border-color: #3f3f3f;
}

.result-panel :deep(table) {
  background: #242424;
  color: #dedede;
}

.result-panel :deep(th) {
  background: #303030;
  color: #ffffff;
}

.result-panel :deep(th),
.result-panel :deep(td) {
  border-color: #3f3f3f;
}

.result-panel :deep(.empty-result) {
  color: #8c8c8c;
  text-align: center;
  padding: 54px 16px;
}

@media (max-width: 900px) {
  .workspace-container {
    height: auto;
    overflow: visible;
  }

  .leetcode-workspace {
    height: auto;
    min-height: 100vh;
  }

  .workspace-grid {
    grid-template-columns: 1fr;
    height: auto;
  }

  .description-pane {
    min-height: 620px;
  }

  .code-pane {
    min-height: 760px;
  }
}
</style>
