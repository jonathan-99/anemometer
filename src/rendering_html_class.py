try:
    import os
    import sys
    import csv
    import json
    import logging
    import datetime
except ImportError as e:
    sys.exit("Importing error: " + str(e))


class RenderingHtmlPage:
    """
    This is to extract all page rendering from functions.
    """

    def __init__(self, page_name="") -> None:
        self.page = None
        self.html_table = None
        self.files_in_directory = []
        self.default_directory = "data/"
        self.title_start = "<!DOCTYPE html><head><title>"
        self.title_finish = "</title></head><body>"
        self.end_tags = "</body></html>"
        self.page_name = page_name

        self._put_files_in_directory_field()
        self.create_and_set_html_table(self.files_in_directory)
        self._set_page_as_string()
        self._generate_html_file(self.page)

    def _put_files_in_directory_field(self):
        for a_file in os.listdir(self.default_directory):
            extension = os.path.splitext(a_file)
            if extension[1] == '.py':
                self.files_in_directory.append(extension[0])
            else:
                pass

    def get_files_in_directory(self) -> list:
        return self.files_in_directory

    def _set_page_as_string(self) -> None:
        self.page = ''.join(self.title_start).join(self.title_finish).join(self.html_table).join(self.end_tags)

    def get_page_as_string(self) -> str:
        return str(self.page)

    def get_page_as_json(self) -> json:
        output_json = {
            "page title": self.page_name,
            "page header": self.title_start.join(self.title_finish),
            "body": self.html_table,
            "html end": self.end_tags
        }
        return output_json

#    def row_major(alist: list) -> list:
#        """
#        Not quite sure of this yet
#        :param alist: list
#        :param sub_len: int
#        :return: list: output_list
#        """
#        for i in range(0, len(alist), len(alist)):
#            output_list = alist[i:i + len(alist)]
#        return output_list

    def create_and_set_html_table(self, input_value: list) -> None:
        """
        This function takes a list of values and wraps them in an html tag list for rendering.
        :param input_value: list
        """
        logging.debug("html_table")

        output = ['<table>']
        for sublist in input_value:
            output.append('<tr><td>')
            output.append('</td><td>'.join(sublist))
            output.append('</td></tr>')
        output.append('</table>')
        output_as_string = ''.join(output)
        self.set_html_table(output_as_string)

    def set_html_table(self, input_string: str) -> None:
        self.html_table = input_string

    def get_html_table_as_string(self) -> str:
        return self.html_table

    def get_newest_file(self, input_list: list) -> str:
        logging.debug("get_newest_file")

        for value in range(-1, 30, 1):
            check_this_day = str(datetime.datetime.now() - datetime.timedelta(value))[0:10]+".txt"
            if check_this_day in input_list:
                output_date = check_this_day
                logging.debug("Most current file: " + str(output_date))
                return output_date
            else:
                logging.debug("Need to go back further in get_newest_file() to find newest file")
        return "No file found"
    def _generate_html_file(self) -> None:
        try:
            with open(self.page_name + ".html", "w") as fileObject:
                fileObject.write(self.page)
        except FileExistsError as e:
            print("<html><body><h1>" + "File Error: {}" + "</h1></body></html>".format(str(e)))
            logging.error("File Exists Error in generate_html_page()", exc_info=True)