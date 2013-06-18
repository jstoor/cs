#!/usr/bin/python

from twisted.web import server, resource
from twisted.internet import reactor
from json import loads


# Should store values in a database, 
# but for test purposes using in memory dictionary.
# Perhaps look at "sAsync"
Cache = {}

class Root(resource.Resource):

  def getChild(self, name, request):
    return self

  def render_GET(self, request):
    return '<html><body><form method="POST"><input name="the-field" type="text"/></form></body></html>'

  def render_POST(self, request):
    raw_data = request.content.getvalue()
    data = loads(raw_data)
    
    for data_raw_value in data.values():
      data_value = loads(data_raw_value)
      for key, value in data_value.iteritems():
        Cache[key] = value

    return '<html><h1>SAVED</h1></html>'

class Html(resource.Resource):
  isLeaf=True
  def render_GET(self, request):
    result = "<html><body>"
    for k, v in Cache.iteritems():
      result += "%s %s<br/>" % (k,v)
    result += "</body></html>"
  
    return str(result)

class Csv(resource.Resource):
  isLeaf=True
  def render_GET(self, request):
    result = ""
    for k, v in Cache.iteritems():
      result += "%s,%s," % (k,v)

    return str(result)

def main():
  root=Root()
  root.putChild('HTML', Html())
  root.putChild('CSV', Csv())
  reactor.listenTCP(8000, server.Site(root))
  reactor.run()

if __name__ == '__main__':
  main()






