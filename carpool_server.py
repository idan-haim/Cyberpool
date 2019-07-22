# import http.server
# import socketserver
#
# PORT = 8001
#
# Handler = http.server.SimpleHTTPRequestHandler
#
# with socketserver.TCPServer(("", PORT), Handler) as httpd:
#     print("serving at port", PORT)
#     httpd.serve_forever()

from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 8001


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')


httpd = HTTPServer(('localhost', PORT), SimpleHTTPRequestHandler)
print("serving at port", PORT)
httpd.serve_forever()