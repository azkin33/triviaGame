#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import urllib.request
import json


class RequestHandler(BaseHTTPRequestHandler):

    def say_hello(self, query):
        """
        Send Hello Message with optional query
        """
        mes = "Hello"
        if "name" in query:
            # query is params are given as array to us
            mes += " " + "".join(query["name"])
        self.send_response(200)
        self.end_headers()
        self.wfile.write(str.encode(mes+"\n"))

    def start_new_game(self):
        req = urllib.request.Request("https://opentdb.com/api.php?amount=10")
        with urllib.request.urlopen(req) as response:
            data = response.read().decode()
            js = json.loads(data)

        for x in js["results"]:
            print(x["category"])
        print("done")
        self.send_response(200)
        self.end_headers()


    def do_GET(self):
        # Parse incoming request url
        url = urlparse(self.path)
        if url.path == "/hello":
            return self.say_hello(parse_qs(url.query))
        elif url.path == "/newGame":
    
            return self.start_new_game()
 
        # return 404 code if path not found
        self.send_response(404)
        self.end_headers()
        self.wfile.write(b'Not Found!\n')
        

if __name__ == "__main__":
    port = 8080
    print(f'Listening on localhost:{port}')
    server = HTTPServer(('', port), RequestHandler)
    server.serve_forever()
