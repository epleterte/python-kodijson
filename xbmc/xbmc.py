#!/bin/env/python

import urllib, urllib2
import json
from StringIO import StringIO

PLAYER_VIDEO=1

class XBMCTransport(object):
  """Base class for XBMC transport"""
  def execute(self, method, args):
    pass

class XBMCJsonTransport(XBMCTransport):
  """HTTP Json transport"""
  def __init__(self, url, username='xbmc', password='xbmc'):
    self.url=url
    self.username=username
    self.password=password
    self.id = 0

  def execute(self, method, *args, **kwargs):
    header = {
        'Content-Type' : 'application/json',
        'User-Agent' : 'python-xbmc'
        }
    if len(args) == 1:
      args=args[0]
    params = kwargs
    params['jsonrpc']='2.0'
    params['id']=self.id
    self.id +=1
    params['method']=method
    params['params']=args

    values=json.dumps(params)
    auth_handler = urllib2.HTTPBasicAuthHandler()
    auth_handler.add_password(realm=None, uri=self.url, user=self.username, passwd=self.password)
    opener = urllib2.build_opener(auth_handler)
    # ...and install it globally so it can be used with urlopen.
    urllib2.install_opener(opener)
    data = values
    req = urllib2.Request(self.url, data, header)
    print data
    response = urllib2.urlopen(req)
    the_page = response.read()
    print "'%s'"%(the_page)
    if len(the_page) > 0 :
      return json.load(StringIO(the_page))
    else:
      return None # for readability

class XBMC(object):
  """XBMC client"""
  def __init__(self, url, username='xbmc', password='xbmc'):
    self.transport = XBMCJsonTransport(url, username, password)
    self.JSONRPC = JSONRPC(self.transport)
    self.VideoLibrary = VideoLibrary(self.transport)
    self.Application = Application(self.transport)
    self.Gui = Gui(self.transport)
    self.Player = Player(self.transport)
    def execute(self, *args, **kwargs):
      self.transport.execute(*args, **kwargs)

class XbmcNamespace(object):
  """Base class for XBMC namespace."""
  def __init__(self, xbmc):
    self.xbmc = xbmc
  def __getattr__(self, name):
    klass= self.__class__.__name__
    method=name
    xbmcmethod = "%s.%s"%(klass, method)
    def hook(*args, **kwargs):
      return self.xbmc.execute(xbmcmethod, *args, **kwargs)
    return hook

class JSONRPC(XbmcNamespace):
  """XBMC JSONRPC namespace. See http://wiki.xbmc.org/index.php?title=JSON-RPC_API/v6#JSONRPC"""
  pass
class VideoLibrary(XbmcNamespace):
  """XBMC VideoLibrary namespace. See http://wiki.xbmc.org/index.php?title=JSON-RPC_API/v6#VideoLibrary_2"""
  pass
class Application(XbmcNamespace):
  """Application namespace. See http://wiki.xbmc.org/index.php?title=JSON-RPC_API/v6#Application"""
  pass
class Gui(XbmcNamespace):
  """XBMC Gui namespace. See http://wiki.xbmc.org/index.php?title=JSON-RPC_API/v6#GUI_2"""
  pass
class Player(XbmcNamespace):
  """XBMC Player namespace. http://wiki.xbmc.org/index.php?title=JSON-RPC_API/v6#Player"""
  pass

