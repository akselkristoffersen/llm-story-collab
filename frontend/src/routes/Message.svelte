<script>
	export let message;
	export let author = "";
</script>

<span class={author}>
	{message}
</span>

<style>
	.ai {
		font-weight: 600;
		color: var(--ai-text-color);
	}
</style>

