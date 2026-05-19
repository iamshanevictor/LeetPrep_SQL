<template>
  <section>
    <header class="page-header">
      <RouterLink class="back-link" :to="`/roadmap/${route.params.moduleId}`">
        Back to module
      </RouterLink>
      <h1 class="page-title">{{ bossProblem?.title || "Boss Problem" }}</h1>
      <p class="page-subtitle">{{ bossProblem?.prompt }}</p>
    </header>

    <div v-if="isLoading" class="empty-state">Loading boss problem...</div>
    <div v-else-if="errorMessage" class="empty-state">{{ errorMessage }}</div>
    <div v-else class="boss-layout">
      <div class="content-column">
        <div class="concepts">
          <ConceptBadge
            v-for="concept in bossProblem.concepts"
            :key="concept"
            :concept="concept"
          />
        </div>

        <section class="panel">
          <h2 class="section-title">Prerequisites</h2>
          <ul class="plain-list">
            <li v-for="lessonId in bossProblem.prerequisites" :key="lessonId">
              {{ lessonId }}
            </li>
          </ul>
        </section>

        <SchemaViewer :tables="bossProblem.schema" />
        <SampleDataViewer
          :schema="bossProblem.schema"
          :seed-data="bossProblem.seed_data"
        />

        <HintPanel :hints="bossProblem.hints" />

        <section class="panel">
          <h2 class="section-title">Common Mistakes</h2>
          <ul class="plain-list">
            <li v-for="mistake in bossProblem.common_mistakes" :key="mistake">
              {{ mistake }}
            </li>
          </ul>
        </section>
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

import { fetchBossProblem, runBossQuery, submitBossQuery } from "../api/roadmap";
import ConceptBadge from "../components/ConceptBadge.vue";
import FeedbackPanel from "../components/FeedbackPanel.vue";
import HintPanel from "../components/HintPanel.vue";
import ResultTable from "../components/ResultTable.vue";
import SampleDataViewer from "../components/SampleDataViewer.vue";
import SchemaViewer from "../components/SchemaViewer.vue";
import SqlEditor from "../components/SqlEditor.vue";

const route = useRoute();
const bossProblem = ref(null);
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
    const data = await fetchBossProblem(route.params.moduleId);
    bossProblem.value = data.boss_problem;
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
    const data = await runBossQuery(route.params.moduleId, query.value);
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

  const data = await submitBossQuery(route.params.moduleId, query.value);
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

.boss-layout {
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

.plain-list {
  display: grid;
  gap: 8px;
  margin: 0;
  padding-left: 22px;
  color: #526070;
  line-height: 1.5;
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
  .boss-layout {
    grid-template-columns: 1fr;
  }

  .workspace-column {
    position: static;
  }
}
</style>
