<template>
  <section class="workspace-page">
    <LoadingState v-if="isLoading" class="workspace-state" message="Loading lesson..." />
    <ErrorState
      v-else-if="errorMessage"
      class="workspace-state"
      title="Could not load lesson"
      :message="errorMessage"
    />

    <div v-else class="dense-workspace">
      <header class="workspace-topbar">
        <div class="crumbs">
          <RouterLink :to="`/roadmap/${route.params.moduleId}`">Module</RouterLink>
          <span>/</span>
          <strong>{{ lesson.title }}</strong>
        </div>
        <div class="topbar-actions">
          <RouterLink class="button button-secondary" to="/roadmap">Roadmap</RouterLink>
          <RouterLink class="button button-secondary" :to="`/roadmap/${route.params.moduleId}/boss`">
            Boss
          </RouterLink>
        </div>
      </header>

      <div class="workspace-columns lesson-columns">
        <aside class="workspace-panel left-panel">
          <section class="panel-section">
            <p class="page-eyebrow">Lesson</p>
            <h1>{{ lesson.title }}</h1>
            <p>{{ lesson.learning_objective }}</p>
            <div class="concept-list">
              <ConceptBadge
                v-for="concept in lesson.concepts"
                :key="concept"
                :concept="concept"
              />
            </div>
          </section>

          <section class="panel-section">
            <TutorialPanel :tutorial="lesson.tutorial" />
          </section>

          <section class="panel-section">
            <GuidedExamplePanel :guided-example="lesson.guided_example" />
          </section>
        </aside>

        <main class="workspace-panel center-panel">
          <section class="practice-strip">
            <div>
              <h2>Practice</h2>
              <p>{{ lesson.practice.prompt }}</p>
            </div>
            <span class="badge">{{ lesson.practice.order_matters ? "Ordered" : "Any order" }}</span>
          </section>

          <section class="editor-section">
            <SqlEditor v-model="query" :disabled="isRunning || isSubmitting" />
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
          <SchemaViewer :schema="lesson.schema" />
          <SampleDataViewer :schema="lesson.schema" :seed-data="lesson.seed_data" />

          <section class="panel-section">
            <div class="result-header">
              <h2>Expected output</h2>
            </div>
            <ResultTable
              :result="lesson.expected_result"
              empty-message="Expected output is not available."
            />
          </section>

          <HintPanel :hints="lesson.hints" />
        </aside>
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";

import { fetchLesson, runLessonQuery, submitLessonQuery } from "../api/roadmap";
import FeedbackPanel from "../components/learning/FeedbackPanel.vue";
import GuidedExamplePanel from "../components/learning/GuidedExamplePanel.vue";
import HintPanel from "../components/learning/HintPanel.vue";
import ResultTable from "../components/learning/ResultTable.vue";
import SampleDataViewer from "../components/learning/SampleDataViewer.vue";
import SchemaViewer from "../components/learning/SchemaViewer.vue";
import SqlEditor from "../components/learning/SqlEditor.vue";
import TutorialPanel from "../components/learning/TutorialPanel.vue";
import ConceptBadge from "../components/ui/ConceptBadge.vue";
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
.practice-strip {
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

p {
  color: var(--color-text-muted);
  font-size: var(--font-sm);
  line-height: 1.45;
}

.practice-strip {
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: start;
}

.result-header {
  justify-content: space-between;
}

.center-panel :deep(.result-table) {
  max-height: 180px;
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
