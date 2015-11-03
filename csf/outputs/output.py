import HTML

PLATFORM = {
    "twitter" : 0,
}

class OutputFactory:
    def append(self, input_list, platform):
        raise NotImplementedError("Please Implement this method")


class HtmlOutput(OutputFactory):
    def append(self, input_list, platform):
        if platform == PLATFORM["twitter"]:
            t = HTML.Table(
                header_row=[
                    'timestamp',
                    'author',
                    'message']
                )
            for message in input_list:
                messenger_id = message[2]+"("+message[3]+")"
                t.rows.append(
                    [message[6], messenger_id, message[5]])
            htmlcode = str(t)
            print htmlcode


class TextOutput(OutputFactory):

    def format_twitter_message(self, message):
        messenger_id = message[2]+"("+message[3]+")"
        formated_message = message[6] +\
                    " by " + messenger_id +\
                    ":"   + message[5]
        return formated_message

    def append(self, input_list, platform):
        if platform == PLATFORM["twitter"]:
            for message in input_list:
                print "[+]", self.format_twitter_message(message)

def htmlOutput():
    return HtmlOutput()

def textOutput():
    return TextOutput()
