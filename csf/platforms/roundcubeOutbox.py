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

class RoundcubeOutboxParser:
    def get_roundcube_outbox_set(self, input_file):
        strings_joined = '\n'.join(input_file.readlines())

        processed_input = re.sub(r'\\(.)', r'\1', strings_joined)

        # Input split into message blocks tuples
        begin = r'this\.add\_message\_row\((.+?)\)\;'

        message_block_regex = re.compile(begin, re.VERBOSE)

        message_tuples = message_block_regex.findall(processed_input)

        # Regex for intel extraction from each tuple
        msg_number = r'(\d+)'
        subject = r'{\"subject\":\"(.+?)\",\"to\"'
        destination = r'title=\"(.+?)\"\sclass'

        thread_regex = re.compile(
            '.*?'.join([msg_number, subject, destination]),
            re.VERBOSE | re.DOTALL)

        results = []

        for t in message_tuples:
            threads = thread_regex.findall(t)
            if len(threads) > 0:
                results.append(threads[0])
                continue

        return set(results)

    def get_roundcube_outbox_timeline(self, roundcube_outbox_list):
        return sorted(roundcube_outbox_list, key=lambda t_list: t_list[0])

    def get_timeline(self, input_file):
        roundcube_outbox_list     = self.get_roundcube_outbox_set(input_file)
        roundcube_outbox_timeline = self.get_roundcube_outbox_timeline(roundcube_outbox_list)
        return roundcube_outbox_timeline

class Output(outputs.OutputFactory):

    def __format_roundcube_outbox_message(self, message):
        msg_id = message[0]
        subject = message[1]
        dest_id = message[2]

        return msg_id + \
            " : "+ subject + \
            " to "+ dest_id

    def text_code(self, input_list):
        if self.verbose:
                print "[*] ROUNDCUBE OUTBOX"
        text = ""
        for roundcube_outbox_tuple in input_list:
            message = self.__format_roundcube_outbox_message(roundcube_outbox_tuple)
            text += message + "\n"
            if self.verbose:
                print "[+]", message
        return text

    def html_code(self, input_list):
        t = outputs.HTML.Table(
                header_row=[
                    'Email ID',
                    'Subject',
                    'Receiver',
                ],
                classes="table table-striped"
            )
        for message in input_list:
            msg_id = message[0]
            subject = message[1]
            dest_id = message[2]
            t.rows.append(
                [msg_id, subject, dest_id])
        return str(t)

class RoundcubePreProcesser:
    def process(self, input_filename, output_file):
        #print input_file.name, output_file.name
        cmd = "grep -E 'add_message_row' " + input_filename
        #print cmd
        grep_process = Popen(cmd, stdout=PIPE, shell=True)
        output_file.write(grep_process.communicate()[0])
        #print "done"

if __name__ == '__main__':
    roundcube_outbox = RoundcubeOutboxParser()
    for entry in roundcube.get_roundcube_outbox_set(open(sys.argv[1], "r")):
        print entry
