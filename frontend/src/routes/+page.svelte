<script>
	import Message from './Message.svelte';
	import Button from './Button.svelte';

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
		awaitingResponse = true;
		messages = [...messages, message];
		socket.send(message);
		message = "";
	}

</script>

<div class="wrapper">

<h1>Write history with AI</h1>

<div class="connection-status">
	<div 
	  class="status-light"
	  style="background-color: {socketIsConnected ? 'var(--connect-color)' : '#969696'}"
	></div>
	<p style="opacity: 0.7;">{socketIsConnected ? 'Connected' : 'Disconnected'}</p>
</div>

<Button on:click={connectToWebsocket} hidden={socketIsConnected || socketConnecting} styleType="connect">
	Connect
</Button>

{#if socketIsConnected}
<p class="history-field">
	{#each messages as message, i}<Message {message} author={i % 2 == 0 ? "" :  "ai"}/>{/each}{message}
	<span class="ai-thinking" hidden={!awaitingResponse}>...AI is thinking </span>
</p>
<form>
	<input class="input-text"
		type="text"
		spellcheck="true"
		disabled={awaitingResponse}
		placeholder="Enter your text"
		bind:value={message}
	/>
	<input class="input-submit" type="submit" on:click={onSendMessage} disabled={awaitingResponse}/>
</form>
{/if}

<Button on:click={disconnectFromWebsocket} hidden={!(socketConnecting || socketIsConnected)} styleType="disconnect">
	Disconnect
</Button>

</div>


<style lang="scss">
	.wrapper {
		width: 800px;
        display: flex;
        flex-direction: column;
		align-items: center;
	}

	h1 {
		width: 70%;
		text-align: center;
		margin: 50px 0px 0px 0px;
		color: var(--title-color);
		font-size: 40px;
	}

	.connection-status {
		display: flex;
		align-items: center;
	}

	.status-light {
		width: 15px;
		height: 15px;
		border-radius: 50%;
		background-color: red;
		margin-right: 10px;
		box-shadow: 0 0 3px rgba(0, 0, 0, 0.2);
	}

	.history-field {
		width: 80%;
		min-height: 100px;
		max-height: 40vh;
		background-color: white;
		border: 2px solid var(--border);
		border-radius: 6px;
		margin: 10px 0px 10px 0px;
		padding: 10px 15px;
		word-wrap: break-word;
		overflow-wrap: break-word;
		word-break: break-word;
		white-space: normal;
		overflow-y: scroll;
	}

	.ai-thinking {
		color: lightgray;
	}

	form {
		margin: 10px 0px 15px 0px;
	}

	.input-text {
		padding: 10px;
		font-size: 16px;
		border: 1px solid var(--border);
		border-radius: 5px;
		width: 230px;
		box-sizing: border-box;
	}

	.input-submit {
		background-color: var(--connect-color);
		color: white;
		padding: 10px 15px;
		font-size: 16px;
		border: none;
		border-radius: 5px;
		cursor: pointer;
		transition: background-color 0.1s ease;
	}

	.input-submit:hover {
		filter:	brightness(90%);
	}

	.input-submit:disabled {
		filter:	brightness(90%);
		cursor: auto;    
	}

</style>