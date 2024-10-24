from socket import *
import re

# Step 1: Initialize Socket
clientSocket = socket(AF_INET, SOCK_STREAM)

# Step 2: Get a URI input
url = input("Enter the URL: ")
# Convert URL into an HTTP request
url = re.sub("http://", "", url)
url = re.split("/", url)
[HOST, PORT] = re.split(":", url[0])
link = url[1]

request = "GET /" + link + " HTTP/1.1\r\n" + "Host: " + HOST + ":" + PORT + "\r\n" + "Connection: close\r\n\r\n"
print(request)

# Step 3: Establish TCP connection to server
clientSocket.connect((HOST, int(PORT)))

# Step 4: Send HTTP request
clientSocket.send(request.encode("utf-8"))

# Step 5: Receive data from the client socket
message = clientSocket.recv(4096).decode("utf-8")
# Parse data
lines = re.split("\n", message)
status = re.sub("HTTP/1.1 ", "", lines[0])
print("Status: " + status)

# Print the html body
body = lines[-1]
print(body)

# Step 6: Close the connection
clientSocket.close()

