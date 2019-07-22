import json
import logging
import urllib

from http.server import BaseHTTPRequestHandler, HTTPServer

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s -%(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
fh = logging.FileHandler('cyberpool.log')
fh.setFormatter(formatter)
logger.addHandler(fh)


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
        self.send_response(200)
        self.end_headers()

        self.data_bytes = self.rfile.read(int(self.headers['Content-Length']))
        logger.info(f'Got new raw request: {self.data_bytes}')
        data_dict = self.convert_query_string_to_dict(self.data_bytes)
        logger.info(f'data_dict: {data_dict}')
        slack_json = json.loads(str(data_dict))
        logger.info(f'Request transformed to json: {slack_json}')
        data_to_mysql = self.to_json(slack_json)
        # print the parsed json to the screen
        self.wfile.write(json.dumps(data_to_mysql, indent=2).encode('utf-8'))

        return

    def convert_query_string_to_dict(self, data):
        data_str = data.decode('utf-8')
        qs_data = urllib.parse.urlsplit(data_str).path.replace("'", '"')
        return json.loads(qs_data)

    def to_json(self, slack_input):
        text = slack_input["text"]
        text = text.split(',')
        user_id = slack_input["slack_id"]
        if text[0] == 'create':
            res = {"roll": "0", "from": text[1].strip(), "to": text[2].strip(), "date": text[3].strip(),
                   "time": text[4].strip(), "seats": text[5].strip(), "id": user_id}
        else:
            res = {"roll": "1", "from": text[1].strip(), "to": text[2].strip(), "date": text[3].strip(),
                   "time": text[4].strip(), "id": user_id}
        logger.info(f'The json for the database {res}')
        return res


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



