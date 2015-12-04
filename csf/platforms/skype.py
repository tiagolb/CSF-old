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

import sys
import re
from subprocess import Popen, PIPE
import outputs

class SkypeParser:
    def get_skype_set(self, input_file):
        strings_joined  = '\n'.join(input_file.readlines())
        processed_input = re.sub(r'\\(.)', r'\1', strings_joined)

        # Gather relevant blocks containing messages
        begin = r'\{\"eventMessages\"\:\[\{(.+?)\}\}\]\}'

        message_block_regex = re.compile(begin, re.VERBOSE)
        message_tuples = message_block_regex.findall(processed_input)



        # Regex fields for pertinent data extraction in NewMessage block
        resource = r'resourceType\"\:\"NewMessage'
        date = r'time\"\:\"(.+?)Z'
        recipient = r'resourceLink\"\:\"https\:\/\/db3\-client\-s\.gateway\.messenger\.live\.com\/v1\/users\/ME\/conversations\/8\:(\w+)'
        sender = r'from\"\:\"https\:\/\/db3\-client\-s\.gateway\.messenger\.live\.com\/v1\/users\/ME\/contacts\/8\:(\w+)'
        content = r'content\"\:\"(.+?)\"\,\"composetime'

        # Full regex for a NewMessage conversation snippet
        skype_new_message_regex = re.compile(
            '.*?'.join([resource, date, recipient, sender, content]),
            re.VERBOSE | re.DOTALL)

        # Regex fields for pertinent data extraction in ConversationUpdate block
        resource  = r'resourceType\"\:\"ConversationUpdate'
        date      = r'originalarrivaltime\"\:\"(.+?)\.'
        recipient = r'resourceLink\"\:\"https\:\/\/db3\-client\-s\.gateway\.messenger\.live\.com\/v1\/users\/ME\/conversations\/8\:(\w+)'
        sender    = r'(?:from|conversationLink)\"\:\"https\:\/\/db3\-client\-s\.gateway\.messenger\.live\.com\/v1\/users\/ME\/contacts\/8\:(\w+)'
        content   = r'content\"\:\"(.+?)\"\,\"type\"\:'

        # Full regex for a ConversationUpdate conversation snippet
        skype_update_regex = re.compile(
            '.*?'.join([resource, recipient, date, content, sender]),
            re.VERBOSE )

        # Message blocks' data extraction loop
        results = []

        for t in message_tuples:
            skype_tuple = skype_new_message_regex.findall(t)
            if len(skype_tuple) > 0:
                results.append(skype_tuple[0])

            skype_tuple = skype_update_regex.findall(t)
            if len(skype_tuple) > 0:
                arranjed_tuple = (skype_tuple[0][1], skype_tuple[0][0], skype_tuple[0][3], skype_tuple[0][2])
                results.append(arranjed_tuple)

        return set(results)

    def get_skype_timeline(self, skype_list):
        return sorted(skype_list, key=lambda t_list: t_list[0])

    def get_timeline(self, input_file):
        skype_list     = self.get_skype_set(input_file)
        skype_timeline = self.get_skype_timeline(skype_list)
        return skype_timeline

class Output(outputs.OutputFactory):

    def __format_skype_message(self, message):
        datetime  = message[0].replace("T", " - ")
        author_id = message[2]
        dest_id   = message[1]
        return datetime +\
            " by "+ author_id + \
            " to "+ dest_id +\
            " : " + outputs.urldecode(message[3])

    def text_code(self, input_list):
        if self.verbose:
                print "[*] SKYPE"
        text = ""
        for skype_tuple in input_list:
            message = self.__format_skype_message(skype_tuple)
            text += message + "\n"
            if self.verbose:
                print "[+]", message
        return text

    def html_code(self, input_list):
        t = outputs.HTML.Table(
                header_row=[
                    'Timestamp',
                    'Author',
                    'Receiver',
                    'Message',
                ],
                classes="table table-striped"
            )
        for message in input_list:
            datetime  = message[0].replace("T", " - ")
            author_id = message[2]
            dest_id   = message[1]
            t.rows.append(
                [datetime, author_id, dest_id, outputs.urldecode(message[3])])
        return str(t)

class SkypePreProcesser:
    # Pre processing of dump file by an identifying field of a relevant block
    def process(self, input_filename, output_file):
        cmd = "grep -E 'eventMessages' " + input_filename
        grep_process = Popen(cmd, stdout=PIPE, shell=True)
        output_file.write(grep_process.communicate()[0])


if __name__ == '__main__':
    skype = SkypeParser()
    for entry in skype.get_skype_set(open(sys.argv[1], "r")):
        print entry
