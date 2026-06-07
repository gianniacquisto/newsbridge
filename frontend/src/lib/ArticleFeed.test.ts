import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/svelte";
import ArticleFeed from "./ArticleFeed.svelte";

describe("ArticleFeed", () => {
  it("displays translated_title when available", () => {
    render(ArticleFeed, {
      props: {
        articles: [
          {
            id: 1,
            title: "Belgische verkiezingen",
            translated_title: "Belgian elections",
            source_id: 1,
            source_name: "De Standaard",
            created_at: "2026-06-07T10:00:00Z",
          },
        ],
      },
    });

    expect(screen.getByRole("heading", { name: /Belgian elections/i })).toBeInTheDocument();
  });

  it("falls back to original title when translated_title is null", () => {
    render(ArticleFeed, {
      props: {
        articles: [
          {
            id: 2,
            title: "Geen Vertaling",
            translated_title: null,
            source_id: 4,
            source_name: "Knack",
            created_at: "2026-06-07T09:00:00Z",
          },
        ],
      },
    });

    expect(screen.getByRole("heading", { name: /Geen Vertaling/i })).toBeInTheDocument();
  });

  it("shows empty message when no articles", () => {
    render(ArticleFeed, { props: { articles: [] } });

    expect(screen.getByText(/No articles yet/i)).toBeInTheDocument();
  });

  it("shows source name on each card", () => {
    render(ArticleFeed, {
      props: {
        articles: [
          {
            id: 1,
            title: "Test",
            translated_title: "Test EN",
            source_id: 1,
            source_name: "VRT NWS",
            created_at: "2026-06-07T10:00:00Z",
          },
        ],
      },
    });

    expect(screen.getByText("VRT NWS")).toBeInTheDocument();
  });

  it("links to article detail page", () => {
    render(ArticleFeed, {
      props: {
        articles: [
          {
            id: 42,
            title: "Test",
            translated_title: "Test EN",
            source_id: 1,
            source_name: "Le Soir",
            created_at: "2026-06-07T10:00:00Z",
          },
        ],
      },
    });

    const link = screen.getByRole("link", { name: /Test EN/i });
    expect(link).toHaveAttribute("href", "/article/42");
  });
});
