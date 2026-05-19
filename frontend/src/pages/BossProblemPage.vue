<template>
  <section class="page">
    <RouterLink class="back-link" :to="`/roadmap/${route.params.moduleId}`">
      Back to Module
    </RouterLink>

    <PageHeader
      eyebrow="Boss Problem"
      :title="bossProblem?.title || 'Boss Problem'"
      subtitle="Final challenge for this module. Use the concepts together, then submit when your result matches the target output."
    />

    <LoadingState v-if="isLoading" message="Loading boss problem..." />
    <ErrorState
      v-else-if="errorMessage"
      title="Could not load boss problem"
      :message="errorMessage"
    />
    <div v-else class="two-column-layout boss-layout">
      <main class="stack-lg">
        <section class="boss-prompt">
          <p class="boss-label">Final Challenge</p>
          <h2>{{ bossProblem.title }}</h2>
          <p>{{ bossProblem.prompt }}</p>
        </section>

        <section class="card">
          <div class="card-header">
            <h2 class="card-title">Required Concepts</h2>
          </div>
          <div class="concept-list">
            <ConceptBadge
              v-for="concept in bossProblem.concepts"
              :key="concept"
              :concept="concept"
            />
          </div>
        </section>

        <section class="card">
          <div class="card-header">
            <h2 class="card-title">Prerequisites</h2>
            <p class="card-description">Review these lessons if the challenge feels too big.</p>
          </div>
          <ul class="plain-list">
            <li v-for="lessonId in bossProblem.prerequisites" :key="lessonId">
              {{ lessonId }}
            </li>
          </ul>
        </section>

        <section class="card">
          <div class="card-header">
            <h2 class="card-title">Expected Output</h2>
            <p class="card-description">Your submitted query should return these columns and rows.</p>
          </div>
          <ResultTable :result="bossProblem.expected_result" />
        </section>

        <HintPanel :hints="bossProblem.hints" />

        <section class="card">
          <div class="card-header">
            <h2 class="card-title">Common Mistakes</h2>
          </div>
          <ul class="plain-list">
            <li v-for="mistake in bossProblem.common_mistakes" :key="mistake">
              {{ mistake }}
            </li>
          </ul>
        </section>
      </main>

      <aside class="workspace-column stack">
        <SchemaViewer :schema="bossProblem.schema" />
        <SampleDataViewer
          :schema="bossProblem.schema"
          :seed-data="bossProblem.seed_data"
        />

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

import { fetchBossProblem, runBossQuery, submitBossQuery } from "../api/roadmap";
import FeedbackPanel from "../components/learning/FeedbackPanel.vue";
import HintPanel from "../components/learning/HintPanel.vue";
import ResultTable from "../components/learning/ResultTable.vue";
import SampleDataViewer from "../components/learning/SampleDataViewer.vue";
import SchemaViewer from "../components/learning/SchemaViewer.vue";
import SqlEditor from "../components/learning/SqlEditor.vue";
import PageHeader from "../components/layout/PageHeader.vue";
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
.boss-layout {
  align-items: start;
}

.workspace-column {
  position: sticky;
  top: 86px;
}

.boss-prompt {
  display: grid;
  gap: var(--space-3);
  border: 1px solid #f2c078;
  border-radius: var(--radius-lg);
  background: linear-gradient(180deg, #fff7e8, #ffffff);
  box-shadow: var(--shadow-card);
  padding: var(--space-6);
}

.boss-label,
.boss-prompt h2,
.boss-prompt p {
  margin: 0;
}

.boss-label {
  color: var(--color-warning);
  font-size: 13px;
  font-weight: 900;
  text-transform: uppercase;
}

.boss-prompt h2 {
  color: var(--color-text);
  font-size: 24px;
}

.boss-prompt p {
  color: var(--color-text);
  font-size: 17px;
  font-weight: 700;
  line-height: 1.6;
}

.concept-list {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
}

.plain-list {
  display: grid;
  gap: var(--space-2);
  margin: 0;
  padding-left: 22px;
  color: var(--color-muted);
  line-height: 1.55;
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
