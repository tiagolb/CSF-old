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

class FacebookThreadsParser:
    def get_facebook_threads_set(self, input_file):
        strings_joined  = '\n'.join(input_file.readlines())
        processed_input = re.sub(r'\\(.)', r'\1', strings_joined)

        # Gather relevant blocks containing messages
        begin = r'{\"thread_id\":(.+?)titan_originated_thread_id'

        message_block_regex = re.compile(begin, re.VERBOSE | re.DOTALL)

        message_tuples = message_block_regex.findall(processed_input)


        # Regex fields for pertinent data extraction in each block
        handler   = r'\"snippet_sender\":\"fbid:(\d+)'
        date      = r'\"timestamp\":(\d+)'
        content   = r'\"snippet\":\"(.*?)\",\"snippet_has_attachment'
        recipient = r'\"thread_fbid\":\"(\d+)'
        participants  = r'\"participants\":\[(.+?)\],'
        message_count = r'\"message_count\":(\d+)'
        former_participants = r'\"former_participants\":\[(.*?)\],'

        # Full regex for a conversation snippet
        thread_regex = re.compile(
            '.*?'.join([recipient, participants, former_participants, content, handler, message_count, date]),
            re.VERBOSE | re.DOTALL)

        # Message blocks' data extraction loop
        results = []

        for t in message_tuples:
            threads = thread_regex.findall(t)
            if len(threads) > 0:
                results.append(threads[0])

        return set(results)

    def get_facebook_threads_timeline(self, facebook_threads_list):
        return sorted(facebook_threads_list, key=lambda t_list: t_list[6])

    def get_timeline(self, input_file):
        facebook_threads_list     = self.get_facebook_threads_set(input_file)
        facebook_threads_timeline = self.get_facebook_threads_timeline(facebook_threads_list)
        return facebook_threads_timeline

class Output(outputs.OutputFactory):

    def __format_facebook_threads_message(self, message):
        datetime = outputs.time_convert(message[6][:-3])
        author_id = message[4]
        dest_id = message[0]

        participants = []
        for p in message[1].split(","):
            participants.append(p[6:-1])

        former_participants = []
        for fp in message[2].split(","):
            former_participants.append(fp[6:-1])

        return datetime + " by " + author_id + " to " + dest_id + " : " +\
            message[3] +", with these participants: " + str(participants) +\
            " and these former participants: " + str(former_participants)

    def text_code(self, input_list):
        if self.verbose:
                print "[*] FACEBOOK THREADS"
        text = ""
        for facebook_tuple in input_list:
            message = self.__format_facebook_threads_message(facebook_tuple)
            text += message + "\n"
            if self.verbose:
                print "[+]", message
        return text

    def html_code(self, input_list):
        t = outputs.HTML.Table(
                header_row=[
                    'Timestamp',
                    'Author',
                    'Receiver (group)',
                    'Message',
                    'Participants',
                    'Former Participants',
                    'Count'
                ],
                classes="table table-striped"
            )
        for message in input_list:
            datetime  = outputs.time_convert(message[6][:-3])
            author_id = '<a href="https://facebook.com/'+\
                message[4]+'">' + message[4] +'</a>'
            dest_id   = '<a href="https://facebook.com/'+\
                message[0]+'">' + message[0] +'</a>'
            count     = message[5]

            part = []
            for p in message[1].split(","):
                tp = '<a href="https://facebook.com/'+p[6:-1]+'">'+p[6:-1]+'</a>'
                part.append(tp)

            fpart = []
            for fp in message[2].split(","):
                tfp = '<a href="https://facebook.com/'+fp[6:-1]+'">'+fp[6:-1]+'</a>'
                fpart.append(tfp)

            participants = outputs.HTML.List(
                lines = part,
                attribs = { "class" : "list-unstyled" }
                )
            former_participants = outputs.HTML.List(
                lines = fpart,
                attribs = { "class" : "list-unstyled" }
                )

            t.rows.append([
                datetime,
                author_id,
                dest_id,
                message[3],
                participants,
                former_participants,
                count])
        return str(t)

class FacebookThreadsPreProcesser:
    # Pre processing of dump file by an identifying field of a relevant block
    def process(self, input_filename, output_file):
        cmd = "grep -E 'fbid' " + input_filename
        grep_process = Popen(cmd, stdout=PIPE, shell=True)
        output_file.write(grep_process.communicate()[0])


if __name__ == '__main__':
    facebook_threads = FacebookThreadsParser()
    for entry in facebook_threads.get_facebook_threads_set(open(sys.argv[1], "r")):
        print entry
