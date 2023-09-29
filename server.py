#  coding: utf-8
import socketserver


# Copyright 2013 Abram Hindle, Eddie Antonio Santos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()

        print("Got a request of: %s\n" % self.data)

        http_method = self.data.decode('utf-8').split()[0]
        http_path = self.data.decode('utf-8').split()[1]

        if http_method != "GET":
            response = "HTTP/1.1 405 Method Not Allowed\r\n\r\n".encode()
        else:
            if http_path.endswith("/"):  # if a directory/html file
                http_path = "./www" + http_path + "index.html"
                with open(http_path, 'r') as f:
                    html_file = f.read()
                response = f"HTTP/1.1 200 OK \r\nContent-Type: text/html\r\n\r\n<body>{html_file}</body>".encode()
            elif http_path.endswith(".css"):  # if a css file
                http_path = "./www" + http_path
                with open(http_path, 'r') as f:
                    css_file = f.read()
                response = f"HTTP/1.1 200 OK \r\nContent-Type: text/css\r\n\r\n{css_file}".encode()
            elif http_path.endswith(".html"):  # if a html file
                http_path = "./www" + http_path
                with open(http_path, 'r') as f:
                    html_file = f.read()
                response = f"HTTP/1.1 200 OK \r\nContent-Type: text/html\r\n\r\n{html_file}".encode()
            else:
                try:
                    path = http_path + "/"
                    response = f"HTTP/1.1 301 Moved Permanently \r\nLocation: {path}\r\n\r\n".encode()
                except FileNotFoundError:
                    response = "HTTP/1.1 404 Not Found \r\n\r\n<html><h1>404 File not found</h1></html>\r\n\r\n".encode()

        self.request.sendall(response)


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

    connection.close()
