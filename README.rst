RAMAS
=====

RAM Analysis System


Notes
=====
Google Chrome:
Clears data after navigating away to other webpage. (Process which serves the website changes) RAM content is cleared.
Messages can still be extracted when user simply logged out of the account (Facebook & Twitter) and may or may not closed the browser. Data recovery works even for Private Navigation.

Messenger: 
Recovered sent msg after logOut-CloseBrowser-DumpIt
Business as usual with dump after LogOut

Firefox/Tor:
Facebook data is scrambled (just after logout & after browsing).
Twitter data can be accessed when user logs out, even if browser is closed after (data is scrambled after navigation).

Internet Explorer 11:
Mobile Twitter Version = 0 extraction
No Facebook data

Pidgin:
Dumping Pidgin memory/DumpIt while Pidgin is opened works for retrieving messages even if logs are disabled and OTR is used. This probably happens because of some GUI buffer. We may be able to recover only partial messages.

After Pidgin is closed we can not recover anything.

An Observation (NOT REGEX EXTRACTED, JUST CUTE): we are able to see messages traded with server, other artifacts and HTML logs(if any). Pidgin seems to load logged info on startup.

Telegram:
Cannot recover any structure of Telegram, let it be on Chrome/Firefox/DesktopApp

WhatsApp:
Cannot recover any structure of WhatsApp, Chrome/Firefox

Roundcube:
We are able to recover email headers in a structured way - Chrome

Skype:
Nope.

MiRC:
Algumas cenas, look into it

Twitter:
Whenever filtering the memory dump, please use: `grep -E "DirectMessage|DM|data-user-id"`

This project has been set up using PyScaffold 2.4.2. For details and usage
information on PyScaffold see http://pyscaffold.readthedocs.org/.
