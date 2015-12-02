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

import outputs
import sys
import re
from subprocess import Popen, PIPE


class PidginParser:
    def get_pidgin_set(self, input_file):
        strings_joined = '\n'.join(input_file.readlines())

        processed_input = re.sub(r'\\(.)', r'\1', strings_joined)

        
        pidgin_exp = r':[0-9][0-9]:[0-9][0-9]\s(?:P|A)M\)\s.+:.+'
                   

        pidgin_regex = re.compile(pidgin_exp, re.VERBOSE)

        message_tuples = pidgin_regex.findall(processed_input)

        # Regex for intel extraction from each tuple
        partial_date = r'(.+?)\)'
        sender = r'\s(.+?):'
        content = r'(.+)'

        thread_regex = re.compile(
            '.*?'.join([partial_date, sender, content]),
            re.VERBOSE )

        results = []

        for t in message_tuples:
            threads = thread_regex.findall(t)
            if len(threads) > 0:
                results.append(threads[0])
                continue

        return set(results)

    def get_pidgin_timeline(self, pidgin_list):
        return sorted(pidgin_list, key=lambda t_list: t_list[0])

    def get_timeline(self, input_file):
        pidgin_list     = self.get_pidgin_set(input_file)
        pidgin_timeline = self.get_pidgin_timeline(pidgin_list)
        return pidgin_timeline

class Output(outputs.OutputFactory):

    def __format_pidgin_message(self, message):
        partial_date = message[0]
        sender = message[1]
        content = message[2]

        return partial_date +\
            " : "+ sender + \
            " : "+ content

    def text_code(self, input_list):
        if self.verbose:
                print "[*] PIDGIN"
        text = ""
        for pidgin_tuple in input_list:
            message = self.__format_pidgin_message(pidgin_tuple)
            text += message + "\n"
            if self.verbose:
                print "[+]", message
        return text

    def html_code(self, input_list):
        t = outputs.HTML.Table(
                header_row=[
                    'Partial Date',
                    'Sender',
                    'Content',
                ],
                classes="table table-striped"
            )
        for message in input_list:
            partial_date = "--" + message[0]
            sender = message[1]
            content = message[2]
            t.rows.append(
                [partial_date, sender, content])
        return str(t)

class PidginPreProcesser:
    def process(self, input_filename, output_file):
        #print input_file.name, output_file.name
        cmd = "grep -E ':[0-9][0-9]:[0-9][0-9]' " + input_filename
        #print cmd
        grep_process = Popen(cmd, stdout=PIPE, shell=True)
        output_file.write(grep_process.communicate()[0])
        #print "done"


if __name__ == '__main__':
    pidgin = PidginParser()
    for entry in pidgin.get_pidgin_set(open(sys.argv[1], "r")):
        print entry
