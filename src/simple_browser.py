#!/usr/bin/env python3

"""To set up a simple HTTP browser for seeing what has been logged."""

try:
    import sys
    import logging
    from http.server import BaseHTTPRequestHandler, HTTPServer
    import src.basic_plotting as basic_plot
    import src.functions
    import src.rendering_html_class as html_class
except ImportError as e:
    logging.error("Importing error: " + str(e))


class WebServer(BaseHTTPRequestHandler):
    """
    This is a basic server class for serving a html file.
    """
    logging.debug("Within WebServer Class")

    def serve_page(self, page: str):
        self.path = page
        try:
            logging.debug("first, {}".format(self.path[1:]))
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
        except FileNotFoundError as err:
            file_to_open = str(err)
            self.send_response(404)
            logging.error("File Not Found Error - in serve_page()", exc_info=True)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, "utf-8"))

    def do_get(self) -> bool:
        html_class.RenderingHtmlPage("table")
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
    # plot of newest data
    basic_plot.create_plot()
    server = HTTPServer(('localhost', 7000), WebServer)
    status = "Serving on: " + str(server.server_name) \
        + " addr: " \
        + str(server.server_address) \
        + " port: " \
        + str(server.server_port)
    logging.debug(status)
    server.serve_forever()


if __name__ == '__main__':
    logging.basicConfig(filename='logging/log.txt')
    setup()
