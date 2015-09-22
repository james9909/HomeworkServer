HomeworkServer
==============

Script to quickly upload/download files to/from the CS Homework Server.

```
usage: homeworkserver [-h] [-s FILE] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -s FILE, --file FILE  submit homework
  -v, --view            view homework
```
Setup & Installation
------------

To setup the script to use your account, open up settings.conf and replace the temporary details with your details.

Here's an example config:

```
name = "OCdQOtNJ;Wang, James"
password = "password"
period = "p9"
id = "3497"
teacher = "cbrown"
semester = "fall2015"
```

Currently, I do not know the algorithm for encoding/decoding the student ids, so you're going to have to
find your username yourself. In order to do so, just go onto the homework server, view the source, and find
the value for the entry with your name. It may look like this:

`<option value="vCmQztPJ;Wang, James">Wang, James</option>`

The period is a combination of 'p' and the period you have class.

The teacher's name is the first letter of their first name, combined with their last name.
If you do not know their first name, just go onto the homework server and grab it from the url.

The semester is `fall/spring + year`.

Finally, run `install.sh` from terminal to install.

TODO
----

- Automatic retrieval of username based on real name
- Display contents of file before (prompting?) downloading
- ~~Automatically use proxy if DOE filter blocks the website~~
- Documentation
