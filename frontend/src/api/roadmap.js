import { apiRequest } from "./client";

const cache = {
  roadmap: null,
  modules: new Map(),
  lessons: new Map(),
  bosses: new Map(),
};

export function fetchRoadmap() {
  if (!cache.roadmap) {
    cache.roadmap = apiRequest("/roadmap").catch((error) => {
      cache.roadmap = null;
      throw error;
    });
  }

  return cache.roadmap;
}

export function fetchModules() {
  return apiRequest("/modules");
}

export function fetchModule(moduleId) {
  if (!cache.modules.has(moduleId)) {
    cache.modules.set(
      moduleId,
      apiRequest(`/modules/${moduleId}`).catch((error) => {
        cache.modules.delete(moduleId);
        throw error;
      }),
    );
  }

  return cache.modules.get(moduleId);
}

export function fetchLesson(moduleId, lessonId) {
  const cacheKey = `${moduleId}/${lessonId}`;
  if (!cache.lessons.has(cacheKey)) {
    cache.lessons.set(
      cacheKey,
      apiRequest(`/modules/${moduleId}/lessons/${lessonId}`).catch((error) => {
        cache.lessons.delete(cacheKey);
        throw error;
      }),
    );
  }

  return cache.lessons.get(cacheKey);
}

export function runLessonQuery(moduleId, lessonId, query) {
  return apiRequest(`/modules/${moduleId}/lessons/${lessonId}/run`, {
    method: "POST",
    body: JSON.stringify({ query }),
  });
}

export function submitLessonQuery(moduleId, lessonId, query) {
  return apiRequest(`/modules/${moduleId}/lessons/${lessonId}/submit`, {
    method: "POST",
    body: JSON.stringify({ query }),
  });
}

export function fetchBossProblem(moduleId) {
  if (!cache.bosses.has(moduleId)) {
    cache.bosses.set(
      moduleId,
      apiRequest(`/modules/${moduleId}/boss`).catch((error) => {
        cache.bosses.delete(moduleId);
        throw error;
      }),
    );
  }

  return cache.bosses.get(moduleId);
}

export function runBossQuery(moduleId, query) {
  return apiRequest(`/modules/${moduleId}/boss/run`, {
    method: "POST",
    body: JSON.stringify({ query }),
  });
}

export function submitBossQuery(moduleId, query) {
  return apiRequest(`/modules/${moduleId}/boss/submit`, {
    method: "POST",
    body: JSON.stringify({ query }),
  });
}

export function prefetchModule(moduleId) {
  fetchModule(moduleId).catch(() => {});
}

export function prefetchLesson(moduleId, lessonId) {
  fetchLesson(moduleId, lessonId).catch(() => {});
}

export function prefetchBossProblem(moduleId) {
  fetchBossProblem(moduleId).catch(() => {});
}

export function clearRoadmapCache() {
  cache.roadmap = null;
  cache.modules.clear();
  cache.lessons.clear();
  cache.bosses.clear();
}
