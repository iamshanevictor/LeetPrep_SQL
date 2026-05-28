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
          <strong>{{ bossUnlocked ? bossProblem.title : "Boss Problem Locked" }}</strong>
        </div>
        <div class="topbar-actions">
          <span class="badge badge-medium">Boss Problem</span>
          <RouterLink class="button button-secondary" to="/roadmap">Roadmap</RouterLink>
        </div>
      </header>

      <div v-if="!bossUnlocked" class="locked-boss-panel">
        <span class="badge badge-medium">Boss Problem</span>
        <h1>Final challenge locked</h1>
        <p>
          Complete every lesson in {{ moduleData?.title || "this module" }} to reveal the boss
          problem. The prompt, schema, sample data, hints, and expected output stay hidden until
          then.
        </p>
        <RouterLink
          v-if="nextIncompleteLesson"
          class="button button-primary"
          :to="`/roadmap/${route.params.moduleId}/lessons/${nextIncompleteLesson.id}`"
        >
          Continue Lessons
        </RouterLink>
      </div>

      <div v-else class="workspace-columns">
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
import FeedbackPanel from "../components/learning/FeedbackPanel.vue";
import HintPanel from "../components/learning/HintPanel.vue";
import ResultTable from "../components/learning/ResultTable.vue";
import SampleDataViewer from "../components/learning/SampleDataViewer.vue";
import SchemaViewer from "../components/learning/SchemaViewer.vue";
import SqlEditor from "../components/learning/SqlEditor.vue";
import ConceptBadge from "../components/ui/ConceptBadge.vue";
import ErrorState from "../components/ui/ErrorState.vue";
import LoadingState from "../components/ui/LoadingState.vue";
import { useBossWorkspace } from "../composables/useBossWorkspace";

const {
  route,
  bossProblem,
  moduleData,
  query,
  userResult,
  expectedResult,
  feedback,
  isLoading,
  isRunning,
  isSubmitting,
  errorMessage,
  bossUnlocked,
  nextIncompleteLesson,
  runQuery,
  submitQuery,
} = useBossWorkspace();
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
.workspace-panel,
.locked-boss-panel {
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

.locked-boss-panel {
  display: grid;
  align-content: center;
  justify-items: start;
  gap: var(--space-3);
  min-height: 320px;
  border-color: var(--color-warning);
  background: var(--color-warning-soft);
  padding: var(--space-4);
}

.locked-boss-panel h1,
.locked-boss-panel p {
  margin: 0;
}

.locked-boss-panel h1 {
  color: var(--color-text);
  font-size: var(--font-lg);
}

.locked-boss-panel p {
  max-width: 620px;
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
