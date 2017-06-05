from http.server import HTTPServer, BaseHTTPRequestHandler
import os


class MyHandler(BaseHTTPRequestHandler):

    def __init__(self):
        BaseHTTPRequestHandler.__init__(self)
