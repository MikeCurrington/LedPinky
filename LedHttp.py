from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

PORT_NUMBER = 8080

class LedHttp:
  def __init__(self, controlHandler):
    try:
      #Create a web server and define the handler to manage the
      #incoming request
      HandlerClass = self.MakeHandlerClass(controlHandler)
      server = HTTPServer(('', PORT_NUMBER), HandlerClass)
      print 'Started httpserver on port ' , PORT_NUMBER

      #Wait forever for incoming htto requests
      server.serve_forever()

    except KeyboardInterrupt:
      print '^C received, shutting down the web server'
      server.socket.close() 

  def MakeHandlerClass(self, controlHandler):
    class CustomHandler(BaseHTTPRequestHandler, object):
      def __init__(self, *args, **kwargs):
        self.controlHandler = controlHandler
        super(CustomHandler, self).__init__(*args, **kwargs)

      #Handler for the GET requests
      def do_GET(self):
        response = 'unknown command'
        if self.path.startswith("/playing/"):
          self.controlHandler.SetGame( self.path[9:] )
          response = 'ok'
        elif self.path.startswith("/sleep"):
          self.controlHandler.SetSleep(True)
          response = 'ok'
        elif self.path.startswith("/wake"):
          self.controlHandler.SetSleep(False)
          response = 'ok'
        elif self.path.startswith("/brightness"):
          brightness = 100
          if self.path.startswith("/brightness="):
            brightness = int( self.path[12:] )
          self.controlHandler.SetMarqueeBrightness(brightness)
          response = 'ok'
        elif self.path.startswith("/fan"):
          fanspeed = 100
          if self.path.startswith("/fan="):
            fanspeed = int( self.path[5:] )
          self.controlHandler.SetFanSpeed(fanspeed)
          response = 'ok'
        elif self.path.startswith("/demo"):
          self.controlHandler.SetDemo()
          response = 'ok'
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        # Send the html message
        self.wfile.write(response)
        return

    return CustomHandler

  def StartServer():
    try:
      #Create a web server and define the handler to manage the
      #incoming request
      HandlerClass = MakeHandlerClassFromArgv("")
      server = HTTPServer(('', PORT_NUMBER), HandlerClass)
      print 'Started httpserver on port ' , PORT_NUMBER

      #Wait forever for incoming htto requests
      server.serve_forever()

    except KeyboardInterrupt:
      print '^C received, shutting down the web server'
      server.socket.close()

