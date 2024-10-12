<script>
	export let message;
	export let author;
</script>

<span class={author}>
	{message}
</span>

<style>
	.human {
		color: black;
	}
	.ai {
		color: rgb(150, 4, 4);
	}
</style>

