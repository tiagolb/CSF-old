import os
from html_assets import *
import urllib
import datetime

AUDIT_DIR = "audit_result"
AUDIT_HTML = AUDIT_DIR + "/audit.html"

def time_convert(time_long):
    return datetime.datetime.fromtimestamp(
        int(time_long)
    ).strftime('%Y-%m-%d %H:%M:%S')

def urldecode(string):
    return urllib.unquote(string)

# Based on the template design pattern
class OutputFactory(object):
    targets = []

    def __build_html_header(self):
        head = header.header_html(self.title, self.targets)
        return head

    def __build_index_header(self, newTitle):
        head = header.header_html(newTitle, self.targets)
        return head

    def __build_html_footer(self):
        foot = footer.footer_html()
        return foot

    def __build_index(self):
        header_code = self.__build_index_header("RAMAS")
        footer_code = self.__build_html_footer()
        html_code = """
            <div class="row">
              <div class="col-md-2"></div>
              <div class="col-md-8">
                <h1>RAMAS</h1>
                <h3 class="text-justify">This is RAMAS, a data-carving utility designed to extract data from conversations that took place while using applications such as Facebook, Twitter and more.</h3>
                <h3 class="text-justify">RAMAS was implemented for the Ciber Forensic Security course at Instituto Superior Tecnico and is available at this <a href="https://github.com/tiagolb/CSF">GitHub repository</a>.</h3>

                <h4 class="text-center">
                    <br/>
                    Project by:<br/>
                    Tiago Brito<br/>
                    Diogo Barradas<br/>
                    David Duarte
                </h4>
                </div>
              <div class="col-md-2"></div>
            </div>
        """
        file_handler = open(AUDIT_HTML, "w")
        file_handler.write(header_code)
        file_handler.write(html_code)
        file_handler.write(footer_code)
        file_handler.close()

    def __create_directories(self):
        if not os.path.exists(AUDIT_DIR):
            os.makedirs(AUDIT_DIR)
        if not os.path.exists(AUDIT_HTML) and self.html:
            self.__build_index()

    def setup(self, title, targets, html, verbose):
        self.targets = targets
        self.title = title
        self.html = html
        self.verbose = verbose

        if html:
            self.html_filename = "/"+title+".html"

        self.text_filename = "/"+title+".txt"
        self.__create_directories()

    def text_code(self): pass
    def html_code(self): pass

    def out(self, input_list):

        if self.html:
            header_code = self.__build_html_header()
            footer_code = self.__build_html_footer()

            file_handler = open(AUDIT_DIR + self.html_filename, "w")
            file_handler.write(header_code)
            file_handler.write("<h1>"+ self.title +"</h1>")
            file_handler.write(self.html_code(input_list))
            file_handler.write(footer_code)
            file_handler.close()

        file_handler = open(AUDIT_DIR + self.text_filename, "w")
        file_handler.write("***** "+ self.title +" *****")
        file_handler.write(self.text_code(input_list))
        file_handler.close()
