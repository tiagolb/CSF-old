import sys
import re


class TwitterEntry:
    def __init__(self, direction, msg_id, username, user_id, avatar, content, timestamp):
        self.direction = direction
        self.msg_id = msg_id
        self.username = username
        self.user_id = user_id
        self.avatar = avatar
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
        strings_joined = '\n'.join(input_file.readlines())

        processed_input = re.sub(r'\\(.)', r'\1', strings_joined)

        message_type = r'<div.*?DirectMessage--(sent|received).*?data-message-id="(\d+)'
        handler = r'a\s*href="/([^"]+?)".*?data-user-id="(\d+)'
        avatar = r'DMAvatar-image"\s*src="([^"]+?.jpe?g)".'
        content = r'class="TweetTextSize[^>]+?>([^<]+?)<'
        date = r'data-time="(\d+)"'

        talk_regex = re.compile(
            '.*?'.join([message_type, handler, avatar, content, date]),
            re.VERBOSE | re.DOTALL)

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


if __name__ == '__main__':
    twitter = TwitterParser()
    for entry in twitter.get_twitter_set(open(sys.argv[1], "r")):
        print entry
