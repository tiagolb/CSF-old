#!/usr/bin/env python
import ConfigParser


def readConfig(configFile):
    Config = ConfigParser.ConfigParser()
    Config.read(configFile)

    config_sections = Config.sections()
    if(len(config_sections) == 5):
        if('StartDelimiter' in config_sections and 'EndDelimiter' in config_sections and
            'PreProcess' in config_sections and 'Info' in config_sections):
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
                    return False
            else:
                print "'Record' option must be defined"
                return False
        else:
            print 'Malformed sections: Provide Start/End Delimiters and PreProcess'
            return False
    else:
        print 'Malformed sections: Other than five. Ensure you define Info, StartDelimiter, EndDelimiter, PreProcess and Mediator'
        return False

def readModuleInfo(configFile):
    Config = ConfigParser.ConfigParser()
    Config.read(configFile)

    name = Config.get('Info','name')
    desc = Config.get('Info','description')
    return name, desc

def readRecordFields(configFile):
    Config = ConfigParser.ConfigParser()
    Config.read(configFile)
    return Config.options('StartDelimiter')[1:]

def readPreProcessorConfig(configFile):
    Config = ConfigParser.ConfigParser()
    Config.read(configFile)

    config_sections = Config.sections()
    if('PreProcess' in config_sections):
        preProcess_options = Config.options('PreProcess')
        if(len(preProcess_options) == 1 and 'keyword' in preProcess_options):
            return Config.get('PreProcess','keyword')

def readMediatorInfo(configFile):
    Config = ConfigParser.ConfigParser()
    Config.read(configFile)
    return Config.get('Mediator','date')
