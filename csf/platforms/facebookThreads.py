import sys
import re

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


if __name__ == '__main__':
    facebook_threads = FacebookThreadsParser()
    for entry in facebook_threads.get_facebook_threads_set(open(sys.argv[1], "r")):
        print entry
