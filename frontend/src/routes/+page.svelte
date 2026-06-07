<script lang="ts">
  import { onMount } from "svelte";
  import { getArticles } from "$lib/api";
  import ArticleFeed from "$lib/ArticleFeed.svelte";

  interface Article {
    id: number;
    title: string;
    translated_title?: string | null;
    source_id: number;
    source_name?: string;
    published_at?: string;
    source_language?: string;
    created_at: string;
  }

  let articles: Article[] = [];
  let loading = true;
  let error: string | null = null;

  onMount(async () => {
    try {
      articles = await getArticles();
    } catch (e) {
      error = e instanceof Error ? e.message : "Failed to load articles";
    } finally {
      loading = false;
    }
  });
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
  {:else}
    <ArticleFeed {articles} />
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

  .loading, .error {
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
</style>
