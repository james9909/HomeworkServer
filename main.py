import argparse
import collections
import os
import re
import signal
import sys

import requests

from bs4 import BeautifulSoup
from urllib import unquote_plus
from datetime import datetime

NAME = ""
PASSWORD = ""
PERIOD = ""
STUDENT_ID = ""

BASE_URL = "http://bert.stuy.edu"
SUBMIT = "submit_homework2"
SUBMIT_ASSIGNMENT = "Submit this assignment"
VIEW = "homework_view2"
STORE_HOMEWORK = "store_homework"
URL = ""
PROXIES = {"http": "http://filtr.nycboe.org:8002",
           "https": "http://filtr.nycboe.org:8002"
           }

use_proxy = False

def signal_handler(signal, frame):
    print("\nExiting...")
    sys.exit(0)

def init_settings():
    """ Initializes variables based on settings configuration """
    global NAME, PASSWORD, PERIOD, STUDENT_ID, TEACHER, SEMESTER, URL
    path = os.path.join(os.path.dirname(__file__), "settings.conf")
    settings = open(path, "r").readlines()

    # Regex to grab everything within the quotations
    NAME = unquote_plus(re.findall('"([^"]*)"', settings[0])[0])
    PASSWORD = re.findall('"([^"]*)"', settings[1])[0]
    PERIOD = re.findall('"([^"]*)"', settings[2])[0]
    STUDENT_ID = re.findall('"([^"]*)"', settings[3])[0]
    TEACHER = re.findall('"([^"]*)"', settings[4])[0]
    SEMESTER = re.findall('"([^"]*)"', settings[5])[0]
    URL = "%s/%s/%s/pages.py" % (BASE_URL, TEACHER, SEMESTER)

def correct_date(date):
    """ Correct date to comply with datetime format strings """
    date = date.split("/")
    if len(date[0]) != 2:  # Fix month by appending 0
        date[0] = "0" + date[0]
    if len(date[1]) != 2:  # Fix day by appending 0
        date[1] = "0" + date[1]
    if len(date[2]) != 10:  # Fix year by appending 20
        date[2] = "20" + date[2]

    # Fix hour by adding 12 if it is PM
    temp = date[2].split(" ")
    hour = temp[1]
    if "p" in hour:
        hour = hour[:-1]
        hour = hour.split(":")
        hour = str(int(hour[0]) + 12) + ":" + hour[1]
    elif "a" in hour:
        hour = hour[:-1]
    temp[1] = hour
    date[2] = " ".join(temp)

    return "/".join(date)

def is_late(due_date):
    """ Determine if deadline for homework has passed """
    due_date = correct_date(due_date)
    try:
        due_date = datetime.strptime(due_date, "%m/%d/%Y %H")
    except:
        due_date = datetime.strptime(due_date, "%m/%d/%Y %H:%M")
    now = datetime.now()
    if due_date < now:
        return "- Late"
    return ""

def get_page(page, proxy=False):
    """ Returns html of the requested page """
    global use_proxy
    data = {"classes": PERIOD, "students": NAME, "password": PASSWORD, "Submit": "Submit", "page": page}
    if proxy:
        request = requests.post(URL, data=data, proxies=PROXIES)
        use_proxy = True
    else:
        request = requests.post(URL, data=data)
    return request.text

def download_file(url, name=None):
    """ Download file from url """
    if name:
        file_name = name
    else:
        file_name = url.split("/")[-1]  # Retrieve file name from url
    with open(file_name, "wb") as output:
        if use_proxy:
            response = requests.get(url, stream=True, proxies=PROXIES)
        else:
            response = requests.get(url, stream=True)

        if not response.ok:
            print "Could not fetch file"
            return

        for block in response.iter_content(1024):
            output.write(block)
    if not url:
        print "File downloaded as %s" % (file_name)

def parse_homeworks(html):
    """ Returns a list of homeworks that have been submitted and their links """
    soup = BeautifulSoup(html, "lxml")
    links = []
    for a in soup.find_all("a", attrs={"class": "", "href": True}):  # Homework links do not have classes, but they have hrefs
        link = a["href"]
        links.append(link)

    labels = []
    for label in soup.find_all("label", attrs={"class": ""}):
        label = label.text
        label = label.encode("ascii", "ignore")  # Remove unicode
        labels.append(label)

    while len(labels) > len(links):
        labels = labels[1:]

    homeworks = {}
    for x in range(len(labels)):
        try:
            homeworks[labels[x]] = links[x]
        except:
            break

    homeworks = collections.OrderedDict(sorted(homeworks.items()))  # Sort homeworks in order
    return homeworks

