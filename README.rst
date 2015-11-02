===
CSF
===

Add a short description here!


Notes
====
Google Chrome:
Clears data after navigating away to other webpage. (Process which serves the website changes) RAM content is cleared after closing the browser. Messages can still be extracted when user simply logged out of the account (Facebook & Twitter).

Firefox:
Facebook data is scrambled (just after logout & after browsing).
Twitter data can be accessed when user logs out (data is too scrambled after).

Pidgin:
Dumping Pidgin memory/DumpIt while Pidgin is opened works for retrieving messages even if logs are disabled and OTR is used. This probably happens because of some GUI buffer. We may be able to recover only partial messages.
After Pidgin is closed we can not recover anything.

An Observation: we are able to see messages traded with server, other artifacts and HTML logs(if any). Pidgin seems to load logged info on startup.



This project has been set up using PyScaffold 2.4.2. For details and usage
information on PyScaffold see http://pyscaffold.readthedocs.org/.
