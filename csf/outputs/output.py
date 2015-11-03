import HTML
import datetime
import os
from html_assets import *

PLATFORM = {
    "twitter" : 0,
}

AUDIT_DIR = "audit_result"
AUDIT_HTML = AUDIT_DIR + "/audit.html"
AUDIT_TEXT = AUDIT_DIR + "/audit.text"

def time_convert(time_long):
    return datetime.datetime.fromtimestamp(
        int(time_long)
    ).strftime('%Y-%m-%d %H:%M:%S')


class OutputFactory(object):

    verbose = False
    targets = []

    def __init__(self, verbose, targets):
        self.verbose = verbose
        self.targets = targets

    def append(self, input_list, platform):
        raise NotImplementedError("Please Implement this method")

    def __twitter_output(self, input_list):
        raise NotImplementedError("Please Implement this method")


class HtmlOutput(OutputFactory):

    def __build_html_header(self, title, targets):
        head = header.header_html(title, targets)
        return head

    def __build_html_footer(self):
        foot = footer.footer_html()
        return foot

    def __init__(self, verbose, targets):
        super(self.__class__, self).__init__(verbose, targets)

        header_code = self.__build_html_header("RAMOS", self.targets)
        footer_code = self.__build_html_footer()
        html_code = "HELLO WORLD!"

        file_handler = open(AUDIT_HTML, "w")
        file_handler.write(header_code)
        file_handler.write(html_code)
        file_handler.write(footer_code)
        file_handler.close()

    def append(self, input_list, platform):
        if platform == PLATFORM["twitter"]:
            self.__twitter_output(input_list)

    def __twitter_output(self, input_list):
        t = HTML.Table(
                header_row=[
                    'timestamp',
                    'author',
                    'message',
                ],
                classes="table table-striped"
            )
        for message in input_list:
            messenger_id = message[2]+"("+message[3]+")"
            datetime = time_convert(message[6])
            t.rows.append(
                [datetime, messenger_id, message[5]])
        html_code = str(t)

        header_code = self.__build_html_header("twitter", self.targets)
        footer_code = self.__build_html_footer()

        file_handler = open(AUDIT_DIR + "/twitter.html", "w")
        file_handler.write(header_code)
        file_handler.write(html_code)
        file_handler.write(footer_code)
        file_handler.close()

        if self.verbose:
            print htmlcode



class TextOutput(OutputFactory):

    def __format_twitter_message(self, message):
        messenger_id = message[2]+"("+message[3]+")"
        datetime = time_convert(message[6])
        formated_message = datetime +\
            " by " + messenger_id +\
            ":"   + message[5]
        return formated_message

    def append(self, input_list, platform):
        if platform == PLATFORM["twitter"]:
            self.__twitter_output(input_list)

    def __twitter_output(self, input_list):
        file_handler = open(AUDIT_TEXT, "w")
        for twitter_tuple in input_list:
            message = self.__format_twitter_message(twitter_tuple)
            file_handler.write(message + "\n")
            if self.verbose:
                print "[+]", message

        file_handler.close()

def __create_directories():
    if not os.path.exists(AUDIT_DIR):
        os.makedirs(AUDIT_DIR)

def create_output_manager(html, verbose, targets):
    __create_directories()
    if html:
        output = HtmlOutput(verbose, targets)
    else:
        output = TextOutput(verbose, targets)
    return output
