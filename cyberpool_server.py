import json
import logging
import urllib
import mysql.connector

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import request, parse


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s -%(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
fh = logging.FileHandler('cyberpool.log')
fh.setFormatter(formatter)
logger.addHandler(fh)


class S(BaseHTTPRequestHandler):

    #def __init__(self):
    #    self.db = mysql.connector.connect(
    #    host="localhost",
    #    user="root",
    #    password="cyberpool",
    #    database="cyberpool"
    #    )
    #    self.cursor_db = self.db.cursor()

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        f = open('map.html', mode='r')
        self.wfile.write(str.encode(f.read()))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        self._set_headers()
        self.send_response(200)
        self.end_headers()

        self.data_bytes = self.rfile.read(int(self.headers['Content-Length']))
        logger.info(f'Got new raw request: {self.data_bytes}')
        data_dict = self.convert_query_string_to_dict(self.data_bytes)
        data_to_mysql = self.parse_data_to_sql(data_dict)
        logger.info(f'data_to_mysql: {data_to_mysql}')

        # print the parsed json to the screen
        f = open('map.html', mode='r')
        self.wfile.write(f.read())

        return

    def convert_query_string_to_dict(self, data):
        data_str = data.decode('utf-8')
        qs_data = urllib.parse.urlsplit(data_str).path.replace("'", '"')
        qs_dict = urllib.parse.parse_qs(qs_data)
        logger.info(f'qs_dict: {qs_dict}')
        return json.loads(qs_dict)

    def parse_data_to_sql(self, data):
        text = data.get("text")
        if not text:
            response_url = data["response_url"]
            self.send_message_to_slack(response_url[0], "Offer: ,From: ,To: ,Date: ,Time: ,Num Of Seats: ")
        else:
            request = text[0].split(',')
            if len(request) == 1 and request[0].lower() == "join":
                # TODO: add return full list from db
                    pass
            else:
                if (len(request) < 5) or (request[0].lower() == "create" and len(request) < 6) or \
                        (request[0].lower() == "join" and len(request) < 5):
                    response_url = data["response_url"]
                    self.send_message_to_slack(response_url[0], "There is not enough arguments")
                else:
                    user_id = data["user_id"]
                    user_name = data["user_name"]
                    if request[0].lower() == 'offer':
                        res = {"roll": "0", "from": request[1].strip(), "to": request[2].strip(),
                               "date": request[3].strip(), "time": request[4].strip(), "seats": request[5].strip(),
                               "id": user_id, "name": user_name}
                    else:
                        res = {"roll": "1", "from": request[1].strip(), "to": request[2].strip(),
                               "date": request[3].strip(), "time": request[4].strip(), "id": user_id, "name": user_name}
                    logger.info(f'The json for the database {res}')
                    return res

    def send_message_to_slack(self, response_url, msg):
        post = {"text": "{0}".format(msg)}
        try:
            json_data = json.dumps(post)
            req = request.Request(response_url,
                                  data=json_data.encode('ascii'),
                                  headers={'Content-Type': 'application/json'})
            request.urlopen(req)
        except Exception as em:
            print("EXCEPTION: " + str(em))


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



