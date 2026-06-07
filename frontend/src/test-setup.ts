import "@testing-library/jest-dom/vitest";
import { cleanup } from "@testing-library/svelte";
import { afterEach, vi } from "vitest";
import { writable } from "svelte/store";

// Auto-cleanup after each test to avoid memory leaks
afterEach(() => {
  cleanup();
});

// Mock SvelteKit $app/stores for page component tests
vi.mock("$app/stores", () => ({
  page: writable({
    params: {},
    url: new URL("http://localhost"),
    route: { id: "" },
  }),
  navigating: writable(null),
  session: writable(undefined),
  updated: writable(() => false),
  subPath: writable(""),
}));
