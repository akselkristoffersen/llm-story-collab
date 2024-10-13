<script>
	import Message from './Message.svelte';
	let message = "";
	let messages = [];
	let socket = undefined;
	let socketConnecting = false;
	let socketIsConnected = false;
	let awaitingResponse = false;
	
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
			awaitingResponse = false;
		};

		socket.onclose = (event) => {
			socketConnecting = false;
			socketIsConnected = false;
			messages = [];
			awaitingResponse = false;
		}
	}

	function disconnectFromWebsocket() {
		socket.close();
	}

	function onSendMessage() {
		if (message.length > 0) {
			awaitingResponse = true;
			messages = [...messages, message];
			socket.send(message);
			message = "";
		}
	}

</script>

<div class="wrapper">

<h1>Write history with AI</h1>

<button class="button-connect" on:click={connectToWebsocket} hidden={socketConnecting || socketIsConnected}>
	Connect
</button>

{#if socketIsConnected}
<p class="history-field">
	{#each messages as message, i}<Message {message} author={i % 2 == 0 ? "human" :  "ai" }/>{/each}{message}
	<span class="ai-thinking" hidden={!awaitingResponse}>...AI is thinking </span>
</p>
<form>
	<input class="input-text"
		type="text"
		spellcheck="true"
		disabled={awaitingResponse}
		placeholder="Input text"
		bind:value={message}
	/>
	<input type="submit" on:click={onSendMessage} disabled={awaitingResponse}/>
</form>
{/if}

<button class="button-connect" on:click={disconnectFromWebsocket} hidden={!(socketConnecting || socketIsConnected)}>
	Disconnect
</button>

</div>


<style lang="scss">
	.wrapper {
		width: 100vw;
        height: 100vh;
        height: 100dvh;
		max-width: 800px;
        display: flex;
        flex-direction: column;
		align-items: center;
        overflow-y: auto;
        overflow-x: hidden;
	}

	h1 {
		width: 70%;
		text-align: center;
	}

	.history-field {
		width: 80%;
		min-height: 100px;
		background-color: white;
		border: 2px solid rgb(208, 208, 208);
		border-radius: 4px;
		padding: 4px 7px;
		word-wrap: break-word;
		overflow-wrap: break-word;
		word-break: break-word;
		white-space: normal;
	}

	.ai-thinking {
		color: lightgray;
	}

	.input-text {
		border: 1px solid rgb(174, 174, 174);
		padding: 4px 7px;
		border-radius: 4px;
		margin: 8px 4px;
	}

	.button-connect {
		background-color: #4CAF50;
		color: white;
		border: none;    
		padding: 15px 30px;
		font-size: 18px;
		font-weight: bold;
		border-radius: 10px;
		cursor: pointer;
		transition: background-color 0.1s ease;
	}

	.button-connect:hover {
		background-color: #45a049;
	}

	.button-connect:active {
		background-color: #388E3C;
		transform: scale(0.98);
	}
</style>