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

      <section v-if="moduleData && bossUnlocked" class="lesson-navigator">
        <div class="lesson-nav-heading">
          <div>
            <p class="page-eyebrow">Current module</p>
            <h2>{{ moduleData.title }}</h2>
          </div>
          <div class="lesson-nav-actions">
            <RouterLink
              v-if="previousLesson"
              class="button button-secondary"
              :to="`/roadmap/${route.params.moduleId}/lessons/${previousLesson.id}`"
              @mouseenter="prefetchLesson(route.params.moduleId, previousLesson.id)"
              @focus="prefetchLesson(route.params.moduleId, previousLesson.id)"
            >
              Previous
            </RouterLink>
            <RouterLink
              v-if="nextLesson && nextLessonUnlocked"
              class="button button-primary"
              :to="`/roadmap/${route.params.moduleId}/lessons/${nextLesson.id}`"
              @mouseenter="prefetchLesson(route.params.moduleId, nextLesson.id)"
              @focus="prefetchLesson(route.params.moduleId, nextLesson.id)"
            >
              Next Lesson
            </RouterLink>
            <span
              v-else-if="nextLesson"
              class="button button-primary is-disabled"
              aria-disabled="true"
              title="Complete this lesson to unlock the next lesson."
            >
              Next Lesson
            </span>
          </div>
        </div>
        <div class="lesson-nav-list">
          <RouterLink
            v-for="(moduleLesson, index) in moduleData.lessons"
            :key="moduleLesson.id"
            class="lesson-nav-link"
            :class="{ 'is-locked': !isLessonUnlocked(moduleData, moduleLesson.id, progress, roadmapModules) }"
            :to="lessonNavTarget(moduleLesson)"
            :aria-disabled="!isLessonUnlocked(moduleData, moduleLesson.id, progress, roadmapModules)"
            @mouseenter="prefetchLesson(route.params.moduleId, moduleLesson.id)"
            @focus="prefetchLesson(route.params.moduleId, moduleLesson.id)"
            @click="blockLockedLessonNavigation($event, moduleLesson)"
          >
            <span>{{ index + 1 }}</span>
            <strong>{{ moduleLesson.title }}</strong>
            <small>
              {{
                moduleLesson.id === route.params.lessonId
                  ? "Current"
                  : isLessonUnlocked(moduleData, moduleLesson.id, progress, roadmapModules)
                    ? "Open"
                    : "Locked"
              }}
            </small>
          </RouterLink>
          <RouterLink
            v-if="moduleData.boss_problem"
            class="lesson-nav-link boss-link"
            :to="`/roadmap/${route.params.moduleId}/boss`"
            @mouseenter="prefetchBossProblem(route.params.moduleId)"
            @focus="prefetchBossProblem(route.params.moduleId)"
          >
            <span>B</span>
            <strong>{{ moduleData.boss_problem.title }}</strong>
            <small>Boss</small>
          </RouterLink>
        </div>
      </section>

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
  progress,
  roadmapModules,
  previousLesson,
  nextLesson,
  nextLessonUnlocked,
  isLessonUnlocked,
  lessonNavTarget,
  prefetchLesson,
  prefetchBossProblem,
  blockLockedLessonNavigation,
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

/* Lesson navigator (shared styling with LessonPage) */
.lesson-navigator {
  display: grid;
  gap: var(--space-2);
  border-bottom: 1px solid var(--color-border);
  padding: var(--space-1) var(--space-1) var(--space-2);
}

.lesson-nav-heading {
  justify-content: space-between;
}

.lesson-nav-heading h2 {
  margin: 0;
  font-size: var(--font-md);
}

.lesson-nav-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 3px;
}

.lesson-nav-link {
  display: grid;
  grid-template-columns: 22px minmax(0, 1fr) auto;
  gap: var(--space-1);
  align-items: center;
  border: 1px solid transparent;
  border-radius: var(--radius-sm);
  background: var(--color-surface-muted);
  color: var(--color-text-muted);
  font-size: var(--font-xs);
  padding: 6px;
}

.lesson-nav-link:hover,
.lesson-nav-link.router-link-active {
  border-color: var(--color-primary);
  background: var(--color-primary-soft);
  color: var(--color-primary);
}

.lesson-nav-link.is-locked {
  cursor: not-allowed;
  opacity: 0.7;
}

.is-disabled {
  cursor: not-allowed;
  opacity: 0.62;
}

.lesson-nav-link span,
.lesson-nav-link small {
  font-weight: 850;
}

.lesson-nav-link strong {
  overflow: hidden;
  color: var(--color-text);
  text-overflow: ellipsis;
  white-space: nowrap;
}

.lesson-nav-link.router-link-active strong {
  color: var(--color-primary);
}

.boss-link {
  border-color: #f1bf76;
  background: var(--color-warning-soft);
}

/* end lesson navigator */

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
