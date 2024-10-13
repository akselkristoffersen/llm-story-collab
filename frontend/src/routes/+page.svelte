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
	  style="background-color: {socketIsConnected ? '#4CAF50' : '#969696'}"
	></div>
	<p>{socketIsConnected ? 'Connected' : 'Disconnected'}</p>
  </div>

<button 
	class="button-connect" 
	on:click={connectToWebsocket} 
	hidden={socketIsConnected || socketConnecting}
	style="background-color: #4CAF50;"
	>
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
		placeholder="Enter your text"
		bind:value={message}
	/>
	<input class="input-submit" type="submit" on:click={onSendMessage} disabled={awaitingResponse}/>
</form>
{/if}

<button 
	class="button-connect" 
	on:click={disconnectFromWebsocket} 
	hidden={!(socketConnecting || socketIsConnected)}
	style="background-color: #969696;"
	>
	Disconnect
</button>

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
		color: #3D52A0;
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
		border: 2px solid rgb(208, 208, 208);
		border-radius: 4px;
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
		border: 1px solid #ccc;
		border-radius: 5px;
		width: 200px;
		box-sizing: border-box;
	}

	.input-submit {
		background-color: #4CAF50;  /* Green background */
		color: white;               /* White text */
		padding: 10px 15px;         /* Padding for the button */
		font-size: 16px;            /* Font size for button text */
		border: none;               /* Remove default border */
		border-radius: 5px; /* Rounded corners, but only right side */
		cursor: pointer;            /* Pointer on hover */
		transition: background-color 0.1s ease; /* Smooth hover transition */
	}

	.input-submit:hover {
		filter:	brightness(90%);
	}

	.input-submit:disabled {
		filter:	brightness(90%);
		cursor: auto;    
	}

	.button-connect {
		color: white;
		border: none;    
		padding: 15px 30px;
		margin-top: 15px;
		font-size: 18px;
		font-weight: bold;
		border-radius: 10px;
		cursor: pointer;
		transition: background-color 0.1s ease;
	}

	.button-connect:hover {
		filter:	brightness(92%);
	}

	.button-connect:active {
		background-color: #388E3C;
		transform: scale(0.98);
	}

</style>