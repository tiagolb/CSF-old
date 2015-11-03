import sys
import re


class TwitterParser:
    def get_twitter_set(self, input_file):
        strings_joined = '\n'.join(input_file.readlines())

        processed_input = re.sub(r'\\(.)', r'\1', strings_joined)

        # talk_id = r'(conversation":{"id":"\d+-\d+)?"'
        message_type = r'<div.*?DirectMessage--(sent|received).*?data-message-id="(\d+)'
        handler = r'a\s*href="/([^"]+?)".*?data-user-id="(\d+)'
        avatar = r'DMAvatar-image"\s*src="([^"]+?)".'
        content = r'class="TweetTextSize[^>]+?>([^<]+?)<'
        date = r'data-time="(\d+)"'

        talk_regex = re.compile(
            '.*?'.join([message_type, handler, avatar, content, date]),
            re.VERBOSE | re.DOTALL)

        talk = talk_regex.findall(processed_input)
        return set(talk)


    def get_twitter_timeline(self, twitter_set):
        twitter_list = list(twitter_set)
        return sorted(twitter_list, key=lambda t_list: t_list[6])

    def get_timeline(self, input_file):
        twitter_set      = self.get_twitter_set(input_file)
        twitter_timeline = self.get_twitter_timeline(twitter_set)
        return twitter_timeline


if __name__ == '__main__':
    twitter = TwitterParser()
    for entry in twitter.get_twitter_set(open(sys.argv[1], "r")):
        print entry
