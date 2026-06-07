import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/svelte";
import { tick } from "svelte";
import ArticleDetail from "./ArticleDetail.svelte";

describe("ArticleDetail", () => {
  const baseArticle = {
    id: 1,
    url: "https://example.com/article",
    title: "Belgische verkiezingen",
    translated_title: "Belgian elections",
    source_name: "De Standaard",
    published_at: "2026-06-07T10:00:00Z",
    content: "Original content text here",
    source_language: "nl",
    created_at: "2026-06-07T10:00:00Z",
    translation: null,
  };

  it("displays translated content when translation exists", async () => {
    const article = {
      ...baseArticle,
      translation: {
        id: 1,
        target_language: "en",
        translated_content: "This is the translated content",
        status: "completed",
      },
    };

    render(ArticleDetail, { props: { article } });

    await waitFor(() => {
      expect(screen.getByRole("heading", { name: /Belgian elections/i })).toBeInTheDocument();
    });

    expect(screen.getByText(/This is the translated content/i)).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /Translate/i })).not.toBeInTheDocument();
  });

  it("falls back to original content and shows language badge when no translation", async () => {
    render(ArticleDetail, { props: { article: baseArticle } });

    await waitFor(() => {
      expect(screen.getByText(/Original content text here/i)).toBeInTheDocument();
    });

    expect(screen.getByText(/nl/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Translate/i })).toBeInTheDocument();
  });

  it("emits translate event when translate button is clicked", async () => {
    const fn = vi.fn();
    const { component } = render(ArticleDetail, { props: { article: baseArticle } });

    component.$on("translate", fn);
    await fireEvent.click(screen.getByRole("button", { name: /Translate/i }));

    expect(fn).toHaveBeenCalledTimes(1);
  });

  it("shows loading state when loading is true", () => {
    render(ArticleDetail, { props: { loading: true } });

    expect(screen.getByText(/Loading article/i)).toBeInTheDocument();
    expect(screen.queryByRole("heading")).not.toBeInTheDocument();
  });

  it("shows error message when error is set", () => {
    render(ArticleDetail, { props: { error: "Failed to load article" } });

    expect(screen.getByText("Failed to load article")).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /Translate/i })).not.toBeInTheDocument();
  });

  it("shows translating state while translating", () => {
    render(ArticleDetail, {
      props: { article: baseArticle, translating: true },
    });

    expect(screen.getByText(/Translating/i)).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /Translate/i })).not.toBeInTheDocument();
  });
});
