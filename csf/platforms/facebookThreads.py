import sys
import re
from subprocess import Popen, PIPE
import outputs

class FacebookThreadsParser:
    def get_facebook_threads_set(self, input_file):
        strings_joined = '\n'.join(input_file.readlines())

        processed_input = re.sub(r'\\(.)', r'\1', strings_joined)

        # Input split into message blocks tuples
        begin = r'{\"thread_id\":(.+?)titan_originated_thread_id'

        message_block_regex = re.compile(begin, re.VERBOSE | re.DOTALL)

        message_tuples = message_block_regex.findall(processed_input)
        """
        for i in message_tuples:
            print i+"\n"
        """
        # Regex for intel extraction from each tuple
        handler = r'\"snippet_sender\":\"fbid:(\d+)'
        date = r'\"timestamp\":(\d+)'
        content = r'\"snippet\":\"(.+?)\",\"snippet_has_attachment'
        recipient = r'\"thread_fbid\":\"(\d+)'
        participants = r'\"participants\":\[(.+?)\],'
        former_participants = r'\"former_participants\":\[(.*?)\],'
        message_count = r'\"message_count\":(\d+)'

        thread_regex = re.compile(
            '.*?'.join([recipient, participants, former_participants, content, handler, message_count, date]),
            re.VERBOSE | re.DOTALL)

        results = []

        for t in message_tuples:
            threads = thread_regex.findall(t)
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
            datetime = outputs.time_convert(message[6][:-3])
            author_id = '<a href="https://facebook.com/'+\
                message[4]+'">' + message[4] +'</a>'
            dest_id = '<a href="https://facebook.com/'+\
                message[0]+'">' + message[0] +'</a>'
            count = message[5]

            part = []
            for p in message[1].split(","):
                tp='<a href="https://facebook.com/'+p[6:-1]+'">'+p[6:-1]+'</a>'
                part.append(tp)

            fpart = []
            for fp in message[2].split(","):
                tfp='<a href="https://facebook.com/'+fp[6:-1]+'">'+fp[6:-1]+'</a>'
                fpart.append(tfp)

            participants = outputs.HTML.List(
                lines=part,
                attribs={ "class" : "list-unstyled" }
                )
            former_participants = outputs.HTML.List(
                lines=fpart,
                attribs={ "class" : "list-unstyled" }
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
    def process(self, input_filename, output_file):
        #print input_file.name, output_file.name
        cmd = "grep -E 'fbid' " + input_filename
        #print cmd
        grep_process = Popen(cmd, stdout=PIPE, shell=True)
        output_file.write(grep_process.communicate()[0])
        #print "done"


if __name__ == '__main__':
    facebook_threads = FacebookThreadsParser()
    for entry in facebook_threads.get_facebook_threads_set(open(sys.argv[1], "r")):
        print entry
