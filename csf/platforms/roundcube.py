import sys
import re

class RoundcubeParser:
    def get_roundcube_set(self, input_file):
        strings_joined = '\n'.join(input_file.readlines())

        processed_input = re.sub(r'\\(.)', r'\1', strings_joined)

        # Input split into message blocks tuples
        begin = r'this\.add\_message\_row\((.+?)\)\;'

        message_block_regex = re.compile(begin, re.VERBOSE)

        message_tuples = message_block_regex.findall(processed_input)
        for i in message_tuples:
            print i+"\n"
             
        # Regex for intel extraction from each tuple
        msg_number = r'(\d+)'
        subject = r'{\"subject\":\"(.+?)\",\"from\"'
        destination = r'title=\"(.+?)\"\sclass'
        date = r'date\":\"(.+?)\",'
        size = r'size":"(.*?)\"}'
        
        thread_regex = re.compile(
            '.*?'.join([msg_number, subject, destination, date, size]),
            re.VERBOSE | re.DOTALL)

        results = []

        for t in message_tuples:
            print t
            threads = thread_regex.findall(t)
            results.append(threads[0])

        return set(results)

    def get_roundcube_timeline(self, roundcube_list):
        return sorted(roundcube_list, key=lambda t_list: t_list[0])

    def get_timeline(self, input_file):
        roundcube_list     = self.get_roundcube_set(input_file)
        roundcube_timeline = self.get_roundcube_timeline(roundcube_list)
        return roundcube_timeline

class Output(outputs.OutputFactory):

    def __format_roundcube_message(self, message):
        msg_id = message[0]
        subject = message[1]
        dest_id = message[2]
        datetime = message[3]
        size = message[4]

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
            msg_id = message[0]
            subject = message[1]
            dest_id = message[2]
            datetime = message[3]
            size = message[4]
            t.rows.append(
                [datetime, msg_id, subject, dest_id, size])
        return str(t)

if __name__ == '__main__':
    roundcube = RoundcubeParser()
    for entry in roundcube.get_roundcube_set(open(sys.argv[1], "r")):
        print entry
