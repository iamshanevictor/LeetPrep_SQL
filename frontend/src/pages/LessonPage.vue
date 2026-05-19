<template>
  <section class="page">
    <RouterLink class="back-link" :to="`/roadmap/${route.params.moduleId}`">
      Back to Module
    </RouterLink>

    <PageHeader
      eyebrow="Lesson"
      :title="lesson?.title || 'Lesson'"
      :subtitle="lesson?.learning_objective || ''"
    />

    <LoadingState v-if="isLoading" message="Loading lesson..." />
    <ErrorState v-else-if="errorMessage" title="Could not load lesson" :message="errorMessage" />
    <div v-else class="two-column-layout lesson-layout">
      <main class="stack-lg">
        <section class="card">
          <div class="card-header">
            <h2 class="card-title">Learning Objective</h2>
            <p class="card-description">{{ lesson.learning_objective }}</p>
          </div>
          <div class="concept-list">
            <ConceptBadge
              v-for="concept in lesson.concepts"
              :key="concept"
              :concept="concept"
            />
          </div>
        </section>

        <TutorialPanel :tutorial="lesson.tutorial" />
        <GuidedExamplePanel :guided-example="lesson.guided_example" />

        <section class="card practice-card">
          <div class="card-header">
            <h2 class="card-title">Practice Prompt</h2>
            <p class="card-description">{{ lesson.practice.prompt }}</p>
          </div>

          <div class="expected-output">
            <h3>Expected Output</h3>
            <ResultTable
              :result="lesson.expected_result"
              empty-message="Expected output is not available yet."
            />
          </div>
        </section>

        <HintPanel :hints="lesson.hints" />
      </main>

      <aside class="workspace-column stack">
        <SchemaViewer :schema="lesson.schema" />
        <SampleDataViewer :schema="lesson.schema" :seed-data="lesson.seed_data" />

        <section class="card editor-card">
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

        <section class="card">
          <div class="card-header">
            <h2 class="card-title">Your Result</h2>
          </div>
          <ResultTable :result="userResult" empty-message="Run your query to see results." />
        </section>

        <section v-if="expectedResult" class="card">
          <div class="card-header">
            <h2 class="card-title">Expected Result</h2>
            <p class="card-description">Shown after an incorrect submission for comparison.</p>
          </div>
          <ResultTable :result="expectedResult" />
        </section>
      </aside>
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
import PageHeader from "../components/layout/PageHeader.vue";
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
.lesson-layout {
  align-items: start;
}

.workspace-column {
  position: sticky;
  top: 86px;
}

.concept-list {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
}

.practice-card,
.expected-output {
  display: grid;
  gap: var(--space-4);
}

.expected-output h3 {
  margin: 0;
  color: var(--color-text);
  font-size: 15px;
}

.editor-card {
  display: grid;
  gap: var(--space-4);
}

@media (max-width: 920px) {
  .workspace-column {
    position: static;
  }
}
</style>
