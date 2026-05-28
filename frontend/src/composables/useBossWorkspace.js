import { computed, onMounted, onUnmounted, ref, watch } from "vue";
import { useRoute } from "vue-router";

import {
  fetchBossProblem,
  fetchModule,
  fetchRoadmap,
  runBossQuery,
  submitBossQuery,
} from "../api/roadmap";
import {
  getBossKey,
  getDraftQuery,
  isBossUnlocked,
  loadProgress,
  markBossComplete,
  saveDraftQuery,
  setLastVisited,
  subscribeProgress,
} from "../services/progressStorage";

export function useBossWorkspace() {
  const route = useRoute();
  const bossProblem = ref(null);
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

  const contentKey = computed(() => getBossKey(route.params.moduleId));
  const bossUnlocked = computed(() =>
    moduleData.value
      ? isBossUnlocked(moduleData.value, progress.value, roadmapModules.value)
      : false,
  );
  const nextIncompleteLesson = computed(() =>
    (moduleData.value?.lessons || []).find(
      (lesson) => !progress.value.completedLessons[`${route.params.moduleId}/${lesson.id}`],
    ),
  );

  onMounted(async () => {
    unsubscribeProgress = subscribeProgress((nextProgress) => {
      progress.value = nextProgress;
    });
    await loadBossPage();
  });

  onUnmounted(() => {
    unsubscribeProgress?.();
  });

  watch(
    () => route.params.moduleId,
    async () => {
      await loadBossPage();
    },
  );

  watch(query, (nextQuery) => {
    if (bossUnlocked.value) {
      saveDraftQuery(contentKey.value, nextQuery);
    }
  });

  async function loadBossPage() {
    isLoading.value = true;
    errorMessage.value = "";
    bossProblem.value = null;
    query.value = "";
    userResult.value = null;
    expectedResult.value = null;
    feedback.value = { status: "neutral", message: "" };

    try {
      const [roadmap, moduleResponse] = await Promise.all([
        fetchRoadmap(),
        fetchModule(route.params.moduleId),
      ]);
      roadmapModules.value = roadmap.modules || [];
      moduleData.value = moduleResponse.module;

      if (!bossUnlocked.value) {
        return;
      }

      const data = await fetchBossProblem(route.params.moduleId);
      bossProblem.value = data.boss_problem;
      query.value = getDraftQuery(contentKey.value);
      setLastVisited({
        type: "boss",
        moduleId: route.params.moduleId,
        title: data.boss_problem.title,
        path: route.fullPath,
      });
    } catch (error) {
      errorMessage.value = error.message;
    } finally {
      isLoading.value = false;
    }
  }

  async function runQuery() {
    if (!bossUnlocked.value) {
      return;
    }

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
    if (!bossUnlocked.value) {
      return;
    }

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

      if (data.is_correct) {
        markBossComplete(route.params.moduleId);
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

  return {
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
  };
}
