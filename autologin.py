import urllib
import urllib2
import time
import sys

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

    submitVars['username'] = "raxxxxx_swbk"     #enter your username
    submitVars['password'] = "12345"            #enter your password

    referer = "10.10.0.1/24online/webpages/client.jsp" # URL of referring web page goes here
    

submitUrl = "http://10.10.0.1/24online/servlet/E24onlineHTTPClient" # URL of form action goes here


submitVarsUrlencoded = urllib.urlencode(submitVars)
req = urllib2.Request(submitUrl, submitVarsUrlencoded)
req.add_header('Referer', referer)
response = urllib2.urlopen(req)
thePage = response.read()

print "You are now online."


#print thePage

#This python script is written and managed by Raja Joddar. This python script is made for PMPL (Meghbela broadband) user to easy login in, mainly for Ubuntu or Any GNU/Linux User.
#This script is now under development, any guys willing to contribute please notify me on "www.facebook.com/rajajoddar".
