<script lang="ts">
  import { page } from "$app/stores";
  import { getArticle, translateArticle } from "$lib/api";
  import ArticleDetail from "$lib/ArticleDetail.svelte";

  let article: any = null;
  let loading = true;
  let error: string | null = null;
  let translating = false;

  $: if ($page?.params?.id) {
    const id = Number($page.params.id);
    loadArticle(id);
  }

  async function loadArticle(id: number) {
    try {
      article = await getArticle(id);
    } catch (e) {
      error = e instanceof Error ? e.message : "Failed to load article";
    } finally {
      loading = false;
    }
  }

  async function handleTranslate() {
    if (!article) return;
    translating = true;
    try {
      await translateArticle(article.id);
      article = await getArticle(article.id);
    } catch (e) {
      error = e instanceof Error ? e.message : "Translation failed";
    } finally {
      translating = false;
    }
  }
</script>

<ArticleDetail
  {article}
  {loading}
  {error}
  {translating}
  on:translate={handleTranslate}
/>
