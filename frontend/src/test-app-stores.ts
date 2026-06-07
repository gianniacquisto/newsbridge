import { writable } from "svelte/store";

export const page = writable({
  params: {},
  url: new URL("http://localhost"),
  route: { id: "" },
});

export const navigating = writable<null | { from: any; to: any }>(null);
export const session = writable<Record<string, unknown> | undefined>(undefined);
export const updated = writable(false);
export const subPath = writable("");
