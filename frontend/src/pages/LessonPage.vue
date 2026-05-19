<template>
  <section>
    <header class="page-header">
      <RouterLink class="back-link" :to="`/roadmap/${route.params.moduleId}`">
        Back to module
      </RouterLink>
      <h1 class="page-title">{{ lesson?.title || "Lesson" }}</h1>
      <p class="page-subtitle">{{ lesson?.learning_objective }}</p>
    </header>

    <div v-if="isLoading" class="empty-state">Loading lesson...</div>
    <div v-else-if="errorMessage" class="empty-state">{{ errorMessage }}</div>
    <div v-else class="lesson-layout">
      <div class="content-column">
        <div class="concepts">
          <ConceptBadge
            v-for="concept in lesson.concepts"
            :key="concept"
            :concept="concept"
          />
        </div>

        <TutorialPanel :tutorial="lesson.tutorial" />
        <SchemaViewer :tables="lesson.schema" />
        <SampleDataViewer :schema="lesson.schema" :seed-data="lesson.seed_data" />
        <GuidedExamplePanel :example="lesson.guided_example" />

        <section class="panel">
          <h2 class="section-title">Practice</h2>
          <p class="practice-prompt">{{ lesson.practice.prompt }}</p>
        </section>

        <HintPanel :hints="lesson.hints" />
      </div>

      <aside class="workspace-column">
        <section class="panel">
          <SqlEditor v-model="query" />
          <div class="actions">
            <button type="button" @click="runQuery">Run Query</button>
            <button class="primary" type="button" @click="submitQuery">
              Submit Answer
            </button>
          </div>
        </section>

        <FeedbackPanel
          :status="feedbackStatus"
          :message="feedbackMessage"
          :error="feedbackError"
        />

        <section class="panel">
          <h2 class="section-title">Your Result</h2>
          <ResultTable
            :columns="userResult?.columns || []"
            :rows="userResult?.rows || []"
          />
        </section>

        <section v-if="expectedResult" class="panel">
          <h2 class="section-title">Expected Result</h2>
          <ResultTable
            :columns="expectedResult.columns"
            :rows="expectedResult.rows"
          />
        </section>
      </aside>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";

import { fetchLesson, runLessonQuery, submitLessonQuery } from "../api/roadmap";
import ConceptBadge from "../components/ConceptBadge.vue";
import FeedbackPanel from "../components/FeedbackPanel.vue";
import GuidedExamplePanel from "../components/GuidedExamplePanel.vue";
import HintPanel from "../components/HintPanel.vue";
import ResultTable from "../components/ResultTable.vue";
import SampleDataViewer from "../components/SampleDataViewer.vue";
import SchemaViewer from "../components/SchemaViewer.vue";
import SqlEditor from "../components/SqlEditor.vue";
import TutorialPanel from "../components/TutorialPanel.vue";

const route = useRoute();
const lesson = ref(null);
const query = ref("");
const userResult = ref(null);
const expectedResult = ref(null);
const feedbackStatus = ref("idle");
const feedbackMessage = ref("");
const feedbackError = ref("");
const isLoading = ref(true);
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
  expectedResult.value = null;
  feedbackError.value = "";

  try {
    const data = await runLessonQuery(
      route.params.moduleId,
      route.params.lessonId,
      query.value,
    );
    userResult.value = data.result;
    feedbackStatus.value = "success";
    feedbackMessage.value = "Query ran successfully. Check your result before submitting.";
  } catch (error) {
    feedbackStatus.value = "error";
    feedbackMessage.value = "The query could not run.";
    feedbackError.value = error.message;
  }
}

async function submitQuery() {
  feedbackError.value = "";

  const data = await submitLessonQuery(
    route.params.moduleId,
    route.params.lessonId,
    query.value,
  );

  userResult.value = data.user_result;
  expectedResult.value = data.expected_result;
  feedbackStatus.value = data.is_correct ? "success" : "error";
  feedbackMessage.value = data.feedback;
  feedbackError.value = data.error || "";
}
</script>

<style scoped>
.back-link {
  color: #1459b8;
  font-weight: 800;
}

.lesson-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(340px, 440px);
  gap: 16px;
}

.content-column,
.workspace-column {
  display: grid;
  align-content: start;
  gap: 16px;
}

.workspace-column {
  position: sticky;
  top: 16px;
}

.concepts {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.practice-prompt {
  margin: 0;
  color: #101828;
  font-weight: 700;
  line-height: 1.6;
}

.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 14px;
}

button {
  border: 1px solid #cfd8e6;
  border-radius: 8px;
  background: #ffffff;
  color: #1459b8;
  cursor: pointer;
  font-weight: 800;
  padding: 10px 14px;
}

button.primary {
  border-color: #1459b8;
  background: #1459b8;
  color: #ffffff;
}

@media (max-width: 960px) {
  .lesson-layout {
    grid-template-columns: 1fr;
  }

  .workspace-column {
    position: static;
  }
}
</style>
