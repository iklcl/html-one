import urllib
import json
import urllib2
data1={
'userName': 'cld_test',
'password': '1',
'terminalid': 13826539847
}
data = urllib.urlencode(data1)
req  = urllib2.Request('http://116.77.32.199:8080/UserService.asmx/GetRealtimeData', data, {'Content-Type':'application/x-www-form-urlencoded'})
try:
	f = urllib2.urlopen(req)
except Exception as e:
	

response = f.read()
f.close()
print response