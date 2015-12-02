#!/usr/bin/env python
'''
The MIT License (MIT)

Copyright (c) 2015 Tiago Brito

Permission is hereby granted, free of charge, to any person obtaining a copy of this software
and associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT
OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

__author__ = "Tiago Brito, Diogo Barradas, David Duarte"
__copyright__ = "Copyright 2015, Tiago Brito"
__credits__ = ["Tiago Brito", "Diogo Barradas", "David Duarte"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Tiago Brito"
__email__ = "tiago.de.oliveira.brito@tecnico.ulisboa.pt"
__status__ = "Production"

import os
from html_assets import *
import urllib
import datetime

AUDIT_DIR = "audit_result"
AUDIT_HTML = AUDIT_DIR + "/audit.html"

# convert timestamps to user friendly time strings
def time_convert(time_long):
    return datetime.datetime.fromtimestamp(
        int(time_long)
    ).strftime('%Y-%m-%d %H:%M:%S')

# decode url encoded strings
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

    def text_code(self): pass # to be implemented by subclasses
    def html_code(self): pass # to be implemented by subclasses

    def out(self, input_list):

        # if the html flag is active
        if self.html:
            # generate header and footer html code
            header_code = self.__build_html_header()
            footer_code = self.__build_html_footer()

            # create html file for this target
            file_handler = open(AUDIT_DIR + self.html_filename, "w")
            file_handler.write(header_code) # write header code
            file_handler.write("<h1>"+ self.title +"</h1>")
            file_handler.write(self.html_code(input_list)) # write results
            file_handler.write(footer_code) # write footer code
            file_handler.close() # close file

        # create text file for this target
        file_handler = open(AUDIT_DIR + self.text_filename, "w")
        file_handler.write("***** "+ self.title +" *****")
        file_handler.write(self.text_code(input_list)) # write results
        file_handler.close() # close file
