#!/usr/bin/env python
import ConfigParser


def readConfig(configFile):
    Config = ConfigParser.ConfigParser()
    Config.read(configFile)

    config_sections = Config.sections()
    if(len(config_sections) == 3):
        if('StartDelimiter' in config_sections and 'EndDelimiter' in config_sections and 'PreProcess' in config_sections):
            start_options = Config.options('StartDelimiter')
            end_options = Config.options('EndDelimiter')
            if('record' in start_options and 'record' in end_options):

                if(start_options == end_options):
                    start_options_values = []
                    for v in start_options:
                        start_options_values.append(Config.get('StartDelimiter',v))

                    end_options_values = []
                    for v in end_options:
                        end_options_values.append(Config.get('EndDelimiter',v))

                    delimiters = []
                    for i, opt in enumerate(start_options):
                        delimiters.append([opt, start_options_values[i], end_options_values[i]])
                    return delimiters

                else:
                    print "Start and End delimiter options must match"
            else:
                print "'Record' option must be defined"
        else:
            print 'Malformed sections: Provide Start/End Delimiters and PreProcess'
    else:
        print 'Malformed sections: Other than two'
