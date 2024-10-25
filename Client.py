from socket import *
import re

# HOW TO RUN THIS PROGRAM:
# 1. Go to the HTTPServer.py file on a separate device and type "0" when prompted
# 2. On this device, run Client.py, and input the url using the following format:
#       http://xxx.xxx.xxx.xxx:8090/index.html
#       "xxx.xxx.xxx.xxx" is the IP address of the other device
#       This should show a 200 OK message and the html body
# 3. Then, rerun the server and the client, now inputting the url using the following format:
#       http://xxx.xxx.xxx.xxx:8090/test.html
#       This should show a 404 Error Not Found message and "File not found" message in the body

# Step 1: Initialize Socket w/ reusable address
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

# Step 2: Get a URI input
url = input("Enter the URL: ")
# Convert URL into an HTTP request
url = re.sub("http://", "", url)
url = re.split("/", url)
[HOST, PORT] = re.split(":", url[0])
link = url[1]

request = "GET /" + link + " HTTP/1.1\r\n" + "Host: " + HOST + ":" + PORT + "\r\n" + "Connection: close\r\n\r\n"
print("\nThe HTTP Request Packet Message: \n-----------------------------------")
print(request)

# Step 3: Establish TCP connection to server
clientSocket.connect((HOST, int(PORT)))

# Step 4: Send HTTP request
clientSocket.send(request.encode("utf-8"))

# Step 5: Receive data from the client socket
message = clientSocket.recv(4096).decode("utf-8")
print("\nThe HTTP Response Packet Message: \n-----------------------------------")
print(message)

# Parse data
lines = re.split("\n", message)
status = re.sub("HTTP/1.1 ", "", lines[0])
print("Status: " + status)

# Print the html body
body = lines[-1]
print(body)

# Step 6: Close the connection
clientSocket.close()

exit()  # Exit the program