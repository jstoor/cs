#!/usr/bin/python

import httplib2
from datetime import datetime
import simplejson


TESTDATA = { 'data' : { "data1": "a1", "data2": "a2" } }

URL = 'http://localhost:8000'

jsondata = simplejson.dumps(TESTDATA)
h = httplib2.Http()
resp, content = h.request(URL,
                          'POST',
                          jsondata,
                          headers={'Content-Type': 'application/json'})
print resp
print content