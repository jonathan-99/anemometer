#!/usr/bin/env python3

"""To set up a simple HTTP browser for seeing what has been logged."""

try:
    import sys
    from http.server import BaseHTTPRequestHandler, HTTPServer
    from src import basic_plotting as basic_plot
    from src import functions
    import logging
except ImportError as e:
    sys.exit("Importing error: " + str(e))


def generate_html_page(name_of_page: str) -> None:
    """
    This gets a list of file names and creates a small html page with those names
    :return:
    """
    logging.basicConfig(filename="../logging/log.txt")
    logging.debug("simple browser generate_html_page() with page " + name_of_page)

    page = functions.listing_directory(name_of_page)
    try:
        with open(name_of_page + ".html", "w") as fileObject:
            fileObject.write(page)
    except FileExistsError as e:
        print("<html><body><h1>" + "File Error" + "</h1></body></html>")
        logging.error("File Exists Error in generate_html_page()", exc_info=True)
    return


class WebServer(BaseHTTPRequestHandler):
    """
    This is a basic server class for serving a html file.
    """
    logging.debug("Within WebServer Class")

    def serve_page(self, page: str):
        self.path = page
        try:
            print("first, ", self.path[1:])
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
        except FileNotFoundError as err:
            file_to_open = str(err)
            self.send_response(404)
            logging.error("File Not Found Error - in serve_page()", exc_info=True)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, "utf-8"))

    def do_GET(self) -> bool:
        generate_html_page("table")
        if self.path == "/":
            self.serve_page("/index.html")
            logging.debug("Served main index.html page")
            return True
        else:
            self.serve_page("/table.html")  # this needs to change for other options.
            self.serve_page("/latest_day_plot.html")
            self.send_response(303, "this is not where you want to be.")
            logging.debug("Served table.html page.")
            return False


def setup() -> None:
    logging.basicConfig(filename="../logging/log.txt")
    # plot of newest data
    basic_plot.create_plot()
    server = HTTPServer(('localhost', 7000), WebServer)
    status = "Serving on: " + str(server.server_name) \
        + " addr: " \
        + str(server.server_address) \
        + " port: " \
        + str(server.server_port)
    print(status)
    logging.debug(status)
    server.serve_forever()


if __name__ == '__main__':
    logging.basicConfig(filename="../logging/log.txt")
    setup()
