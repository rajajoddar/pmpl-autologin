import urllib
# import urllib2
import time
import sys
import pprint, getopt, os

PY_VERSION_MAJOR = sys.version_info.major
PY_VERSION_MINOR = sys.version_info.minor

# def __main__(argv):
#     opts, args = getopt.getopt(argv,"chi:o:",["ifile=","ofile="])
#     pprint.pprint(os.path.dirname(os.path.abspath(__file__)))
#     sys.exit()

#     for opt, arg in opts:
#         if opt == '-c':
#             print ("Welcome to configure.")
#             sys.exit()
#         elif opt == '-h':
#             print ("awesome")
#             sys.exit()

# if __name__ == "__main__":
#    __main__(sys.argv[1:])

try:
    login=sys.argv[1] # 0 -> logout 1-> login
except IndexError:
    login = 1

submitVars={}

if(login==0):   # LOGOUT

    submitVars['mode'] = "191"
    submitVars['isAccessDenied'] = "false"
    submitVars['url'] = "10.10.0.1/24online/webpages/client.jsp"
    submitVars['message'] = "You are Now LOG OUT"
    submitVars['checkClose'] = "0"
    submitVars['sessionTimeout'] = "-1.0"
    submitVars['guestmsgreq'] = "false"

    referer = "http://10.10.0.1/24online/servlet/E24onlineHTTPClient" # URL of referring web page goes here

else:           # LOGIN
    time.sleep(3)
    
    submitVars['mode'] = "191"
    submitVars['isAccessDenied'] = "null"
    submitVars['url'] = "10.10.0.1/24online/webpages/client.jsp"
    submitVars['message'] = "You are Now LOG IN"
    submitVars['checkClose'] = "0"
    submitVars['sessionTimeout'] = "0.0"
    submitVars['guestmsgreq'] = "false"

    submitVars['username'] = "Sohini_scc"     #enter your username
    submitVars['password'] = "12345"            #enter your password

    referer = "10.10.0.1/24online/webpages/client.jsp" # URL of referring web page goes here
    

submitUrl = "http://10.10.0.1/24online/servlet/E24onlineHTTPClient" # URL of form action goes here





# def printhelp():
#     print ("help")



def Req( url, vars ):
    if PY_VERSION_MAJOR < 3:
        from urllib2 import Request
    else:
        from urllib.request import Request
    return Request( url, vars )

def urlo( req ):
    if PY_VERSION_MAJOR < 3:
        from urllib2 import urlopen
    else:
        from urllib.request import urlopen
    return urlopen(req)

def urlen( vars ):
    if PY_VERSION_MAJOR < 3:
        from urllib import urlencode
        return urlencode(vars)
    else:
        from urllib.parse import urlencode
        return urlencode(vars).encode('UTF-8')

submitVarsUrlencoded = urlen(submitVars)
req = Req(submitUrl, submitVarsUrlencoded)
req.add_header('Referer', referer)
response = urlo(req)
thePage = response.read()

print ("You are now online.")

# print thePage

#This python script is written and managed by Raja Joddar. This python script is made for PMPL (Meghbela broadband) user to easy login, mainly for Ubuntu or Any GNU/Linux User.
#This script is now under development, any guys willing to contribute please notify me on "www.facebook.com/rajajoddar".
