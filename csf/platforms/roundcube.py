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

class RoundcubeParser:
    def get_roundcube_set(self, input_file):
        strings_joined  = '\n'.join(input_file.readlines())
        processed_input = re.sub(r'\\(.)', r'\1', strings_joined)

        # Gather relevant blocks containing messages
        begin = r'this\.add\_message\_row\((.+?)\)\;'

        message_block_regex = re.compile(begin, re.VERBOSE)
        message_tuples = message_block_regex.findall(processed_input)

        # Regex fields for pertinent data extraction in each block
        msg_number = r'(\d+)'
        subject = r'{\"subject\":\"(.+?)\",\"from\"'
        destination = r'title=\"(.+?)\"\sclass'
        date = r'date\":\"(.+?)\",'
        size = r'size":"(.*?)\"}'

        # Full regex for a conversation snippet
        thread_regex = re.compile(
            '.*?'.join([msg_number, subject, destination, date, size]),
            re.VERBOSE )

        # Message blocks' data extraction loop
        results = []

        for t in message_tuples:
            threads = thread_regex.findall(t)
            if len(threads) > 0:
                results.append(threads[0])
                continue

        return set(results)

    def get_roundcube_timeline(self, roundcube_list):
        return sorted(roundcube_list, key=lambda t_list: t_list[0])

    def get_timeline(self, input_file):
        roundcube_list     = self.get_roundcube_set(input_file)
        roundcube_timeline = self.get_roundcube_timeline(roundcube_list)
        return roundcube_timeline

class Output(outputs.OutputFactory):

    def __format_roundcube_message(self, message):
        msg_id   = message[0]
        subject  = message[1]
        dest_id  = message[2]
        datetime = message[3]
        size     = message[4]

        return datetime +\
            " : "+ msg_id + \
            " : "+ subject + \
            " to "+ dest_id +\
            " : " + size

    def text_code(self, input_list):
        if self.verbose:
                print "[*] ROUNDCUBE"
        text = ""
        for roundcube_tuple in input_list:
            message = self.__format_roundcube_message(roundcube_tuple)
            text += message + "\n"
            if self.verbose:
                print "[+]", message
        return text

    def html_code(self, input_list):
        t = outputs.HTML.Table(
                header_row=[
                    'Timestamp',
                    'Email ID',
                    'Subject',
                    'Receiver',
                    'Size',
                ],
                classes="table table-striped"
            )
        for message in input_list:
            msg_id   = message[0]
            subject  = message[1]
            dest_id  = message[2]
            datetime = message[3]
            size     = message[4]
            t.rows.append(
                [datetime, msg_id, subject, dest_id, size])
        return str(t)

class RoundcubePreProcesser:
    # Pre processing of dump file by an identifying field of a relevant block
    def process(self, input_filename, output_file):
        cmd = "grep -E 'add_message_row' " + input_filename
        grep_process = Popen(cmd, stdout=PIPE, shell=True)
        output_file.write(grep_process.communicate()[0])

if __name__ == '__main__':
    roundcube = RoundcubeParser()
    for entry in roundcube.get_roundcube_set(open(sys.argv[1], "r")):
        print entry
