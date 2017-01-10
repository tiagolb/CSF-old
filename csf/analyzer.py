#!/usr/bin/env python
'''
The MIT License (MIT)

Copyright (c) 2015 Tiago Brito

Permission is hereby granted, free of charge, to any person obtaining a copy of this software
and associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT
OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

__author__ = "Tiago Brito, Diogo Barradas, David Duarte"
__copyright__ = "Copyright 2015, Tiago Brito"
__credits__ = ["Tiago Brito", "Diogo Barradas", "David Duarte"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Tiago Brito"
__email__ = "tiago.de.oliveira.brito@tecnico.ulisboa.pt"
__status__ = "Production"


from outputs import Output
import shutil, os, sys
import tempfile
import threading
import re
import sqlite3 as lite
import random

from models.messageModel import MessageModel
from subprocess import Popen, PIPE
from moduleConfigParser import readConfig
from moduleConfigParser import readRecordFields
from moduleConfigParser import readPreProcessorConfig

dbName = 'ramas.db'
class Analyzer():
    def __rreplace(self, s, old, new, occurrence):
        li = s.rsplit(old, occurrence)
        return new.join(li)

    def __insertMessage(self, records, recordFields, module):
        try:
            dbCon = lite.connect(dbName)
        except lite.Error, e:
            print "Error connecting to Database"
            #TODO Signal error up to the Interface

        cur = dbCon.cursor()

        #Build query for inserting records in the respective module table
        for record in records:
            query = "INSERT INTO " + module + "_MSG (DUMP_HASH, CASE_NAME,"
            for n,field in enumerate(recordFields):
                if(n < len(recordFields)-1):
                    query += field + ", "
                else:
                    query += field + ") VALUES ("
                    for i in range(0,len(recordFields)):
                        if(i < len(recordFields)-1):
                            query += "?, "
                        else:
                            query += "?,?,?)"

        #Add current image + current case to the record fields
        base = (str(self.fileHash),str(self.currentCase))
        for record in records:
            values = base + record
            cur.execute(query, values)

        dbCon.commit()


    def __get_module_records(self,input_file_handler, module):
        strings_joined  = '\n'.join(input_file_handler.readlines())

        processed_input = re.sub(r'\\(.)', r'\1', strings_joined)

        delimiters = readConfig("platforms/" + module + ".cfg")

        # Gather relevant blocks containing messages
        begin = re.escape(delimiters[0][1]) + r'(.+?)' + re.escape(delimiters[0][2])

        message_block_regex = re.compile(begin, re.VERBOSE | re.DOTALL)

        message_tuples = message_block_regex.findall(processed_input)

        #Change delimiters
        nonce = random.randint(0,100000) #generate rand delimiter
        tag = "RAMAS" + str(nonce)
        random_delim = tag


        for m, t in enumerate(message_tuples):
            for opt in delimiters[1:]:
                if(opt[0] == "content"):
                    message_tuples[m] = message_tuples[m].replace(opt[1], random_delim, 1)      #replace start delimiter for field
                    message_tuples[m] = self.__rreplace(message_tuples[m], opt[2], random_delim, 1) #replace end delimiter for field

        #print "Caught full records:"
        #print message_tuples[0]
        #print len(message_tuples)


        fields = []
        for opt in delimiters[1:]:
            if(opt[0] != "content"):
                fields.append(re.escape(opt[1]) + r'(.*?)' + re.escape(opt[2]))
            else:
                fields.append(random_delim + r'(.*?)' + random_delim)

        # Full regex for a conversation snippet
        thread_regex = re.compile(
            '.*?'.join(fields),
            re.VERBOSE | re.DOTALL)

        # Message blocks' data extraction loop
        results = []

        for t in message_tuples:
            threads = thread_regex.findall(t)
            if len(threads) > 0:
                results.append(threads[0])
        #print results
        return set(results)


    def __process(self,module, output_file):
        keyword = readPreProcessorConfig("platforms/" + module + ".cfg")
        cmd = "grep -E '" + keyword + "' " + self.filename
        grep_process = Popen(cmd, stdout=PIPE, shell=True)
        output_file.write(grep_process.communicate()[0])


    def __modular_processing(self,module):
        prefix = "ramas_"

        #create a temporary file in /tmp for this module
        temp_tuple   = tempfile.mkstemp(suffix=".dump", prefix=prefix)
        temp_handler = open(temp_tuple[1], "w+") # open the file

        self.__process(module, temp_handler) # preprocess the file
        temp_handler.seek(0) # go back to the beginning of the file

        # parse the file (extract information)
        records = self.__get_module_records(temp_handler, module)
        temp_handler.close() # close the file

        #output operations
        output_gen = Output()
        output_gen.setup(self.fileHash, module, self.modules)
        recordFields = readRecordFields("platforms/" + module + ".cfg")

        self.__insertMessage(records, recordFields, module)
        output_gen.out(records, recordFields)

    def setup(self,modules, filename, fileHash, currentCase):
        self.filename = filename
        self.fileHash = fileHash
        self.modules = modules
        self.currentCase = currentCase

    def analysisLoop(self):
            threads = []
            # for every module (target) a thread is created ant the function __modular_processing is called
            for module in self.modules:
                t = threading.Thread(
                        target=self.__modular_processing,
                        args=[module])
                t.start()
                # threads are appended to this list so they can be joined next
                threads.append(t)
            for thread in threads:
                thread.join()