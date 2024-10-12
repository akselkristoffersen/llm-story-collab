<script>
	import Message from './Message.svelte';
	let message;
	let messages = [];
	
			
	let waitingrOnResponse = false;
	function onSendMessage() {
		if (message.length > 0) {
		waitingrOnResponse = true;
		messages = [...messages, message];
		socket.send(message);
		message = "";
		}
	}

	let socket = undefined;
	let socketConnecting = false;
	let socketIsConnected = false;

	function connectToWebsocket() {
		if (socketConnecting || socketIsConnected) {
			return;
		}

		socketConnecting = true;
		socket = new WebSocket(import.meta.env.VITE_API_URL);
		
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
		display: flex;
		width: 100%;
		height: 100%;
		flex-direction: column;
		align-items: center;
		justify-content: center;
	}
</style>