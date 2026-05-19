import { createRouter, createWebHistory } from "vue-router";

import DashboardPage from "../pages/DashboardPage.vue";
import BossProblemPage from "../pages/BossProblemPage.vue";
import LessonPage from "../pages/LessonPage.vue";
import ModulePage from "../pages/ModulePage.vue";
import ProblemDetailPage from "../pages/ProblemDetailPage.vue";
import ProblemListPage from "../pages/ProblemListPage.vue";
import RoadmapPage from "../pages/RoadmapPage.vue";

const routes = [
  {
    path: "/",
    name: "dashboard",
    component: DashboardPage,
  },
  {
    path: "/problems",
    name: "problems",
    component: ProblemListPage,
  },
  {
    path: "/roadmap",
    name: "roadmap",
    component: RoadmapPage,
  },
  {
    path: "/roadmap/:moduleId",
    name: "roadmap-module",
    component: ModulePage,
  },
  {
    path: "/roadmap/:moduleId/lessons/:lessonId",
    name: "roadmap-lesson",
    component: LessonPage,
  },
  {
    path: "/roadmap/:moduleId/boss",
    name: "roadmap-boss",
    component: BossProblemPage,
  },
  {
    path: "/problems/:id",
    name: "problem-detail",
    component: ProblemDetailPage,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
