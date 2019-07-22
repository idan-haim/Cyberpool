import json

from http.server import BaseHTTPRequestHandler, HTTPServer


class S(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write(b"Hi<br/> Sharing is Caring")

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        self._set_headers()
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))

        self.send_response(200)
        self.end_headers()

        slack_data = json.loads(self.data_string)
        # For troubleshooting, uncomment the 3 following lines
        with open("test.json", "w") as outfile:
            json.dump(slack_data, outfile)
        print("{}".format(slack_data))
        self.wfile.write(b'POST!!!!!!!!!!!!!!!')

        return


def run(server_class=HTTPServer, handler_class=S, port=8001):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}')
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
