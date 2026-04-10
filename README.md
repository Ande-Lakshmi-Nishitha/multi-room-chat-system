# Multi-Room Chat System

## Project Overview
This project implements a real-time multi-room chat system using a client-server architecture. Multiple users can connect to the server, join different chat rooms, and exchange messages instantly.

The system is designed to handle concurrent users efficiently while maintaining stability under various edge cases such as disconnections and invalid inputs.

---

## Features

- Supports multiple users simultaneously  
- Allows creation and joining of multiple chat rooms  
- Real-time message communication  
- Users can switch between rooms  
- Handles client disconnections gracefully  
- Validates user inputs and prevents crashes  
- Robust error handling for network issues  

---

## System Architecture

Clients connect to a central server which manages communication and chat rooms.

Client → Server → Chat Rooms

The server is responsible for:
- Managing client connections  
- Maintaining chat rooms  
- Broadcasting messages to users in the same room  

---

## Tech Stack

- Programming Language: Python  
- Networking: Socket Programming  
- Protocol: TCP  
- Version Control: Git and GitHub  

---

## Setup Instructions

### Clone the Repository

git clone https://github.com/Ande-Lakshmi-Nishitha/multi-room-chat-system.git  
cd multi-room-chat-system  

---

### Install Dependencies

pip install -r requirements.txt  

---

### Run the Server

python server.py  

---

### Run the Client

Open multiple terminals and run:

python client.py  

---

## Usage

1. Start the server  
2. Run multiple client instances  
3. Enter a username when prompted  
4. Join or create a chat room  
5. Start sending and receiving messages  

---

## Commands

/join room_name   Join or create a room  
/leave            Leave the current room  
/exit             Disconnect from the server  

---

## Optimization and Improvements

- Improved handling of abrupt client disconnections  
- Added validation for incorrect or unexpected inputs  
- Enhanced server stability under multiple connections  
- Fixed bugs identified during testing  
- Improved message handling and delivery  

---

## Testing

The system was tested with multiple concurrent clients to ensure:

- Stable connections  
- Correct message broadcasting  
- Proper handling of edge cases such as disconnections and invalid commands  

---

## Project Structure

multi-room-chat-system/  
│── server.py  
│── client.py  
│── README.md  

---

## Future Improvements

- Add graphical user interface  
- Implement message storage using a database  
- Add user authentication  

