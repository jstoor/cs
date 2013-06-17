#!/usr/bin/python

from twisted.web import server, resource
from twisted.internet import reactor

class Test(resource.Resource):
  def getChild(self, name, request):
      print "--->getChild", name, request
      return self

  def render_GET(self, request):
      print "--->render_GET"
      return '<html><body><form method="POST"><input name="the-field" type="text"/></form></body></html>'

  def render_POST(self, request):
      print "--->Fred"
      newdata = request.content.getvalue()
      print newdata
      return '<html><h1>Test.POST</h1></html>'

class TestHTML(resource.Resource):
  isLeaf=True
  def render_GET(self, request):
      return "<html><body>TestHTML.render_GET</body></html>"

class TestCSV(resource.Resource):
  isLeaf=True
  def render_GET(self, request):
      return "<html><body>TestCSV.render_GET</body></html>"

blog_obj=Test()
blog_obj.putChild('HTML', TestHTML())
blog_obj.putChild('CSV', TestCSV())
reactor.listenTCP(8000, server.Site(blog_obj))
reactor.run()
