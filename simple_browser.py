#!/usr/bin/env python3

"""To set up a simple HTTP browser for seeing what has been logged."""

try:
    import sys
    from http.server import BaseHTTPRequestHandler, HTTPServer
    import functions
    import logging
except ImportError as e:
    sys.exit("Importing error: " + str(e))


def generate_html_page() -> None:
    """
    This gets a list of file names and creates a small html page with those names
    :return:
    """
    logging.basicConfig(filename="/logging/log.txt")
    logging.info("simple browser generate_html_page()")

    alist = functions.list_file_directory()
    blist = functions.row_major(alist, len(alist))
    clist = functions.html_table(blist)
    c = ""
    for cl in clist:
        c += cl
    start, end = functions.create_html_page_wrapper("table")
    page = start + c + end
    try:
        with open("table.html", "w") as fileObject:
            fileObject.write(page)
    except FileExistsError:
        print("<html><body><h1>" + "File Error" + "</h1></body></html>")


class WebServer(BaseHTTPRequestHandler):
    """
    This is a basic server class for serving a html file.
    """

    def serve_page(self, page: str):
        self.path = page
        try:
            print("first, ", self.path[1:])
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
        except FileNotFoundError as err:
            file_to_open = str(err)
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, "utf-8"))

    def do_GET(self) -> bool:
        generate_html_page()
        if self.path == "/":
            self.serve_page("/index.html")
            return True
        else:
            self.serve_page("/table.html")  # this needs to change for other options.
            self.send_response(303, "this is not where you want to be.")
            return False


def setup() -> None:
    logging.basicConfig(filename="/logging/log.txt")
    logging.info("simple browser setup()")
    server = HTTPServer(('localhost', 7000), WebServer)
    server.serve_forever()


if __name__ == '__main__':
    logging.basicConfig(filename="/logging/log.txt")
    setup()
