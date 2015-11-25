import sys
import re
import outputs
from subprocess import Popen, PIPE

class TwitterEntry:
    def __init__(self, direction, msg_id, username, user_id, avatar, content, timestamp):
        self.direction = direction
        self.msg_id = msg_id
        self.username = username
        self.user_id = user_id
        self.avatar = re.sub(r'\\(.)', r'\1', avatar)
        self.content = content
        self.timestamp = timestamp

    def __eq__(self, other):
        return self.timestamp == other.timestamp and self.content == other.content

    def __hash__(self):
        return hash((self.timestamp, self.content))

    def __str__(self):
        return self.direction + ", " + self.msg_id + ", " + self.username + ", " + self.user_id + ", " + self.avatar + \
               ", " + self.content + ", " + self.timestamp


class TwitterParser:

    def get_twitter_set(self, input_file):
        processed_input = '\n'.join(input_file.readlines())

        # processed_input = re.sub(r'\\(.)', r'\1', joined_strings)

        # message_type = r'\\u003cdiv.*?DirectMessage--(sent|received).*?data-message-id=\\"(\d+)'
        # handler = r'a\s*href=\\"\\/([^"]+?)\\".*?data-user-id=\\"(\d+)'
        # avatar = r'DMAvatar-image\\"\s*src=\\"([^"]+?.jpe?g)\\"'
        # content = r'class=\\"TweetTextSize.+?(?:\\u003e)(.+?)(?:\\u003c)'
        # date = r'data-time=\\"(\d+)\\"'

        message_type = r'<div\sclass="DirectMessage\s+DirectMessage--(sent|received).*?data-message-id="(\d+)'
        handler = r'a\s*href="/([^"]+?)".*?data-user-id="(\d+)'
        avatar = r'DMAvatar-image"\s*src="([^"]+?.jpe?g)"'
        content = r'class="TweetTextSize[^>]+?>([^<]+?)<'
        date = r'data-time="(\d+)"'

        talk_regex = re.compile('.*?'.join([message_type, handler, avatar, content, date]), re.VERBOSE | re.DOTALL)

        talk = set(map(lambda t: TwitterEntry(t[0], t[1], t[2], t[3], t[4], t[5], t[6]),
                       talk_regex.findall(processed_input)))

        return map(lambda t: (t.direction, t.msg_id, t.username, t.user_id, t.avatar, t.content, t.timestamp), talk)

    def get_twitter_timeline(self, twitter_set):
        twitter_list = list(twitter_set)
        return sorted(twitter_list, key=lambda t_list: t_list[6])

    def get_timeline(self, input_file):
        twitter_set      = self.get_twitter_set(input_file)
        twitter_timeline = self.get_twitter_timeline(twitter_set)
        return twitter_timeline


class Output(outputs.OutputFactory):

    def __format_twitter_message(self, message):
        messenger_id = message[2]+"("+message[3]+")"
        datetime = outputs.time_convert(message[6])
        formated_message = datetime +\
            " by " + messenger_id +\
            ":"   + message[5]
        return formated_message

    def text_code(self, input_list):
        if self.verbose:
                print "[*] TWITTER"
        text = ""
        for twitter_tuple in input_list:
            message = self.__format_twitter_message(twitter_tuple)
            text += message + "\n"
            if self.verbose:
                print "[+]", message
        return text

    def html_code(self, input_list):
        t = outputs.HTML.Table(
                header_row=[
                    'Timestamp',
                    'Avatar',
                    'Author',
                    'Message',
                ],
                classes="table table-striped"
            )
        for message in input_list:
            messenger_id = '<a href="https://twitter.com/'+\
                message[2]+'">' + message[2] +\
                '</a> ('+message[3]+')'
            avatar = '<img src="' + message[4] + '" height="40" width="40" />'
            datetime = outputs.time_convert(message[6])
            t.rows.append(
                [datetime, avatar, messenger_id, message[5]])
        html_code = str(t)
        return html_code

class TwitterPreProcesser:
    def process(self, input_filename, output_file):
        #print input_file.name, output_file.name
        cmd = "grep -E 'DirectMessage|DM|data-user-id' " + input_filename
        #print cmd
        grep_process = Popen(cmd, stdout=PIPE, shell=True)
        output_file.write(grep_process.communicate()[0])
        #print "done"

if __name__ == '__main__':
    twitter = TwitterParser()
    for entry in twitter.get_twitter_set(open(sys.argv[1], "r")):
        print entry