def parse_assignments(html):
    """ Returns a list of homeworks that may be submitted and their due date"""
    soup = BeautifulSoup(html, "lxml")
    temp_assignments = []

    # Find all assignment options and get its title
    for option in soup.find_all("option"):
        title = str(option.text)  # Remove unicode
        temp_assignments.append(title)

    # Add the due_date to the title
    titles = []
    for assignment in temp_assignments:
        titles.append(assignment[:assignment.find(" (")])

    if len(temp_assignments) < 0:
        print "Could not fetch assignments"
        return

    i = 0
    assignments = {}
    # Link titles with due date + status
    while i < len(temp_assignments):
        status = ""
        assignment = temp_assignments[i]
        due_date = assignment[assignment.find(" (")+7:].strip(")")
        status = is_late(due_date)
        assignments[titles[i]] = "%s %s" % (due_date, status)
        i += 1

    assignments = collections.OrderedDict(sorted(assignments.items()))  # Sort assignments in order
    return assignments

def submit_homework(homework):
    """ Submit homework to the server """
    page = get_page(SUBMIT)

    if "not found" in page:
        print "Page not found"
        return
    elif "Incorrect password" in page:
        print "Invalid credentials"
        return
    elif "Cannot find class" in page:
        print "Invalid period"
        return
    elif "Access to this site is blocked" in page:  # School proxy :(
        page = get_page(SUBMIT, True)

    assignments = parse_assignments(page)

    for assignment in assignments:
        print "[%s] %s" % (assignment, assignments[assignment])
    while True:
        option = str(raw_input("Please select a homework to submit: "))
        if (option not in assignments.keys()):
            print "Invalid choice"
            continue
        else:
            break

    comment = ""
    while True:
        answer = str(raw_input("Would you like to write a comment to the teacher? [y/n] "))
        if answer.lower() == "y":
            comment = str(raw_input("Please enter your comment: "))
        break

    contents = open(homework, "r").read()
    data = {"page": STORE_HOMEWORK, "id4": STUDENT_ID, "classid": PERIOD,
            "assignmentid": str(option), "teacher_comment": comment, "submit": SUBMIT_ASSIGNMENT}
    if use_proxy:
        request = requests.post(URL, data=data, proxies=PROXIES, files={"filecontents": (homework, open(homework, "r"))})
    else:
        request = requests.post(URL, data=data, files={"filecontents": (homework, open(homework, "r"))})

    if request.status_code == 200:
        print "Homework successfully submitted"
    else:
        print "Failed to submit file"

def view_homework():
    """
    View homeworks from the server

    Will show the contents of the file before prompting a download
    """
    page = get_page(VIEW)

    if "not found" in page:
        print "Page not found"
        return
    elif "Incorrect password" in page:
        print "Invalid credentials"
        return
    elif "Cannot find class" in page:
        print "Invalid period"
        return
    elif "Access to this site is blocked" in page:  # School proxy :(
        page = get_page(VIEW, True)

    homeworks = parse_homeworks(page)
    if len(homeworks) == 0:
        print "Could not fetch homeworks"
        return

    for homework in homeworks.keys():
        print "[%s]: %s" % (homework, homeworks[homework])

    while True:
        option = raw_input("Which homework would you like to view? ")
        if (option not in homeworks.keys()):
            if ("0" + option in homeworks.keys()):  # So the input 6 would be equal to 06, validating the input
                option = "0" + option
                break
            else:
                print "Invalid choice"
                continue
        else:
            break

    url = URL.strip("pages.py") + homeworks[option]
    download_file(url, "/tmp/homeworkserver")
    os.system("cat /tmp/homeworkserver")
    option = str(raw_input("Would you like to download this file? [y/n] "))
    if option.lower() == "y":
        download_file(url)
    os.system("rm /tmp/homeworkserver")
    return

def main():
    init_settings()
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "-s",
            "--file",
            nargs=1,
            help="submit homework"
            )
    parser.add_argument(
            "-v",
            "--view",
            help="view homework",
            action="store_true"
            )
    args = parser.parse_args()
    if args.view:
        view_homework()
    elif args.file:
        submit_homework(args.file[0])
    else:
        parser.parse_args(["-h"])

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    main()
