import { createRouter, createWebHistory } from "vue-router";

import DashboardPage from "../pages/DashboardPage.vue";
import ProblemDetailPage from "../pages/ProblemDetailPage.vue";
import ProblemListPage from "../pages/ProblemListPage.vue";

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
