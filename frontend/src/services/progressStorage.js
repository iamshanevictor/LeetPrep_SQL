const STORAGE_KEY = "leetprep-sql-progress-v1";
const PROGRESS_EVENT = "leetprep-sql-progress-updated";

const EMPTY_PROGRESS = {
  version: 1,
  completedLessons: {},
  completedBossProblems: {},
  draftQueries: {},
  lastVisited: null,
  practiceDates: [],
};

export function loadProgress() {
  if (!canUseStorage()) {
    return cloneProgress(EMPTY_PROGRESS);
  }

  try {
    const stored = window.localStorage.getItem(STORAGE_KEY);
    if (!stored) {
      return cloneProgress(EMPTY_PROGRESS);
    }

    return normalizeProgress(JSON.parse(stored));
  } catch {
    return cloneProgress(EMPTY_PROGRESS);
  }
}

export function saveDraftQuery(contentKey, query) {
  updateProgress((progress) => {
    if (query?.trim()) {
      progress.draftQueries[contentKey] = query;
    } else {
      delete progress.draftQueries[contentKey];
    }
  });
}

export function getDraftQuery(contentKey) {
  return loadProgress().draftQueries[contentKey] || "";
}

export function setLastVisited(location) {
  updateProgress((progress) => {
    progress.lastVisited = {
      ...location,
      updatedAt: new Date().toISOString(),
    };
  });
}

export function markLessonComplete(moduleId, lessonId) {
  updateProgress((progress) => {
    progress.completedLessons[getLessonKey(moduleId, lessonId)] = new Date().toISOString();
    recordPracticeDate(progress);
  });
}

export function markBossComplete(moduleId) {
  updateProgress((progress) => {
    progress.completedBossProblems[moduleId] = new Date().toISOString();
    recordPracticeDate(progress);
  });
}

export function getLessonStatus(moduleId, lessonId, progress = loadProgress()) {
  return progress.completedLessons[getLessonKey(moduleId, lessonId)]
    ? "Completed"
    : "Not Started";
}

export function getBossStatus(moduleId, progress = loadProgress()) {
  return progress.completedBossProblems[moduleId] ? "Completed" : "Not Started";
}

export function getModuleStatus(module, progress = loadProgress()) {
  const lessons = module?.lessons || [];
  const completedLessons = lessons.filter((lesson) =>
    progress.completedLessons[getLessonKey(module.id, lesson.id)],
  ).length;
  const bossCompleted = Boolean(progress.completedBossProblems[module?.id]);

  if ((lessons.length > 0 && completedLessons === lessons.length) && bossCompleted) {
    return "Completed";
  }

  if (
    completedLessons > 0 ||
    bossCompleted ||
    progress.lastVisited?.moduleId === module?.id
  ) {
    return "In Progress";
  }

  return "Not Started";
}

export function getRoadmapModuleStatus(module, progress = loadProgress()) {
  return getRoadmapModuleStatusWithModules(module, [], progress);
}

export function getRoadmapModuleStatusWithModules(module, modules = [], progress = loadProgress()) {
  if (!isRoadmapModuleUnlocked(module, modules, progress)) {
    return "Locked";
  }

  const lessonCount = module?.lessons_count || 0;
  const completedLessons = Object.keys(progress.completedLessons).filter((key) =>
    key.startsWith(`${module.id}/`),
  ).length;
  const bossCompleted = Boolean(progress.completedBossProblems[module?.id]);

  if (lessonCount > 0 && completedLessons >= lessonCount && bossCompleted) {
    return "Completed";
  }

  if (
    completedLessons > 0 ||
    bossCompleted ||
    progress.lastVisited?.moduleId === module?.id
  ) {
    return "In Progress";
  }

  return "Not Started";
}

export function isRoadmapModuleUnlocked(module, modules = [], progress = loadProgress()) {
  if (!module) {
    return false;
  }

  const sortedModules = [...modules].sort((first, second) => {
    return (first.order || 0) - (second.order || 0);
  });

  if (!sortedModules.length) {
    return (module.order || 1) <= 1;
  }

  const moduleIndex = sortedModules.findIndex((item) => item.id === module.id);

  if (moduleIndex === -1) {
    return (module.order || 1) <= 1;
  }

  if (moduleIndex === 0) {
    return true;
  }

  const previousModule = sortedModules[moduleIndex - 1];
  return isRoadmapModuleComplete(previousModule, progress);
}

