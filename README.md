HomeworkServer
==============

Script to quickly send and receive files to/from the CS Homework Server.

```
usage: homeworkserver [-h] [-s FILE] [-v] [-g] [-u] [--stdin] [--view-profile]
[--update-profile]

optional arguments:
    -h, --help              show this help message and exit
    -s FILE, --submit FILE  submit homework
    -v, --view              view homework
    -g, --grades            view grades
    -u, --update-settings   update settings file
    --stdin                 submit file from stdin
    --view-profile          view profile
    --update-profile        update profile on the server
```

Style Guide
-----------

https://www.python.org/dev/peps/pep-0008/
Setup & Installation
------------

To setup the script to use your account, open up `settings.conf` and replace the temporary details with your details.

Here's an example config:

```
name = "Wang, James"
password = "password"
period = "p9"
id = "3497"
teacher = "cbrown"
semester = "fall2015"
osis = "123456789"
```

The name consists of your last name followed by your first name.

The period is a combination of 'p' and the period you have class.

The teacher's name is the first letter of their first name, combined with their last name.
If you do not know their first name, just go onto the homework server and grab it from the url.

The semester is fall/spring + year.

Osis is your 9 digit osis number.

Finally, run `install.sh` from terminal to install.

Alternatively, you could just run `install.sh` and then run the script with the `--update-settings` flag.

TODO
----

- ~~Display contents of file before (prompting?) downloading~~
- ~~Automatically use proxy if DOE filter blocks the website~~
- ~~Documentation~~
- Test for compatibility with more classes
