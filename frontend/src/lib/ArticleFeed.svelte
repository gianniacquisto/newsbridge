<script lang="ts">
  export let articles: {
    id: number;
    title: string;
    translated_title?: string | null;
    source_id: number;
    source_name?: string;
    published_at?: string;
    source_language?: string;
    created_at: string;
  }[] = [];

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

{#if articles.length === 0}
  <div class="empty">
    <p>No articles yet.</p>
  </div>
{:else}
  <div class="article-list">
    {#each articles as article (article.id)}
      <a href="/article/{article.id}" class="article-card">
        <div class="card-header">
          <span class="source">{article.source_name}</span>
          <span class="time">{timeAgo(article.created_at)}</span>
        </div>
        <h2 class="title">{article.translated_title || article.title}</h2>
      </a>
    {/each}
  </div>
{/if}

<style>
  .empty {
    text-align: center;
    padding: 3rem;
    color: #666;
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
