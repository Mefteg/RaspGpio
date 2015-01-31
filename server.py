import BaseHTTPServer
import subprocess
import cgi
import json
import threading
import time
import ctypes
import sys

class RaspGpioHTTPServer(BaseHTTPServer.HTTPServer):
    def __init__(self, server_address, RequestHandlerClass):
        print "> constructor: RaspGpioHTTPServer"
        self.thread = RaspGpioExecuteScript()
        self.thread.deamon = True
        BaseHTTPServer.HTTPServer.__init__(self, server_address, RequestHandlerClass)

class RaspGpioHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        print "> constructor: RaspGpioHTTPRequestHandler"
        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def do_POST(self):
        response_code = 201
        try:
            content_type = self.headers.getheader('content-type')

            # get the request's parameters (the new script is stored in)
            params = {}
            if content_type == 'application/x-www-form-urlencoded':
                content_len = int(self.headers.getheader('content-length', 0))
                params = cgi.parse_qs(self.rfile.read(content_len), keep_blank_values=1)
            elif content_type == 'multipart/form-data':
                params = cgi.parse_multipart(self.rfile)

            # if a thread is running, kill it
            if (self.server.thread.is_alive()):
                tid = self.server.thread.ident
                print "\t> Try to kill thread ", tid
                res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(SystemExit))

            # write the new script
            if params['file_content']:
                file_script = open("script.py", 'w')
                file_script.write(params['file_content'][0])
                file_script.close()

            # start the thread to launch the new script
            self.server.thread.start()

        except:
            response_code = 500
            print "\t> Unexpected error:", sys.exc_info()[0]

        # send a response with the response code
        self.send_response(response_code)

class RaspGpioExecuteScript(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        subprocess.call(["python", "script.py"])


PORT = 3000

Handler = RaspGpioHTTPRequestHandler

httpd = RaspGpioHTTPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()