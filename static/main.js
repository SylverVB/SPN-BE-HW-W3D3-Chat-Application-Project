const socket = io(); // Initializing a new socket.io connection

// Event listener for the chat form submission
document.getElementById('chatForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Preventing the form from submitting the traditional way

    // Retrieve and format the username
    let username = document.getElementById('name').value;
    username = username.split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()).join(' ');

    const room = document.getElementById('room').value; // Retrieving the selected room

    // Emitting a join event with the username and room
    socket.emit('join', { username, room });

    // Clearing the input fields after submission
    document.getElementById('name').value = '';
    document.getElementById('room').value = '';

    // Creating a new div element for the user
    const userDiv = document.createElement('div');
    userDiv.classList.add('user-div');
    userDiv.innerHTML = `
        <strong>${username}</strong>
        <form id="messageForm" class="row g-3">
            <div class="col-md-12">
                <textarea id="message" name="message" class="form-control" placeholder="Your Message" required style="width: 100%; word-wrap: break-word; overflow: hidden;"></textarea>
            </div>
            <div class="col-12 mb-3">
                <button type="submit" class="btn btn-primary">Send Message</button>
                <button type="button" class="btn btn-danger leave-room">Leave Room</button>
            </div>
        </form>
    `;

    // Event listener for the leave room button
    const leaveButton = userDiv.querySelector('.leave-room');
    leaveButton.addEventListener('click', function() {
        socket.emit('leave', { username, room }); // Emitting a leave event with the username and room
        userDiv.remove(); // Removing the user's div element from the DOM
    });

    // Event listener for the message form submission
    const messageForm = userDiv.querySelector('#messageForm');
    messageForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Preventing the form from submitting the traditional way
        const message = messageForm.querySelector('#message').value; // Retrieving the message text
        socket.emit('message', { username, room, message }); // Emitting a message event with the username, room, and message
        messageForm.querySelector('#message').value = ''; // Clearing the message input field
    });

    // Appending the user div to the appropriate room div based on the selected room
    if (room === 'Backend Developers Room') {
        document.getElementById('backend-developers-room').appendChild(userDiv);
    } else {
        document.getElementById('frontend-developers-room').appendChild(userDiv);
    }
});

// Event listener for system messages
socket.on('system_message', function(data) {
    const chatDiv = data.room === 'Backend Developers Room' ? 'backend-developers-chat' : 'frontend-developers-chat';
    const messageElement = document.createElement('div');
    messageElement.innerHTML = `<i style='color: gray;'>${data.message}</i>`; // Displaying system messages in gray italics
    document.getElementById(chatDiv).appendChild(messageElement);
});

// Event listener for chat messages
socket.on('chat_message', function(data) {
    const chatDiv = data.room === 'Backend Developers Room' ? 'backend-developers-chat' : 'frontend-developers-chat';
    const messageElement = document.createElement('div');

    // Extracting the timestamp, username, and message content
    const timestampEndIndex = data.message.indexOf(']');
    const timestamp = data.message.slice(0, timestampEndIndex + 1);
    const rest = data.message.slice(timestampEndIndex + 2);
    const usernameEndIndex = rest.indexOf(':');
    const username = rest.slice(0, usernameEndIndex);
    const messageContent = rest.slice(usernameEndIndex + 2);

    // Formatting the entire message
    const formattedMessage = `
        <span style='color: darkred;'>${timestamp}</span>
        <strong>${username}</strong>:
        <span>${messageContent}</span>
    `;

    messageElement.innerHTML = formattedMessage;
    document.getElementById(chatDiv).appendChild(messageElement);
    // console.log(formattedMessage); // Debugging code: log the formatted message
});