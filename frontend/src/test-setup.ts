import "@testing-library/jest-dom/vitest";
import { cleanup } from "@testing-library/svelte";
import { afterEach } from "vitest";

// Auto-cleanup after each test to avoid memory leaks
afterEach(() => {
  cleanup();
});
