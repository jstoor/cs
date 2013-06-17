#!/usr/bin/python

from twisted.web import server, resource
from twisted.internet import reactor
from json import loads

# Should store values in a database, 
# but for test purposes using in memory dictionary.
cache = {}

class Test(resource.Resource):
  def getChild(self, name, request):
      print "--->getChild", name, request
      return self

  def render_GET(self, request):
      print "--->render_GET"
      return '<html><body><form method="POST"><input name="the-field" type="text"/></form></body></html>'

  def render_POST(self, request):
      raw_data = request.content.getvalue()
      data = loads(raw_data)
      
      for data_raw_value in data.values():
        data_value = loads(data_raw_value)
        for key, value in data_value.iteritems():
          cache[key] = value

      return '<html><h1>SAVED</h1></html>'

class TestHTML(resource.Resource):
  isLeaf=True
  def render_GET(self, request):
      result = "<html><body>"
      for k, v in cache.iteritems():
        result += "%s %s<br/>" % (k,v)
      result += "</body></html>"
    
      return str(result)

class TestCSV(resource.Resource):
  isLeaf=True
  def render_GET(self, request):
      result = ""
      for k, v in cache.iteritems():
        result += "%s,%s," % (k,v)

      return str(result)

blog_obj=Test()
blog_obj.putChild('HTML', TestHTML())
blog_obj.putChild('CSV', TestCSV())
reactor.listenTCP(8000, server.Site(blog_obj))
reactor.run()
