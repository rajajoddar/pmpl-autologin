import urllib
# import urllib2
import time
import sys
import pprint, getopt, os, re

SCRIP_VERION = "0.2.0"

PY_VERSION_MAJOR = sys.version_info.major
PY_VERSION_MINOR = sys.version_info.minor

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CURRENT_FILE = os.path.basename(__file__)

# This is the configuration file name.
CONFIG_FILE_NAME = 'config.al'

# This is the config file path
CONFIG_PATH = os.path.join(CURRENT_DIR, CONFIG_FILE_NAME)

# All variable that will be used for request.
REFERRER_LOGIN = "10.10.0.1/24online/webpages/client.jsp",
REFERRER_LOGOUT = "http://10.10.0.1/24online/servlet/E24onlineHTTPClient"
SUBMIT_URL = "http://10.10.0.1/24online/servlet/E24onlineHTTPClient"

# All string for final message
FINAL_MESSAGES = {
    'login': 'We have been able to log you in.',
    'logout': 'You are now logged out.',
    'renew': 'Please renew your package.',
    'unknown': 'Well, there might be some problem, try to use browser.',
    'wup': 'Wrong username/password, please reconfigure.'
}


def getStatusFromPage(page):

    # we are gonna check ability for every messages one by one.
    # To do that store all the patterns in a variable.
    # TODO: more status to be updated.

    patterns = {
        'login':    b'<([^\S]|)font[^\S](.*)>Remaining Time:',
        'renew':    b'<([^\S]|)font[^\S](.*)>Please renew your',
        'logout':   b'<([^\S]|)font[^\S](.*)>You have successfully logged off',
        'wup':      b'<([^\S]|)font[^\S](.*)>Wrong username'
    }

    iterItems = patterns.iteritems() if PY_VERSION_MAJOR < 3  else patterns.items()

    for status, regex in iterItems:
        if re.search(regex, page, re.I) is not None:
            return status

    # if not thing matched
    return 'unknown'


# This is the creating configuration file function
def createConfigFile():
    # file = open(filePath, 'w');

    # Store the username and password
    username = Input("Please enter your username: ")
    password = Input("Please enter your password: ")

    # Now create the file.
    file = open(CONFIG_PATH, 'w')
    file.writelines(['username=' + username, '\n', 'password=' + password])
    file.close()


# This method gets the log in vars.
def getLoginVars():
    # get username and password.
    info = getInfoFromConfig()

    # Its now time to create vars.
    return {
        'mode': "191",
        'isAccessDenied': "null",
        'url': "10.10.0.1/24online/webpages/client.jsp",
        'message': "You are now Log In",
        'checkClose': "0",
        'sessionTimeout': "0.0",
        'guestmsgreq': "false",
        'username': info['username'],
        'password': info['password'],
    }


# this method helps to get log out vars.
def getLogoutVars():
    # get username and password.
    info = getInfoFromConfig()

    return {
        'mode':             "193",
        'isAccessDenied':   "false",
        'url':              "10.10.0.1/24online/webpages/client.jsp",
        'message':          "You are now log out.",
        'checkClose':       "1",
        'sessionTimeout':   "-1.0",
        'guestmsgreq':      "false",
        'loggedinuser':     info['username'],
        'username':         info['username']
    }


# This function helps to send request.
def sendRequest(svars, referer):
    en = urlen(svars)
    req = Req(SUBMIT_URL, en)
    req.add_header('referer', str(referer))
    res = urlo(req)
    return res.read()


# get username and password from config file.
def getInfoFromConfig():
    # First get the  configuration file.
    file = open(CONFIG_PATH, 'r')
    configs = file.read()
    file.close()

    # Now check if the `username` or `password` parameter is available in config file.
    # First match the `username`
    matchUsername = re.search(r'username(?:[^\S]|)=(?:[^\S]|)(.+)(:?[^\S]|)', configs, re.I)
    matchPassword = re.search(r'password(?:[^\S]|)=(?:[^\S]|)(.+)(:?[^\S]|)', configs, re.I)

    if matchPassword is None or matchUsername is None:
        raise Exception("Your configurations file is broken, type ./" + CURRENT_FILE + " -c to reconfigure.")

    return {
        'username': matchUsername.group(1).strip(),
        'password': matchPassword.group(1).strip(),
    }


