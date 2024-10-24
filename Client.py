from socket import *
import re

# Harley's IP: 104.39.74.116            DELETE BEFORE SUBMISSION

HOST = '127.0.0.1'
PORT = 5000

# Step 1: Initialize Socket
clientSocket = socket(AF_INET, SOCK_STREAM)

# Step 2: Get a URI input
url = input("Enter the URL:")

# Step 3: Establish TCP connection to server
clientSocket.connect((HOST, PORT))

# Step 4: Send HTTP request
clientSocket.send(url.encode("utf-8"))

# Step 5: Receive data from the client socket
message = clientSocket.recv(1024).decode("utf-8")
# Parse data
lines = re.split("\n", message)
status_line = re.split(" ", lines[0])
status = status_line[1] + status_line[2]
print("Status: " + status)

# Print the html body
body = lines[-1]
print(body)

# Step 6: Close the connection
clientSocket.close()

