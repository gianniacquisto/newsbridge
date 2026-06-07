import { describe, it, expect, vi, beforeEach } from "vitest";
import { getArticles } from "./api";

describe("getArticles", () => {
  beforeEach(() => {
    vi.resetAllMocks();
  });

  it("fetches articles from the API and returns the response body", async () => {
    const mockArticles = [
      {
        id: 1,
        title: "Original Titel",
        translated_title: "Translated Title",
        source_id: 1,
        source_name: "De Standaard",
        published_at: "2026-06-07T10:00:00Z",
        source_language: "nl",
        content: "Some content",
        created_at: "2026-06-07T10:00:00Z",
      },
    ];

    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockArticles),
    });

    const result = await getArticles();

    expect(fetch).toHaveBeenCalledWith("/api/articles");
    expect(result).toEqual(mockArticles);
  });

  it("throws when the API returns a non-200 response", async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 500,
    });

    await expect(getArticles()).rejects.toThrow("API error: 500");
  });
});
