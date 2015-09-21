import requests
from urllib import unquote_plus
from bs4 import BeautifulSoup

def get_page(url, period, name, password, page):
    '''
    Returns html of the requested page
    '''
    name = unquote_plus(name)
    data = {"classes": period, "students": name, "password": password, "Submit": "Submit", "page": page}
    request = requests.post(url, data=data)
    return request.text

def download_file(url, name=None):
    if name:
        file_name = name
    else:
        file_name = url.split('/')[-1] # Retrieve file name from url
    with open(file_name, 'wb') as output:
        response = requests.get(url, stream=True)

        if not response.ok:
            print "Could not fetch file"
            return

        for block in response.iter_content(1024):
            output.write(block)

def parse_homeworks(html):
    '''
    Returns a list of homeworks that have been submitted and their links
    '''
    soup = BeautifulSoup(html, "lxml")
    links = []
    print soup
    for a in soup.find_all("a", attrs={"class": "", "href": True}): # Homework links do not have classes
        link = a["href"]
        links.append(link)

    labels = []
    for label in soup.find_all("label", attrs={"class": ""}):
        label = label.text
        label = label.encode('ascii', 'ignore') # Remove unicode
        labels.append(label[2:]) # Only the number

    homeworks = {}
    for x in range(len(labels)):
        try:
            homeworks[labels[x]] = links[x]
        except:
            break
    return homeworks

def parse_assignments(html):
    '''
    Returns a list of homeworks that may be submitted
    '''
    soup = BeautifulSoup(html, "lxml")
    assignments = []
    for option in soup.find_all("option"):
        title = str(option.text) # Remove unicode
        assignments.append(title)
    return assignments

def submit_homework(homework):
    page = get_page("http://bert.stuy.edu/cbrown/fall2015/pages.py", "p9", "rCqQhtiJ%3BWang%2C+James", "password", "submit_homework2")
    assignments = parse_assignments(page)
    titles = []
    for assignment in assignments:
        titles.append(assignment[:assignment.find(" (")])

    i = 0
    if len(assignments) < 0:
        print "Could not fetch assignments"
        return

    while i < len(assignments):
        print "[%s]: %s" % (titles[i], assignments[i])
        i += 1

    while True:
        option = str(raw_input("Please select a homework to submit: "))
        if (option not in titles):
            print "Invalid choice"
            continue
        else:
            break

    comment = ""
    while True:
        answer = str(raw_input("Would you like to write a comment to the teacher? [y/n] "))
        if answer.lower == "y":
            comment = str(raw_input("Please enter your comment: "))
        break

    contents = open(homework, "r").read()
    data = {"page": "store_homework", "id4": "3497", "classid": "p9", "assignmentid": str(option), "teacher_comment": comment, "submit": "Submit this assignment"}
    request = requests.post("http://bert.stuy.edu/cbrown/fall2015/pages.py", data=data, files={"filecontents": (homework, open(homework, "rb"))})
    if request.status_code == 200:
        print "Homework successfully submitted"
    else:
        print "Failed to submit file"

def view_homework():
    page = get_page("http://bert.stuy.edu/cbrown/fall2015/pages.py", "p9", "rCqQhtiJ%3BWang%2C+James", "password", "homework_view2")
    homeworks = parse_homeworks(page)
    if len(homeworks) == 0:
        print "Could not fetch homeworks"
        return

    for homework in homeworks.keys():
        print "[%s]: %s" % (homework, homeworks[homework])

    while True:
        option = raw_input("Which homework would you like to view? ")
        if (option not in homeworks.keys()): # Robustness
            if ("0" + option in homeworks.keys()):
                option = "0" + option
                break
            else:
                print "Invalid choice"
                continue
        else:
            break

    print "Selected %s" % (homeworks[option])
    url = "http://bert.stuy.edu/cbrown/fall2015/" + homeworks[option]
    download_file(url)

submit_homework("main.py")
# view_homework()
