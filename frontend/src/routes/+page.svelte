<script lang="ts">
  import { getArticles } from "$lib/api";

  let articles: Article[] = [];
  let loading = true;
  let error: string | null = null;

  interface Article {
    id: number;
    title: string;
    source_id: number;
    source_name?: string;
    published_at?: string;
    source_language?: string;
    created_at: string;
  }

  onMount(async () => {
    try {
      articles = await getArticles();
    } catch (e) {
      error = e instanceof Error ? e.message : "Failed to load articles";
    } finally {
      loading = false;
    }
  });

  function timeAgo(dateStr: string): string {
    const diff = Date.now() - new Date(dateStr).getTime();
    const mins = Math.floor(diff / 60000);
    if (mins < 60) return `${mins}m ago`;
    const hours = Math.floor(mins / 60);
    if (hours < 24) return `${hours}h ago`;
    const days = Math.floor(hours / 24);
    return `${days}d ago`;
  }
</script>

<div class="container">
  <header>
    <h1>Newsbridge</h1>
    <p class="subtitle">Belgian news, translated to your language</p>
  </header>

  {#if loading}
    <div class="loading">
      <div class="spinner"></div>
      <p>Loading articles...</p>
    </div>
  {:else if error}
    <div class="error">
      <p>⚠️ {error}</p>
    </div>
  {:else if articles.length === 0}
    <div class="empty">
      <p>No articles yet. The RSS poller is fetching feeds...</p>
    </div>
  {:else}
    <div class="article-list">
      {#each articles as article (article.id)}
        <a href="/article/{article.id}" class="article-card">
          <div class="card-header">
            <span class="source">{article.source_name}</span>
            <span class="time">{timeAgo(article.created_at)}</span>
          </div>
          <h2 class="title">{article.title}</h2>
        </a>
      {/each}
    </div>
  {/if}
</div>

<style>
  .container {
    max-width: 720px;
    margin: 0 auto;
    padding: 2rem 1rem;
  }

  header {
    text-align: center;
    margin-bottom: 2rem;
  }

  header h1 {
    font-size: 2rem;
    font-weight: 700;
    margin: 0;
  }

  .subtitle {
    color: #666;
    margin: 0.5rem 0 0;
  }

  .loading, .error, .empty {
    text-align: center;
    padding: 3rem;
    color: #666;
  }

  .spinner {
    width: 32px;
    height: 32px;
    border: 3px solid #e0e0e0;
    border-top-color: #333;
    border-radius: 50%;
    margin: 0 auto 1rem;
    animation: spin 0.8s linear infinite;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  .article-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .article-card {
    display: block;
    padding: 1rem 1.25rem;
    background: #fff;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    text-decoration: none;
    color: inherit;
    transition: box-shadow 0.15s ease, border-color 0.15s ease;
  }

  .article-card:hover {
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    border-color: #bbb;
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.35rem;
  }

  .source {
    font-size: 0.8rem;
    font-weight: 600;
    color: #006d77;
    text-transform: uppercase;
    letter-spacing: 0.03em;
  }

  .time {
    font-size: 0.8rem;
    color: #999;
  }

  .title {
    font-size: 1.05rem;
    font-weight: 600;
    margin: 0;
    line-height: 1.4;
  }
</style>
