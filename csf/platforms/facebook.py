import sys
import re


class FacebookParser:
    def get_facebook_set(self, input_file):
        strings_joined = '\n'.join(input_file.readlines())

        processed_input = re.sub(r'\\(.)', r'\1', strings_joined)

        # Input split into message blocks tuples
        begin = r'\[thread_id\]&message_batch\[0\](.+?)&client=mercury'

        message_block_regex = re.compile(begin, re.VERBOSE | re.DOTALL)

        message_tuples = message_block_regex.findall(processed_input)

        # Regex for intel extraction from each tuple
        handler = r'\[author\]=fbid%3A(\d+)'
        date = r'\[timestamp\]=(\d+)'
        content = r'\[body\]=(.+?)&message_batch'
        single_recipient = r'\[other_user_fbid\]=(\d+)'
        group_recipient = r'\[thread_fbid\]=(\d+)'

        single_talk_regex = re.compile(
            '.*?'.join([handler, date, content, single_recipient]),
            re.VERBOSE | re.DOTALL)

        group_talk_regex = re.compile(
            '.*?'.join([handler, date, content, group_recipient]),
            re.VERBOSE | re.DOTALL)

        results = []

        for t in message_tuples:
            single_talk = single_talk_regex.findall(t)
            if len(single_talk) > 0:
                results.append(single_talk[0])
                continue
            else:
                group_talk = group_talk_regex.findall(t)
                if len(group_talk) > 0:
                    results.append(group_talk[0])

        return set(results)

    def get_facebook_timeline(self, facebook_list):
        return sorted(facebook_list, key=lambda t_list: t_list[1])

    def get_timeline(self, input_file):
        facebook_list     = self.get_facebook_set(input_file)
        facebook_timeline = self.get_facebook_timeline(facebook_list)
        return facebook_timeline


if __name__ == '__main__':
    facebook = FacebookParser()
    for entry in facebook.get_facebook_set(open(sys.argv[1], "r")):
        print entry
