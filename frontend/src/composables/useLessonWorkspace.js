import { computed, onMounted, onUnmounted, ref, watch } from "vue";
import { useRoute } from "vue-router";

import {
  fetchLesson,
  fetchModule,
  fetchRoadmap,
  prefetchBossProblem,
  prefetchLesson,
  runLessonQuery,
  submitLessonQuery,
} from "../api/roadmap";
import {
  getDraftQuery,
  getLessonKey,
  isLessonUnlocked,
  loadProgress,
  markLessonComplete,
  saveDraftQuery,
  setLastVisited,
  subscribeProgress,
} from "../services/progressStorage";

export function useLessonWorkspace() {
  const route = useRoute();
  const lesson = ref(null);
  const moduleData = ref(null);
  const roadmapModules = ref([]);
  const query = ref("");
  const userResult = ref(null);
  const expectedResult = ref(null);
  const feedback = ref({ status: "neutral", message: "" });
  const isLoading = ref(true);
  const isRunning = ref(false);
  const isSubmitting = ref(false);
  const errorMessage = ref("");
  const progress = ref(loadProgress());
  let unsubscribeProgress = null;

  const contentKey = computed(() =>
    getLessonKey(route.params.moduleId, route.params.lessonId),
  );
  const currentLessonIndex = computed(() =>
    (moduleData.value?.lessons || []).findIndex(
      (moduleLesson) => moduleLesson.id === route.params.lessonId,
    ),
  );
  const previousLesson = computed(() => {
    if (currentLessonIndex.value <= 0) {
      return null;
    }

    return moduleData.value.lessons[currentLessonIndex.value - 1];
  });
  const nextLesson = computed(() => {
    if (
      currentLessonIndex.value < 0 ||
      currentLessonIndex.value >= (moduleData.value?.lessons || []).length - 1
    ) {
      return null;
    }

    return moduleData.value.lessons[currentLessonIndex.value + 1];
  });
  const nextLessonUnlocked = computed(() =>
    nextLesson.value
      ? isLessonUnlocked(
          moduleData.value,
          nextLesson.value.id,
          progress.value,
          roadmapModules.value,
        )
      : false,
  );
  const lessonUnlocked = computed(() =>
    moduleData.value
      ? isLessonUnlocked(
          moduleData.value,
          route.params.lessonId,
          progress.value,
          roadmapModules.value,
        )
      : false,
  );
  const lockMessage = computed(() => {
    if (!moduleData.value) {
      return "Loading lesson requirements...";
    }

    if (currentLessonIndex.value > 0) {
      const previous = moduleData.value.lessons[currentLessonIndex.value - 1];
      return `Complete the previous lesson first: ${previous.title}.`;
    }

    return "Complete the previous module before practicing this lesson.";
  });

  onMounted(async () => {
    unsubscribeProgress = subscribeProgress((nextProgress) => {
      progress.value = nextProgress;
    });
    await loadRoadmapContext();
    await loadModuleContext();
  });

  onUnmounted(() => {
    unsubscribeProgress?.();
  });

  watch(
    () => [route.params.moduleId, route.params.lessonId],
    async () => {
      await loadLesson();
    },
    { immediate: true },
  );

  watch(
    () => route.params.moduleId,
    async () => {
      await loadRoadmapContext();
      await loadModuleContext();
    },
  );

  watch(query, (nextQuery) => {
    saveDraftQuery(contentKey.value, nextQuery);
  });

  async function loadModuleContext() {
    try {
      const data = await fetchModule(route.params.moduleId);
      moduleData.value = data.module;
    } catch {
      moduleData.value = null;
    }
  }

  async function loadRoadmapContext() {
    try {
      const roadmap = await fetchRoadmap();
      roadmapModules.value = roadmap.modules || [];
    } catch {
      roadmapModules.value = [];
    }
  }

  async function loadLesson() {
    isLoading.value = true;
    errorMessage.value = "";
    userResult.value = null;
    expectedResult.value = null;
    feedback.value = { status: "neutral", message: "" };

    try {
      const data = await fetchLesson(route.params.moduleId, route.params.lessonId);
      lesson.value = data.lesson;
      query.value = getDraftQuery(contentKey.value);
      setLastVisited({
        type: "lesson",
        moduleId: route.params.moduleId,
        lessonId: route.params.lessonId,
        title: data.lesson.title,
        path: route.fullPath,
      });
    } catch (error) {
      errorMessage.value = error.message;
    } finally {
      isLoading.value = false;
    }
  }

  async function runQuery() {
    if (!lessonUnlocked.value) {
      return;
    }

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
    if (!lessonUnlocked.value) {
      return;
    }

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

      if (data.is_correct) {
        markLessonComplete(route.params.moduleId, route.params.lessonId);
      }
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

  function lessonNavTarget(moduleLesson) {
    if (
      isLessonUnlocked(moduleData.value, moduleLesson.id, progress.value, roadmapModules.value)
    ) {
      return `/roadmap/${route.params.moduleId}/lessons/${moduleLesson.id}`;
    }

    return route.fullPath;
  }

  function blockLockedLessonNavigation(event, moduleLesson) {
    if (
      !isLessonUnlocked(moduleData.value, moduleLesson.id, progress.value, roadmapModules.value)
    ) {
      event.preventDefault();
    }
  }

  return {
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
  };
}
