import HTML
import datetime
import os
import re
from html_assets import *

PLATFORM = {
    "twitter" : 0,
    "facebook" : 1,
}

AUDIT_DIR = "audit_result"
AUDIT_HTML = AUDIT_DIR + "/audit.html"
AUDIT_TEXT = AUDIT_DIR + "/audit.text"

def time_convert(time_long):
    return datetime.datetime.fromtimestamp(
        int(time_long)
    ).strftime('%Y-%m-%d %H:%M:%S')


class OutputFactory(object):

    verbose = False
    targets = []

    def __init__(self, verbose, targets):
        self.verbose = verbose
        self.targets = targets

    def twitter_output(self, input_list): pass

    # In the case of facebook input_list is a list of two input_lists
    def facebook_output(self, input_list): pass

    def append(self, input_list, platform):
        if platform == PLATFORM["twitter"]:
            self.twitter_output(input_list)
        if platform == PLATFORM["facebook"]:
            self.facebook_output(input_list)

class HtmlOutput(OutputFactory):

    def __build_html_header(self, title, targets):
        head = header.header_html(title, targets)
        return head


    def __build_html_footer(self):
        foot = footer.footer_html()
        return foot


    def __init__(self, verbose, targets):
        super(self.__class__, self).__init__(verbose, targets)

        header_code = self.__build_html_header("RAMOS", self.targets)
        footer_code = self.__build_html_footer()
        html_code = """
            <div class="row">
              <div class="col-md-2"></div>
              <div class="col-md-8">
                <h1>RAMOS</h1>
                <h3 class="text-justify">This is RAMOS, a data-carving utility designed to extract data from conversations that took place while using applications such as Facebook, Twitter and more.</h3>
                <h3 class="text-justify">RAMOS was implemented for the Ciber Forensic Security course at Instituto Superior Tecnico and is available at this <a href="https://github.com/tiagolb/CSF">GitHub repository</a>.</h3>

                <h4 class="text-center">
                    <br/>
                    Project by:<br/>
                    Tiago Brito<br/>
                    Diogo Barradas<br/>
                    David Duarte
                </h4>
                </div>
              <div class="col-md-2"></div>
            </div>
        """

        file_handler = open(AUDIT_HTML, "w")
        file_handler.write(header_code)
        file_handler.write(html_code)
        file_handler.write(footer_code)
        file_handler.close()


    def twitter_output(self, input_list):
        t = HTML.Table(
                header_row=[
                    'timestamp',
                    'avatar',
                    'author',
                    'message',
                ],
                classes="table table-striped"
            )
        for message in input_list:
            messenger_id = '<a href="https://twitter.com/'+\
                message[2]+'">' + message[2] +\
                '</a> ('+message[3]+')'
            avatar = '<img src="' + message[4] + '" height="40" width="40" />'
            datetime = time_convert(message[6])
            t.rows.append(
                [datetime, avatar, messenger_id, message[5]])
        html_code = str(t)

        header_code = self.__build_html_header("Twitter", self.targets)
        footer_code = self.__build_html_footer()

        file_handler = open(AUDIT_DIR + "/twitter.html", "w")
        file_handler.write(header_code)
        file_handler.write("<h1>Twitter</h1>")
        file_handler.write(html_code)
        file_handler.write(footer_code)
        file_handler.close()

        if self.verbose:
            print "[*] TWITTER"
            print html_code


    def __facebook_table(self, input_list):
        t = HTML.Table(
                header_row=[
                    'timestamp',
                    'author',
                    'receiver',
                    'message',
                ],
                classes="table table-striped"
            )
        for message in input_list:
            datetime = time_convert(message[1][:-3])
            author_id = '<a href="https://facebook.com/'+\
                message[0]+'">' + message[0] +'</a>'
            dest_id = '<a href="https://facebook.com/'+\
                message[3]+'">' + message[3] +'</a>'
            t.rows.append(
                [datetime, author_id, dest_id, message[2]])
        return str(t)


    def __facebook_threads_table(self, input_list):
        t = HTML.Table(
                header_row=[
                    'timestamp',
                    'author',
                    'receiver (group)',
                    'message',
                    'participants',
                    'former_participants'
                ],
                classes="table table-striped"
            )
        for message in input_list:
            datetime = time_convert(message[6][:-3])
            author_id = '<a href="https://facebook.com/'+\
                message[4]+'">' + message[4] +'</a>'
            dest_id = '<a href="https://facebook.com/'+\
                message[0]+'">' + message[0] +'</a>'

            part = []
            for p in message[1].split(","):
                tp='<a href="https://facebook.com/'+p[6:-1]+'">'+p[6:-1]+'</a>'
                part.append(tp)

            fpart = []
            for fp in message[2].split(","):
                tfp='<a href="https://facebook.com/'+fp[6:-1]+'">'+fp[6:-1]+'</a>'
                fpart.append(tfp)

            participants = HTML.List(
                lines=part,
                attribs={ "class" : "list-unstyled" }
                )
            former_participants = HTML.List(
                lines=fpart,
                attribs={ "class" : "list-unstyled" }
                )

            t.rows.append([
                datetime,
                author_id,
                dest_id,
                message[3],
                participants,
                former_participants])
        return str(t)


    def facebook_output(self, input_list):
        # table for normal facebook conversations
        html_code_1 = self.__facebook_table(input_list[0])
        # table for threaded facebook conversations
        html_code_2 = self.__facebook_threads_table(input_list[1])

        header_code = self.__build_html_header("Facebook", self.targets)
        footer_code = self.__build_html_footer()

        file_handler = open(AUDIT_DIR + "/facebook.html", "w")
        file_handler.write(header_code)
        file_handler.write("<h1>Facebook</h1>")
        file_handler.write(html_code_1)
        file_handler.write("<h1>Facebook Threads</h1>")
        file_handler.write(html_code_2)
        file_handler.write(footer_code)
        file_handler.close()

        if self.verbose:
            print "[*] FACEBOOK"
            print html_code



