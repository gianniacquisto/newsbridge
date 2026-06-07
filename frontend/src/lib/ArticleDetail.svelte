<script lang="ts">
  import { createEventDispatcher } from "svelte";

  export let article: {
    id: number;
    url: string;
    title: string;
    translated_title: string | null;
    source_name?: string;
    published_at?: string;
    content: string;
    source_language?: string;
    created_at: string;
    translation: {
      id: number;
      target_language: string;
      translated_content: string;
      status: string;
    } | null;
  } | null = null;

  export let loading = false;
  export let error: string | null = null;
  export let translating = false;

  const dispatch = createEventDispatcher<{ type: "translate" }>();

  function handleTranslate() {
    dispatch("translate");
  }
</script>

{#if loading}
  <div class="loading">
    <div class="spinner"></div>
    <p>Loading article...</p>
  </div>
{:else if error}
  <div class="error">
    <p>{error}</p>
  </div>
{:else if article}
  <article>
    <header>
      <h1>{article.translated_title || article.title}</h1>
      <div class="meta">
        <span class="source">{article.source_name}</span>
        <span class="time">{new Date(article.created_at).toLocaleDateString()}</span>
        {#if article.source_language}
          <span class="lang-badge">{article.source_language}</span>
        {/if}
      </div>
    </header>

    <div class="content">
      {#if article.translation}
        <p>{article.translation.translated_content}</p>
      {:else}
        <p>{article.content}</p>
      {/if}
    </div>

    <footer>
      <a href={article.url} target="_blank">Read original article →</a>
    </footer>

    {#if !article.translation && !translating}
      <button on:click={handleTranslate} disabled={translating}>
        Translate
      </button>
    {/if}

    {#if translating}
      <div class="translating">
        <div class="spinner"></div>
        <p>Translating...</p>
      </div>
    {/if}
  </article>
{/if}

<style>
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

  article {
    background: #fff;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 1.5rem;
  }

  h1 {
    font-size: 1.5rem;
    margin: 0 0 0.5rem;
  }

  .meta {
    display: flex;
    gap: 0.5rem;
    align-items: center;
    font-size: 0.85rem;
    color: #666;
    margin-bottom: 1rem;
  }

  .source {
    font-weight: 600;
    color: #006d77;
  }

  .lang-badge {
    background: #f0f0f0;
    padding: 0.15rem 0.5rem;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 600;
  }

  .content {
    line-height: 1.7;
    margin-bottom: 1.5rem;
    white-space: pre-wrap;
  }

  footer a {
    color: #006d77;
    font-weight: 600;
    text-decoration: none;
  }

  footer a:hover {
    text-decoration: underline;
  }

  button {
    background: #006d77;
    color: #fff;
    border: none;
    padding: 0.6rem 1.2rem;
    border-radius: 6px;
    font-weight: 600;
    cursor: pointer;
    margin-top: 1rem;
  }

  button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .translating {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-top: 1rem;
    color: #666;
  }
</style>
