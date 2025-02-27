import socket as s
from socket import *
import os
import re

# HOW TO RUN THIS PROGRAM:
# 1. Make sure index.html is in the .venv folder along with this Python project
# 2. When prompted, type any value other than "0" (ex. "1") to use the localhost IP
# 3. On your device, type in http://127.0.0.1:8090/index.html in your browser
#       This should output the text in index.html
# 4. On your device, type in http://127.0.0.1:8090/test.html in your browser
#       This should output a 404 File Not Found error

i = input("Type 0 to use your device's IP, otherwise localhost for any other input: ")
if i == "0":
    HOST = s.gethostbyname(s.gethostname())
else:
    HOST = "127.0.0.1"
PORT = 8090         # Use arbitrary port 8090

# Step 1: Initialize the Socket and bind to IP address and port w/ reusable address
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind((HOST, PORT))
print("HTTP Server with IP " + HOST + " and Port " + str(PORT) + " online.")

while True:
    # Step 2: Establish a TCP Connection when contacted by client
    serverSocket.listen()
    serverSocket.settimeout(60)         # Automatically close the server after a minute of inactivity
    print("Server socket is listening...")
    connSocket, addr = serverSocket.accept()

    try:
        # STEP 3: Receive a HTTP request
        http_message = connSocket.recv(1024).decode("utf-8")    # Decode HTTP message from binary to ASCII using utf-8

        print("\nThe HTTP Request Packet Message: \n-----------------------------------")
        print(http_message)

        print("\nData after parsing request: \n-----------------------------------")
        # STEP 4: Parse the request to determine file
        lines = re.split("\n", http_message)
        # Assume HTTP version 1.1 and GET request
        request_line = re.split(" ", lines[0])
        url = re.sub("/", "", request_line[1])
        print("URL: " + url)

        host_line = re.split(" ", lines[1])
        host = host_line[1]
        print("HOST: " + host)

        # Can parse the second header line to ask if the request is persistent,
        # but in this case, assume it is not and close the connection after the request.

        # Step 5: Read requested file
        if os.path.isfile(url):     # If file is in the server directory
            print("File found in server!")
            status = "200 OK"
            with open(url, 'rb') as file:
                content = file.read()
            header = "Content-Type: text/html\r\n" + "Content-Length: " + str(len(content)) + "\r\n" + "Connection: close\r\n"

        else:       # If the file is not in the server directory
            print("File NOT found in server.")
            status = "404 File Not Found"
            header = "Connection: close\r\n"
            content = "404 File Not Found".encode("utf-8")

        # Step 6: Create HTTP response message
        http_response = "HTTP/1.1 " + status + "\r\n" + header + "\r\n"
        print("\nThe HTTP Response Packet Message: \n-----------------------------------")
        print(http_response + content.decode("utf-8") + "\n")

        # Step 7: Send a TCP response
        connSocket.send(http_response.encode("utf-8") + content)

        # Step 8: Close the Connection
        break

    except IOError:
        print("No connection between client and server. Send Error 400.")
        status = "400 Bad Request"
        content = "Invalid Request!".encode("utf-8")
        http_response = "HTTP/1.1 " + status + "\r\n" + "Connection: close\r\n\r\n"
        print("\nThe HTTP Response Packet Message: \n-----------------------------------")
        print(http_response + content.decode("utf-8") + "\n")
        connSocket.send(http_response.encode("utf-8") + content)
        break

print("Closing the connection.")
serverSocket.close()
exit()  # Exit the program