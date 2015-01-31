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
        self.lock = threading.Lock()
        BaseHTTPServer.HTTPServer.__init__(self, server_address, RequestHandlerClass)

class RaspGpioHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        print "> constructor: RaspGpioHTTPRequestHandler"
        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def do_POST(self):
        # acquire the lock
        self.server.lock.acquire()

        response_code = 201
        try:
            # get the content type
            content_type = self.headers.getheader('content-type')

            # get the request's parameters (the new script is stored in)
            params = {}
            if content_type == 'application/x-www-form-urlencoded':
                content_len = int(self.headers.getheader('content-length', 0))
                params = cgi.parse_qs(self.rfile.read(content_len), keep_blank_values=1)
            elif content_type == 'multipart/form-data':
                params = cgi.parse_multipart(self.rfile)

            # write the new script
            if params['file_content']:
                file_script = open("script.py", 'w')
                file_script.write(params['file_content'][0])
                file_script.close()

            # if a thread is running, kill it
            if (self.server.thread.is_alive()):
                self.server.thread.stop()
                # wait for thread end
                cpt = 0
                while self.server.thread.is_alive() and cpt < 5:
                    time.sleep(1)
                    cpt += 1
                # create a new thread
                self.server.thread = RaspGpioExecuteScript()

            # start the thread to launch the new script
            self.server.thread.start()

        except:
            response_code = 500
            print "\t> Unexpected error:", sys.exc_info()[0]

        # send a response with the response code
        self.send_response(response_code)

        # release the lock
        self.server.lock.release()

class RaspGpioExecuteScript(threading.Thread):
    def __init__(self):
        self.popen = None
        self.go_on = True
        threading.Thread.__init__(self)

    def run(self):
        self.popen = subprocess.Popen(["python", "script.py"])
        while self.go_on:
            time.sleep(1)
        self.popen.terminate()

    def stop(self):
        self.go_on = False


PORT = 3000

Handler = RaspGpioHTTPRequestHandler

httpd = RaspGpioHTTPServer(("", PORT), Handler)

try:
    print "serving at port", PORT
    httpd.serve_forever()
except:
    print "> server has to stop"
    print "> kill the thread..."
    httpd.thread.stop()
    cpt = 0
    while httpd.thread.is_alive() and cpt < 5:
        time.sleep(1)
        cpt += 1
    if httpd.thread.is_alive():
        print "> thread killed"
    else:
        print "> not able to kill the thread, be careful it might be still running!"

print "> server stopped"