class TextOutput(OutputFactory):

    def __format_twitter_message(self, message):
        messenger_id = message[2]+"("+message[3]+")"
        datetime = time_convert(message[6])
        formated_message = datetime +\
            " by " + messenger_id +\
            ":"   + message[5]
        return formated_message

    def __format_facebook_message(self, message):
        datetime = time_convert(message[1][:-3])
        author_id = message[0]
        dest_id = message[3]
        return datetime +\
            " by "+ author_id + \
            " to "+ dest_id +\
            " : " + message[2]

    def __format_facebook_threads_message(self, message):
        datetime = time_convert(message[6][:-3])
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


    def twitter_output(self, input_list):
        if self.verbose:
                print "[*] TWITTER"
        file_handler = open(AUDIT_DIR + "/twitter.txt", "w")
        for twitter_tuple in input_list:
            message = self.__format_twitter_message(twitter_tuple)
            file_handler.write(message + "\n")
            if self.verbose:
                print "[+]", message
        file_handler.close()


    def facebook_output(self, input_list):
        if self.verbose:
                print "[*] FACEBOOK"
        file_handler = open(AUDIT_DIR + "/facebook.txt", "w")
        file_handler.write("### FACEBOOK NORMAL ###\n")
        for facebook_tuple_1 in input_list[0]:
            message_1 = self.__format_facebook_message(facebook_tuple_1)
            file_handler.write(message_1 + "\n")
            if self.verbose:
                print "[+]", message_1

        file_handler.write("\n### FACEBOOK THREADS ###\n")
        for facebook_tuple_2 in input_list[1]:
            message_2 = self.__format_facebook_threads_message(facebook_tuple_2)
            file_handler.write(message_2 + "\n")
            if self.verbose:
                print "[+]", message_2

        file_handler.close()

###################################

def __create_directories():
    if not os.path.exists(AUDIT_DIR):
        os.makedirs(AUDIT_DIR)

def create_output_manager(html, verbose, targets):
    __create_directories()
    if html:
        output = HtmlOutput(verbose, targets)
    else:
        output = TextOutput(verbose, targets)
    return output
