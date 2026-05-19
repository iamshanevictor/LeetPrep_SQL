import { apiRequest } from "./client";

export function fetchProblems() {
  return apiRequest("/problems");
}

export function fetchProblem(problemId) {
  return apiRequest(`/problems/${problemId}`);
}

export function runProblemQuery(problemId, query) {
  return apiRequest(`/problems/${problemId}/run`, {
    method: "POST",
    body: JSON.stringify({ query }),
  });
}

export function submitProblemQuery(problemId, query) {
  return apiRequest(`/problems/${problemId}/submit`, {
    method: "POST",
    body: JSON.stringify({ query }),
  });
}
