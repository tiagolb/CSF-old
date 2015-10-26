#!/usr/bin/env python
import argparse


class DefaultListAction(argparse.Action):
    CHOICES = ['twitter', 'facebook', 'gmail', 'pidgin']
    def __call__(self, parser, namespace, values, option_string=None):
        if values:
            for value in values:
                if value not in self.CHOICES:
                    message = ("invalid choice: {0!r} (choose from {1})"
                               .format(value,
                                       ', '.join([repr(action)
                                                  for action in self.CHOICES])))

                    raise argparse.ArgumentError(self, message)
            setattr(namespace, self.dest, values)

def main():
    #Argument Parsing & Program Info
    parser = argparse.ArgumentParser(
        usage='%(prog)s -f <dump file>',
        description='%(prog)s is a memory data carving program.')
    parser.add_argument('-V', '--version', action='version', version='%(prog)s 1')
    parser.add_argument('-f', '--file', nargs=1, required=True, help='Raw memory dump file.')
    parser.add_argument('--html', action='store_true', help='HTML output flag.')
    parser.add_argument('-t', '--target', nargs='+', action=DefaultListAction,
        default=DefaultListAction.CHOICES) 
    args = parser.parse_args()

    print args.file[0]
    
    if args.target:
        for target in args.target:
            print target

if __name__ == "__main__":
    main()
