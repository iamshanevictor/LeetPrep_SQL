import { apiRequest } from "./client";

export function fetchRoadmap() {
  return apiRequest("/roadmap");
}

export function fetchModules() {
  return apiRequest("/modules");
}

export function fetchModule(moduleId) {
  return apiRequest(`/modules/${moduleId}`);
}

export function fetchLesson(moduleId, lessonId) {
  return apiRequest(`/modules/${moduleId}/lessons/${lessonId}`);
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
  return apiRequest(`/modules/${moduleId}/boss`);
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