# send log in request.
def loginUser():
    print("Sending request for logging in..")
    time.sleep(3)
    page = sendRequest(getLoginVars(), REFERRER_LOGIN)

    # Now print the final message from page.
    print(FINAL_MESSAGES[getStatusFromPage(page)])


# send log out request.
def logoutUser():
    print("Sending request for logging out..")
    time.sleep(3)

    page = sendRequest(getLogoutVars(), REFERRER_LOGOUT)

    # Now print the final message from page.
    print(FINAL_MESSAGES[getStatusFromPage(page)])


# Python 2 AND 3 Compatibility work started here #


def Input(str):
    if PY_VERSION_MAJOR < 3:
        return raw_input(str)
    else:
        return input(str)


def Req(url, vars):
    if PY_VERSION_MAJOR < 3:
        from urllib2 import Request
    else:
        from urllib.request import Request
    return Request(url, vars)


def urlo(req):
    if PY_VERSION_MAJOR < 3:
        from urllib2 import urlopen
    else:
        from urllib.request import urlopen
    return urlopen(req)


def urlen(vars):
    if PY_VERSION_MAJOR < 3:
        from urllib import urlencode
        return urlencode(vars)
    else:
        from urllib.parse import urlencode
        return urlencode(vars).encode('UTF-8')


# END OF Python 2 AND 3 Compatibility work #

def printHelp():
    print(
        """
           PMPL-AUTO LOGIN version %s
           Please report bugs to our git hub page: https://github.com/boseakash7/pmpl-autologin

           example: %s -l

           -l --log-in      send a log in request.
           -L --log-out     send a log out request.
           -c               configure again for username and password.
           -h --help        show this help.

        """ % (SCRIP_VERION, CURRENT_FILE)
    )


def checkPythonVersion():
    if PY_VERSION_MAJOR < 3 and PY_VERSION_MINOR < 7:
        print("Python version 2.7 or higher is require.")
        sys.exit()


def __main__(argv):

    # First check if the user has installed required pytthon version.
    checkPythonVersion()

    # Now check if the configuration file exists.
    # If not then just simply create one.
    if os.path.isfile(CONFIG_PATH) is not True:
        print("\nWelcome to PMPL-AUTOLOGIN.")
        print("We need to configure your username and password.\n")
        print("Warning: write your username and password with maintained caps.\n")
        createConfigFile()

        # check if the user want to log in right now.
        if Input("Do you want to get login now? (y/n)").lower()[0] == 'y':
            loginUser()
            sys.exit()
        else:
            sys.exit()  # Exit the script as user do not want to get logged in

    # Now its time to work with arguments
    opts, args = getopt.getopt(argv, "chlL", ["log-in", "log-out"])

    if len(argv) > 1:
        print("Please use only one option.")
        sys.exit()
    elif len(argv) < 1:
        printHelp()
        sys.exit()

    for opt, arg in opts:

        if opt == '-c':
            print("Welcome to configuration.")
            createConfigFile()
            sys.exit()

        elif opt == '-h' or opt == '--help':
            printHelp()

        elif opt == '-L' or opt == '--log-out':
            logoutUser()

        elif opt == '-l' or opt == '--log-in':
            loginUser()


if __name__ == "__main__":
    try:
        __main__(sys.argv[1:])
    except (KeyboardInterrupt, EOFError) as e:
        print("\n\nAs you command, exiting in the middle..")
    except getopt.GetoptError:
        printHelp()
    except Exception as ex:
        print("\n\nError: " + str(ex))
