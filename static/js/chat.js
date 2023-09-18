const id =JSON.parse(document.getElementById('json-username').textContent);
const message_username = JSON.parse(document.getElementById('json-message-username').textContent);
const socket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/'
    + id
    + '/'
);
socket.onopen = function(e){
    console.log("connection established");
}

socket.onclose = function(e){
    console.log("connection lost");
}

socket.onerror = function(e){
    console.log(e);
}

socket.onmessage = function(e){
    const data = JSON.parse(e.data);
    
    if (data.username==message_username){
        document.querySelector('#chat-body').innerHTML += 
        `<tr>
        <td>
            <p class="you">
                ${data.message}
                
            </p>
        </td>
        </tr>`
    }
    else{
        document.querySelector('#chat-body').innerHTML += 
        `<tr>
        <td>
            <p class="frnd">
                ${data.message}
               
            </p>
        </td>
        </tr>`
    }
}



document.querySelector('#chat-message-submit').onclick = function(e){
    const message_input=document.querySelector('#message_input');
    const message=message_input.value;
   
  
    if (message == "")
   {
      
   return false;
   }
    else{
   
    socket.send(JSON.stringify({
       'message':message,
       'username':message_username
    }))
    message_input.value = '';
   }
}