# Mini-Project: Chat Application Project

# Our objective is to create a versatile WebSocket Chat Application, that enables users to communicate in real-time. The system should facilitate a seamless user experience by supporting a wide array of operations, including joining chat rooms, sending messages, and handling users. To achieve this goal, we must implement a diverse set of functionalities using WebSocket technology and JavaScript programming techniques.

# Project Requirements

# 1. WebSocket Setup and Configuration:
# - Implement WebSocket connections in the chat application.
# - Understand the concept of bi-directional, full-duplex communication.
# - Configure WebSocket server and client to establish communication channels.
# - Implement Cors Origin to allow communication with front-end applications

# 2. Implementing WebSocket Events and Handlers:
# - Implement connection, message, and disconnection events.
# - Understand WebSocket event handling and how it differs from traditional HTTP request-response cycles.
# - Handle WebSocket events to manage user interactions in the chat application.

# 3. Creating a Chat Room:
# - Design and implement a chat room feature where users can join and participate in conversations.
# - Every time a user joins the chat room, broadcast a message to everyone in the room that the user has joined
# - Create join_room.html to create a room and join to enter the chat

# 4. Real-Time Messaging and Broadcasting (Optional):
# - Implement real-time messaging between users in the chat room.
# - Implement features like message deletion and editing to enhance user experience.
# - Broadcast messages to all users in the chat room when a new message is sent.

# Project Tips

# 1. WebSocket Events and Handlers:
# - Use WebSocket events like onopen, onmessage, and onclose to manage user connections and disconnections.

# 2. Chat Room Management:
# - Create a data structure to store active chat rooms and their participants.

# 3. Real-Time Messaging:
# - Use WebSocket's real-time capabilities to send and receive messages instantly.


from flask import Flask, render_template, request  # Importing Flask modules for web application
from flask_socketio import SocketIO, emit, join_room, leave_room  # Importing SocketIO modules for WebSocket support
from flask_cors import CORS  # Importing CORS for cross-origin support
from datetime import datetime  # Importing datetime for timestamping messages
import os  # Importing os for environment variables

app = Flask(__name__)  # Initializing Flask application
CORS(app, resources={r"/*": {"origins": "http://localhost:5000"}})  # Configuring CORS
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'super-secret-key'  # Setting secret key for session management
socketio = SocketIO(app, cors_allowed_origins="*")  # Initializing SocketIO with Flask app

@app.route('/')
def index():
    return render_template('index.html') # Rendering the index.html template when accessing the root URL

@socketio.on('join')  # Listening for 'join' events
def on_join(data):
    username = ' '.join([word.capitalize() for word in data['username'].split()]) # Capitalizing each word in the username
    room = data['room']  # Retrieving the room name from the data
    join_room(room)  # Joining the specified room
    time_stamp = datetime.now().strftime("%Y-%m-%d %I:%M %p")  # Getting the current timestamp
    message = f"{username} enters the chat at {time_stamp}"  # Creating the join message
    emit('system_message', {'message': message, 'room': room}, room=room)  # Emitting the system message to the room

@socketio.on('leave')  # Listening for 'leave' events
def on_leave(data):
    username = ' '.join([word.capitalize() for word in data['username'].split()])
    room = data['room']
    # print(f"User {username} is leaving room {room}")  # Debugging line
    time_stamp = datetime.now().strftime("%Y-%m-%d %I:%M %p")
    message = f"{username} leaves the chat at {time_stamp}"  # Creating the leave message
    # print(f"Prepared message: {message}")  # Debugging line
    emit('system_message', {'message': message, 'room': room}, room=room, broadcast=True)
    leave_room(room)  # Leaving the specified room

@socketio.on('message')  # Listening for 'message' events
def on_message(data):
    username = ' '.join([word.capitalize() for word in data['username'].split()])
    room = data['room']
    message = data['message']  # Retrieving the message content
    time_stamp = datetime.now().strftime("%Y-%m-%d %I:%M %p")
    formatted_message = f"[{time_stamp}] {username}: {message}"  # Formatting the chat message
    # print(f"Emitting message: {message}")  # Debugging line
    emit('chat_message', {'message': formatted_message, 'room': room}, room=room)  # Emitting the chat message to the room
    # print("Message emitted")  # Debugging line

if __name__ == '__main__':
    socketio.run(app, debug=True)  # Running Flask app with SocketIO in debug mode