#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
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

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it


import sys
import socket
import re
# you may use urllib to encode data appropriately
# https://docs.python.org/3/library/urllib.parse.html introduction of urlparse and urlencode
from urllib.parse import urlparse,urlencode


def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    def get_host_port(self,url):
        url = urlparse(url)
        if url.hostname:
            host =url.hostname 
        else:
            host = localhost
        if url.port:
            port = url.port
        else:
            port = 80
        return host,port

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        code = int(data.split(' ')[1])
        return code

    def get_headers(self,data):
        header = data.split('\r\n\r\n')[0]
        return header

    def get_body(self, data):
        body = data.split('\r\n\r\n')[1]
        return body
    
    def get_path(self,url):
        url = urlparse(url)
        if url.path:
            path = url.path
        else:
            path = '/'
        return path

    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    def get_length(self,args):
        if args:
            length = len(urlencode(args))
            
        else:
            length = 0
        return length

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        host,port = self.get_host_port(url)
        path = self.get_path(url)
        self.connect(host,port)
        request = f"GET {path} HTTP/1.1\r\nHost: {host}:{port}\r\nConnection: close\r\n\r\n"
        self.sendall(request)
        data = self.recvall(self.socket)
        self.close()
        code = self.get_code(data)
        body = self.get_body(data)
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        host,port = self.get_host_port(url)
        path = self.get_path(url)
        length = self.get_length(args)
        self.connect(host,port)
        if args:
            request = f"POST {path} HTTP/1.1\r\nHost: {host}:{port}\r\nContent-type: application/x-www-form-urlencoded\r\nContent-length: {length}\r\n\r\n{urlencode(args)}"
        else:
            request = f"POST {path} HTTP/1.1\r\nHost: {host}:{port}\r\nContent-type: application/x-www-form-urlencoded\r\nContent-length: {length}\r\n\r\n"
        self.sendall(request)
        data = self.recvall(self.socket)
        self.close()
        code = self.get_code(data)
        body = self.get_body(data)
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    print("argv is ",sys.argv[2], sys.argv[1])
    client = HTTPClient()
    command = "GET"
    print("argv is ",sys.argv[2], sys.argv[1])
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))