export function isLessonUnlocked(module, lessonId, progress = loadProgress(), modules = []) {
  if (!module || !isRoadmapModuleUnlocked(module, modules, progress)) {
    return false;
  }

  const lessons = module.lessons || [];
  const lessonIndex = lessons.findIndex((lesson) => lesson.id === lessonId);

  if (lessonIndex <= 0) {
    return lessonIndex === 0;
  }

  const previousLesson = lessons[lessonIndex - 1];
  return Boolean(progress.completedLessons[getLessonKey(module.id, previousLesson.id)]);
}

export function isBossUnlocked(module, progress = loadProgress(), modules = []) {
  if (!module || !isRoadmapModuleUnlocked(module, modules, progress)) {
    return false;
  }

  const lessons = module.lessons || [];
  return lessons.length > 0 && lessons.every((lesson) =>
    Boolean(progress.completedLessons[getLessonKey(module.id, lesson.id)]),
  );
}

export function getProgressSummary(modules = [], progress = loadProgress()) {
  return {
    completedLessons: Object.keys(progress.completedLessons).length,
    completedBossProblems: Object.keys(progress.completedBossProblems).length,
    currentStreak: calculateCurrentStreak(progress.practiceDates),
    lastVisited: progress.lastVisited,
    completedModules: modules.filter((module) => isRoadmapModuleComplete(module, progress)).length,
  };
}

export function subscribeProgress(listener) {
  if (typeof window === "undefined") {
    return () => {};
  }

  const notify = () => listener(loadProgress());
  const onStorage = (event) => {
    if (event.key === STORAGE_KEY) {
      notify();
    }
  };

  window.addEventListener(PROGRESS_EVENT, notify);
  window.addEventListener("storage", onStorage);

  return () => {
    window.removeEventListener(PROGRESS_EVENT, notify);
    window.removeEventListener("storage", onStorage);
  };
}

export function getLessonKey(moduleId, lessonId) {
  return `${moduleId}/${lessonId}`;
}

export function getBossKey(moduleId) {
  return `${moduleId}/boss`;
}

function updateProgress(mutator) {
  const progress = loadProgress();
  mutator(progress);
  persistProgress(progress);
}

function isRoadmapModuleComplete(module, progress) {
  const lessonCount = module?.lessons_count || 0;
  const completedLessons = Object.keys(progress.completedLessons).filter((key) =>
    key.startsWith(`${module?.id}/`),
  ).length;
  const bossCompleted = Boolean(progress.completedBossProblems[module?.id]);

  return lessonCount > 0 && completedLessons >= lessonCount && bossCompleted;
}

function persistProgress(progress) {
  if (!canUseStorage()) {
    return;
  }

  try {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(normalizeProgress(progress)));
    window.dispatchEvent(new CustomEvent(PROGRESS_EVENT));
  } catch {
    // Some browsers disable storage in strict privacy modes. In that case,
    // the app keeps working; progress just will not persist.
  }
}

function normalizeProgress(progress) {
  return {
    ...cloneProgress(EMPTY_PROGRESS),
    ...(progress || {}),
    completedLessons: progress?.completedLessons || {},
    completedBossProblems: progress?.completedBossProblems || {},
    draftQueries: progress?.draftQueries || {},
    practiceDates: Array.isArray(progress?.practiceDates) ? progress.practiceDates : [],
  };
}

function recordPracticeDate(progress) {
  const today = getTodayKey();
  if (!progress.practiceDates.includes(today)) {
    progress.practiceDates.push(today);
    progress.practiceDates.sort();
  }
}

function calculateCurrentStreak(practiceDates = []) {
  const dates = new Set(practiceDates);
  let streak = 0;
  const cursor = new Date();

  while (dates.has(toDateKey(cursor))) {
    streak += 1;
    cursor.setDate(cursor.getDate() - 1);
  }

  return streak;
}

function getTodayKey() {
  return toDateKey(new Date());
}

function toDateKey(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function cloneProgress(progress) {
  return JSON.parse(JSON.stringify(progress));
}

function canUseStorage() {
  try {
    return typeof window !== "undefined" && Boolean(window.localStorage);
  } catch {
    return false;
  }
}
