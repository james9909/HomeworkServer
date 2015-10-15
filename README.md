HomeworkServer
==============

Script to quickly send and receive files to/from the CS Homework Server.

```
usage: homeworkserver [-h] [-s FILE] [-v] [--update-settings]

optional arguments:
  -h, --help              show this help message and exit
  -s FILE, --submit FILE  submit homework
  -v, --view              view homework
  --update-settings       update settings file
```

Style Guide
-----------

https://www.python.org/dev/peps/pep-0008/
Setup & Installation
------------

To setup the script to use your account, open up `settings.conf` and replace the temporary details with your details.

Here's an example config:

```
name = "3497;Wang, James"
password = "password"
period = "p9"
id = "3497"
teacher = "cbrown"
semester = "fall2015"
```

The name consists of your 4 digit id, and full name, delimited by a semicolon.

The period is a combination of 'p' and the period you have class.

The teacher's name is the first letter of their first name, combined with their last name.
If you do not know their first name, just go onto the homework server and grab it from the url.

The semester is fall/spring + year.

Finally, run `install.sh` from terminal to install.

Alternatively, you could just run `install.sh` and then run the script with the `--update-settings` flag.

TODO
----

- ~~Display contents of file before (prompting?) downloading~~
- ~~Automatically use proxy if DOE filter blocks the website~~
- ~~Documentation~~
- Test for compatibility with more classes
