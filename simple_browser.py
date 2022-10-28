#!/usr/bin/env python3

"""To set up a simple HTTP browser for seeing what has been logged."""

try:
    import datetime
    import os
    import sys
    from http.server import BaseHTTPRequestHandler, HTTPServer
    import functions
except ImportError as e:
    sys.exit("Importing error: " + str(e))


class WebServer(BaseHTTPRequestHandler):
    """
    This is a basic server class for serving a html file.
    """

    def do_GET(self) -> bool:
        if self.path == "/":
            self.path = "/index.html"
            try:
                print("first, ", self.path[1:])
                file_to_open = open(self.path[1:]).read()
                self.send_response(200)
            except FileNotFoundError as err:
                file_to_open = str(err)
                self.send_response(404, str(err))
            self.end_headers()
            self.wfile.write(bytes(file_to_open, "utf-8"))
            return True
        else:
            self.send_response(303, "this is not where you want to be.")
        return False


def setup() -> None:
    server = HTTPServer(('localhost', 7000), WebServer)
    server.serve_forever()


if __name__ == '__main__':
    setup()
