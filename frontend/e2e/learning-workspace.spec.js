import { expect, test } from "@playwright/test";

const moduleOne = {
  id: "module_01_salary_comparison",
  title: "Salary Comparison by Department",
  goal: "Learn aggregation, joins, CASE WHEN, CTEs, and company-vs-group comparisons.",
  order: 1,
  difficulty: "Beginner to Intermediate",
  concepts: ["INNER JOIN", "GROUP BY", "AVG", "CTE", "CASE WHEN"],
  lessons_count: 2,
  boss_problem_title: "Compare Department Average Salary vs Company Average",
};

const moduleOneDetail = {
  ...moduleOne,
  lessons: [
    {
      id: "lesson_01_group_by_avg",
      module_id: "module_01_salary_comparison",
      title: "Calculate Average Salary by Department",
      concepts: ["GROUP BY", "AVG"],
      estimated_minutes: 15,
      learning_objective: "Learn GROUP BY with AVG.",
      order: 1,
    },
    {
      id: "lesson_02_join_departments",
      module_id: "module_01_salary_comparison",
      title: "Join Employees to Departments",
      concepts: ["INNER JOIN"],
      estimated_minutes: 15,
      learning_objective: "Learn joins.",
      order: 2,
    },
  ],
  boss_problem: {
    id: "boss_problem",
    module_id: "module_01_salary_comparison",
    title: "Compare Department Average Salary vs Company Average",
  },
};

const lessonOne = {
  id: "lesson_01_group_by_avg",
  module_id: "module_01_salary_comparison",
  type: "tutorial_practice",
  title: "Calculate Average Salary by Department",
  concepts: ["GROUP BY", "AVG"],
  learning_objective: "Learn GROUP BY with AVG.",
  tutorial: {
    explanation: "GROUP BY creates one output row per group.",
    syntax: "SELECT department_id, AVG(salary) FROM employees GROUP BY department_id;",
    mental_model: "AVG runs inside each group.",
  },
  schema: [
    {
      table_name: "employees",
      columns: {
        employee_id: "INTEGER",
        employee_name: "TEXT",
        department_id: "INTEGER",
        salary: "INTEGER",
      },
    },
  ],
  seed_data: {
    employees: [
      [1, "Alice", 1, 60000],
      [2, "Bob", 1, 70000],
    ],
  },
  guided_example: {
    prompt: "Find average salary.",
    solution_query:
      "SELECT department_id, AVG(salary) AS avg_salary FROM employees GROUP BY department_id;",
    explanation: "Group first, then aggregate.",
  },
  practice: {
    prompt: "Find total salary by department.",
    order_matters: false,
  },
  expected_result: {
    columns: ["department_id", "total_salary"],
    rows: [[1, 130000]],
  },
  hints: ["Start with department_id."],
};

test.beforeEach(async ({ page }) => {
  await page.route("**/api/roadmap", async (route) => {
    await route.fulfill({
      json: {
        title: "Roadmap to Advanced SQL Interview Problems",
        description: "Mock roadmap",
        modules: [moduleOne],
      },
    });
  });

  await page.route("**/api/modules/module_01_salary_comparison", async (route) => {
    await route.fulfill({ json: { module: moduleOneDetail } });
  });

  await page.route(
    "**/api/modules/module_01_salary_comparison/lessons/lesson_01_group_by_avg",
    async (route) => {
      await route.fulfill({ json: { lesson: lessonOne } });
    },
  );

  await page.route("**/api/problems", async (route) => {
    await route.fulfill({ json: { problems: [] } });
  });
});

test("roadmap opens module detail", async ({ page }) => {
  await page.goto("/roadmap");

  await expect(page.getByRole("heading", { name: "SQL Learning Roadmap" })).toBeVisible();
  await page.getByRole("link", { name: /Salary Comparison by Department/ }).first().click();

  await expect(page).toHaveURL(/module_01_salary_comparison/);
  await expect(page.getByRole("heading", { name: "Lessons" })).toBeVisible();
});

test("locked lesson rows do not navigate", async ({ page }) => {
  await page.goto("/roadmap/module_01_salary_comparison");

  await expect(page.getByText("Join Employees to Departments")).toBeVisible();
  await page.getByText("Join Employees to Departments").click();

  await expect(page).toHaveURL(/module_01_salary_comparison$/);
  await expect(page.getByText("Locked").first()).toBeVisible();
});

test("lesson workspace shows tutorial, editor, and schema", async ({ page }) => {
  await page.goto(
    "/roadmap/module_01_salary_comparison/lessons/lesson_01_group_by_avg",
  );

  await expect(
    page.getByRole("heading", { name: "Calculate Average Salary by Department" }).first(),
  ).toBeVisible();
  await expect(page.getByLabel("SQL query editor")).toBeVisible();
  await expect(page.getByRole("heading", { name: "Schema" })).toBeVisible();
});
