<template>
  <section class="workspace-page">
    <LoadingState v-if="isLoading" class="workspace-state" message="Loading lesson..." />
    <ErrorState
      v-else-if="errorMessage"
      class="workspace-state"
      title="Could not load lesson"
      :message="errorMessage"
    />

    <div
      v-else
      class="dense-workspace"
      :class="{ 'has-lesson-nav': moduleData }"
    >
      <header class="workspace-topbar">
        <div class="crumbs">
          <RouterLink :to="`/roadmap/${route.params.moduleId}`">Module</RouterLink>
          <span>/</span>
          <strong>{{ lesson.title }}</strong>
        </div>
      </header>

      <section v-if="moduleData" class="lesson-navigator">
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
          <section v-if="!lessonUnlocked" class="lock-banner">
            <h2>Practice locked</h2>
            <p>{{ lockMessage }}</p>
          </section>

          <section class="practice-strip">
            <div>
              <h2>Practice</h2>
              <p>{{ lesson.practice.prompt }}</p>
            </div>
            <span class="badge">{{ lesson.practice.order_matters ? "Ordered" : "Any order" }}</span>
          </section>

          <section class="editor-section">
            <SqlEditor v-model="query" :disabled="!lessonUnlocked || isRunning || isSubmitting" />
            <div class="actions">
              <button
                class="button button-secondary"
                type="button"
                :disabled="!lessonUnlocked || isRunning || isSubmitting"
                @click="runQuery"
              >
                {{ isRunning ? "Running..." : "Run Query" }}
              </button>
              <button
                class="button button-primary"
                type="button"
                :disabled="!lessonUnlocked || isRunning || isSubmitting"
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
import { useLessonWorkspace } from "../composables/useLessonWorkspace";

const {
  route,
  lesson,
  moduleData,
  roadmapModules,
  query,
  userResult,
  expectedResult,
  feedback,
  isLoading,
  isRunning,
  isSubmitting,
  errorMessage,
  progress,
  previousLesson,
  nextLesson,
  nextLessonUnlocked,
  lessonUnlocked,
  lockMessage,
  isLessonUnlocked,
  prefetchBossProblem,
  prefetchLesson,
  runQuery,
  submitQuery,
  lessonNavTarget,
  blockLockedLessonNavigation,
} = useLessonWorkspace();
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

.dense-workspace.has-lesson-nav {
  grid-template-rows: 38px auto minmax(0, 1fr);
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
  justify-content: flex-start;
  gap: var(--space-2);
  position: relative;
  padding: 0 var(--space-2);
}

.crumbs,
.concept-list,
.result-header,
.lesson-nav-heading,
.lesson-nav-actions {
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
.practice-strip,
.lock-banner {
  display: grid;
  gap: var(--space-2);
  border-bottom: 1px solid var(--color-border);
  padding-bottom: var(--space-2);
}

.panel-section:last-child,
.result-section:last-child {
  border-bottom: 0;
}

.lock-banner {
  border: 1px solid var(--color-warning);
  border-radius: var(--radius-sm);
  background: var(--color-warning-soft);
  padding: var(--space-2);
}

.lock-banner h2,
.lock-banner p {
  margin: 0;
}

.lock-banner h2 {
  font-size: var(--font-md);
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
