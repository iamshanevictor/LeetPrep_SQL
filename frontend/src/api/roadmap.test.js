import { beforeEach, describe, expect, it, vi } from "vitest";

import { apiRequest } from "./client";
import { clearRoadmapCache, fetchModule, fetchRoadmap } from "./roadmap";

vi.mock("./client", () => ({
  apiRequest: vi.fn(),
}));

describe("roadmap API cache", () => {
  beforeEach(() => {
    clearRoadmapCache();
    apiRequest.mockReset();
  });

  it("reuses successful roadmap requests", async () => {
    apiRequest.mockResolvedValueOnce({ modules: [] });

    await fetchRoadmap();
    await fetchRoadmap();

    expect(apiRequest).toHaveBeenCalledTimes(1);
    expect(apiRequest).toHaveBeenCalledWith("/roadmap");
  });

  it("invalidates failed roadmap requests so a retry can recover", async () => {
    apiRequest
      .mockRejectedValueOnce(new Error("Backend unavailable"))
      .mockResolvedValueOnce({ modules: [] });

    await expect(fetchRoadmap()).rejects.toThrow("Backend unavailable");
    await expect(fetchRoadmap()).resolves.toEqual({ modules: [] });

    expect(apiRequest).toHaveBeenCalledTimes(2);
  });

  it("invalidates failed module requests so a retry can recover", async () => {
    apiRequest
      .mockRejectedValueOnce(new Error("Module not found"))
      .mockResolvedValueOnce({ module: { id: "module_01_salary_comparison" } });

    await expect(fetchModule("module_01_salary_comparison")).rejects.toThrow(
      "Module not found",
    );
    await expect(fetchModule("module_01_salary_comparison")).resolves.toEqual({
      module: { id: "module_01_salary_comparison" },
    });

    expect(apiRequest).toHaveBeenCalledTimes(2);
  });
});
