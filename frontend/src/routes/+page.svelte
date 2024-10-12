<script>
	import Message from './Message.svelte';
	let message;
	let messages = [];
	let socket = undefined;
	let socketConnecting = false;
	let socketIsConnected = false;
	let waitingrOnResponse = false;
	
	function connectToWebsocket() {
		if (socketConnecting || socketIsConnected) {
			return;
		}

		socketConnecting = true;
		socket = new WebSocket(import.meta.env.VITE_API_URL);
		if (socket.CLOSED) {
			socketConnecting = false;
		}

		socket.onopen = (event) => {
			socketIsConnected = true;
			socketConnecting = false;
		}

		socket.onmessage = (event) => {
			messages = [...messages, event.data];
			waitingrOnResponse = false;
		};

		socket.onclose = (event) => {
			socketConnecting = false;
			socketIsConnected = false;
			messages = [];
			waitingrOnResponse = false;
		}
	}

	function disconnectFromWebsocket() {
		socket.close();
	}

	function onSendMessage() {
		if (message.length > 0) {
			waitingrOnResponse = true;
			messages = [...messages, message];
			socket.send(message);
			message = "";
		}
	}

</script>

<div class="wrapper">

<h1>Write history with AI</h1>

<button on:click={connectToWebsocket} hidden={socketConnecting || socketIsConnected}>
	Connect
</button>

{#if socketIsConnected}
<p>
	{#each messages as message, i}
		<Message {message} author={i % 2 == 1 ? "human" :  "ai" } />
	{/each}
</p>
<form>
	<input
		type="text"
		spellcheck="true"
		disabled={waitingrOnResponse}
		bind:value={message}
	/>
	<input type="submit" on:click={onSendMessage} disabled={waitingrOnResponse} hidden/>
</form>
{/if}

<button on:click={disconnectFromWebsocket} hidden={!(socketConnecting || socketIsConnected)}>
	Disconnect
</button>

</div>


<style>
	.wrapper {
		width: 100vw;
        height: 100vh;
        height: 100dvh;
        display: flex;
        flex-direction: column;
		align-items: center;
        overflow-y: auto;
        overflow-x: hidden;
	}
</style>