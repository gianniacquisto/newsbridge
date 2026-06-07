const API_BASE = import.meta.env.VITE_API_URL || "/api";

interface Article {
  id: number;
  url: string;
  title: string;
  source_id: number;
  source_name?: string;
  published_at?: string;
  content?: string;
  source_language?: string;
  created_at: string;
}

interface ArticleWithTranslation extends Article {
  translation?: {
    id: number;
    article_id: number;
    target_language: string;
    translated_content?: string;
    status: string;
    created_at: string;
    completed_at?: string;
  };
}

async function fetchJSON<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function getArticles() {
  return fetchJSON<Article[]>("/articles");
}

export async function getArticle(id: number) {
  return fetchJSON<ArticleWithTranslation>(`/articles/${id}`);
}

export async function translateArticle(id: number) {
  const res = await fetch(`${API_BASE}/articles/${id}/translate`, {
    method: "POST",
  });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function getSources() {
  return fetchJSON<{ id: number; name: string; url: string }[]>("/sources");
}
