RAMAS
=====

 RAM Analysis System, or simply RAMAS, is an extensible carving utility which aims to ease and automate the process of analysing communication records left behind in physical memory by instant-messaging and email web clients. We have developed a forensic framework where the responsibility of creating and updating carving modules for different applications is distributed amongst practitioners. RAMAS also provides a way to inspect results, either by the inspection of forensic timelines or by making available a database which can be queried to unveil sophisticated correlations among the recovered evidence.



Supported Applications
----------------------

RAMAS is able to extract communication records from several web-applications, such as:

* Facebook (and Messenger.com) Chat
* Twitter Direct Messages
* Skype Web Clients
* Roundcube Email Client
* Outlook Email Client

Usage
-----

First off, to setup RAMAS you need to clone the repository and, at the root of the repository, perform the following command:

```
$ pip install -r requirements.txt
```
This installs all the dependencies of RAMAS automatically. This may require root access, in this case perform the same command with the sudo prefix:

```
$ sudo pip install -r requirements.txt
```

To extract data using RAMAS, change directory to `csf/` and execute the tool:

```
$ python ramas.py
```

RAMAS takes as input strings files, obtained from the processing of raw memory images. Strings files can be obtained by running the `strings` utility over raw dumps.

A simple example is depicted below.

```
$ strings RAW_DUMP_FILE > STRINGS_DUMP_FILE
```

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

This tool was initially developed for Forensic Cyber Security course at IST (https://tecnico.ulisboa.pt) under the open-source MIT License (https://opensource.org/licenses/MIT).
Likewise, the improved RAMAS v2.0 was developed in the scope of the Research Topics course at IST.

This tool was tested in a 64-bit Ubuntu 16.04 LTS with python 2.7.12.

This tool uses the `HTML.py` module for html generation (http://www.decalage.info/python/html)

This project has been set up using PyScaffold 2.4.2. For details and usage
information on PyScaffold see http://pyscaffold.readthedocs.org/.
