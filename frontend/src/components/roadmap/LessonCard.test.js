import { mount } from "@vue/test-utils";
import { describe, expect, it } from "vitest";

import LessonCard from "./LessonCard.vue";

const lesson = {
  id: "lesson_02_join_departments",
  module_id: "module_01_salary_comparison",
  title: "Join Employees to Departments",
  learning_objective: "Learn how INNER JOIN connects related tables.",
  concepts: ["INNER JOIN"],
  estimated_minutes: 15,
};

describe("LessonCard", () => {
  it("renders locked lessons as non-navigable rows", () => {
    const wrapper = mount(LessonCard, {
      props: {
        lesson,
        index: 1,
        status: "Not Started",
        locked: true,
      },
    });

    expect(wrapper.element.tagName).toBe("DIV");
    expect(wrapper.attributes("aria-disabled")).toBe("true");
    expect(wrapper.text()).toContain("Locked");
    expect(wrapper.find("a").exists()).toBe(false);
  });
});
