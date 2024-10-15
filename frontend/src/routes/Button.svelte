<script>
    export let hidden;
    export let styleType = 'connect'; // 'connect' or 'disconnect'
</script>

<button
    class="button {styleType}"
    on:click
    {hidden}
    >
    <slot></slot>
</button>

<style lang="scss">
    .button {
        color: var(--bright-text-color);
		border: none;
		padding: 15px 30px;
		margin-top: 15px;
		font-size: 18px;
		font-weight: 600;
		border-radius: 9px;
		cursor: pointer;
		transition: background-color 0.1s ease;
    }

    .connect {
        background-color: var(--connect-color);
    }

    .disconnect {
        background-color: var(--disconnect-color);
    }

    .button:hover {
		filter:	brightness(92%);
	}

	.button:active {
		filter:	brightness(92%);
		transform: scale(0.98);
	}
</style>