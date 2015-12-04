RAMAS
=====

RAM Analysis System is an extensible memory forensics analysis tool for linux which is able to capture useful data from instant-messaging and email client applications through the matching of regular expressions. Although we employ a general memory data carving approach, we argue that our tool is a valuable asset in a digital forensic investigator's kit, so as to ease the automatic extraction of relevant communication data. To the best of our knowledge, this is the only available tool aimed at extracting and building a timeline of the communications taken forth by a given suspect.


Supported Applications
----------------------

As of this moment the supported (of the shelf) applications are the following:

* Facebook Chat Messages (and Messenger)
* Twitter Direct Messages
* Skype Web Client
* Roundcube Email Client
* Pidgin Desktop Client

Usage
-----

First off, to setup RAMAS you need to clone the repository and, at the root of the repository, perform the following command:

```
$ pip install -r requirements.txt
```
This installs all the dependencies of RAMAS automatically. This may require root access, in this case perfrom the same command with the sudo prefix:

```
$ sudo pip install -r requirements.txt
```

To extract data using RAMAS, change directory to `csf/` and check the following command for help:

```
$ python ramas.py extract --help
```

To extract the memory dump we suggest the use of DumpIt, a tool for Windows which was used for the development of this system.
DumpIt generates a RAW dump file which can then be given as input to strings (linux CLI program) so it can extract the strings to another file which can then be given as input RAMAS.

A simple example to extract chat messages from Facebook and present the results with HTML:

```
$ strings RAW_DUMP_FILE > STRINGS_DUMP_FILE
```

```
$ python ramas.py extract -f STRINGS_DUMP_FILE -t facebook --html --threads
```

After this command is executed, a folder called `audit_result/` is created and in it are the results of this audit. If the HTML flag is used, then a file called audit.html is generated as an entry point for the results.


Extension Development
---------------------

To develop new modules for RAMAS, the following command is available:

```
$ python ramas.py create
```

This command creates a directory called external/ which contains two files:

- project
    * `ramas.py`
    * (...)
    * external/
        * `__init__.py`  
        * `newModule.py`

Both of these files need to be edited so the new module can be installed. Rename `newModule.py` file to whatever name you desire and modify the three classes which compose RAMAS' API:

```python
import outputs

class NewModulePreProcessor:
    def process(self, input_filename, output_file):
        # to be implemented

class NewModuleParser:
    def get_timeline(self, input_file):
        # to be implemented

class NewModuleOutput(outputs.OutputFactory):
    def text_code(self, input_list):
        # to be implemented

    def html_code(self, input_list):
        # to be implemented
```

You can edit the name of these classes but not the name of these functions!

Next you'll need to edit the `__init__.py` file with the following:

```python
import newModule
MODULES = {
  'newModule' : [
    newModule.NewModuleParser(),
    newModule.NewModuleOutput(),
    newModule.NewModulePreProcessor()
  ]
}
```

Where you replace newModule with the name you have given to the module file. After this you can execute the following command:

```
$ python ramas.py extract --help
```

to check if the new module is installed.


Testing
-------

If you want to test RAMAS we suggest you use the following file:
[Dump in DropBox](https://www.dropbox.com/s/6s90z940wxozm8z/ultimateDump?dl=0)
This file was used during testing and represents a fairly large dump from a 4GB machine preprocessed to a smaller size using the strings program. It can be directly used in RAMAS.

Note that the result of analysing this memory dump does not show results for skype, as there is no information regarding this application in the dump.


Documentation
-------------

To generate python documentation in this project you must run the following command whilst in the root of the project:
```
$ python setup.py docs
```
The Sphinx documentation will then be available at `docs/_build/html`.


Authors
-------

@tiagolb
@dmbb
@magicknot

Notes
-----

This tool was developed for Forensic Cyber Security course at IST (https://tecnico.ulisboa.pt) and is licensed under the open-source MIT License (https://opensource.org/licenses/MIT).

This tool was tested for dumps from the Chrome Web Browser running on a Windows 7 machine.
This tool was tested in a 64-bit Ubuntu 14.04 LTS with python 2.7.6.

This tool uses the `HTML.py` module for html generation (http://www.decalage.info/python/html)

This project has been set up using PyScaffold 2.4.2. For details and usage
information on PyScaffold see http://pyscaffold.readthedocs.org/.
