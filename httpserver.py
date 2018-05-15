'''
Revised from the code segments:
http://stackoverflow.com/questions/23264569/python-3-x-basehttpserver-or-http-server
and
https://wiki.python.org/moin/BaseHttpServer#Official_Documentation

Xiannong Meng
2015-09-12
Revised
2018-03-29
for CSCI 305
'''

from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib
import time
import os
import sqlite3

HOST_NAME = "localhost"
#HOST_NAME = "dana213-lnx-5"
#HOST_NAME = "polaris"
#HOST_NAME = "brki164-lnx-20"  # any real host name where the server is running
HOST_PORT = 9000               # 1024 < port < 65536
server_name = "Python Server"

default_page = "<html><head><title>Invalid file.</title></head>" + \
            "<body><p>You requested an invalid file.</p>" + \
            "</body></html>"

class MyServer(BaseHTTPRequestHandler):
    
    def do_HEAD(self):
        """
        Return an HTML header if the client requests head only
        """
        print("in do_HEAD");
        okay = self.check_file(self.path)
        if okay == True:
            self.send_response(200)  # good file
        else:
            self.send_response(404)  # bad file, we lump all codes for now
        cont_type = self.check_type(self.path)
        self.send_header("Server", server_name)
        self.send_header("Content-Type", cont_type)
        self.end_headers()
    
    def do_GET(self):
        """
        Return the page requested by the client.
        """
        print("in do_GET");
        if (self.path == "/search"): # send form, set up the search box
            length = self.find_file_length("/form.html")
            self.send_my_head(200, length, "text/html")
            self.send_file("/form.html")
            return

        if (self.path == "/players"):
            ret_data = self.build_players()
            self.send_my_head(200, len(ret_data), "text/html")
            self.wfile.write(bytes(ret_data,"utf-8"))
            return

        if (self.path == "/tournaments"):
            ret_data = self.build_tournaments()
            self.send_my_head(200, len(ret_data), "text/html")
            self.wfile.write(bytes(ret_data,"utf-8"))
            return

        if (self.path == "/characters"):
            ret_data = self.build_characters()
            self.send_my_head(200, len(ret_data), "text/html")
            self.wfile.write(bytes(ret_data,"utf-8"))
            return

        if (self.path == "/winner"):
            ret_data = self.build_winner()
            self.send_my_head(200, len(ret_data), "text/html")
            self.wfile.write(bytes(ret_data,"utf-8"))
            return

        okay = self.check_file(self.path)
        if okay == True:
            cont_type = self.check_type(self.path)
            length = self.find_file_length(self.path)
            self.send_my_head(200, length, cont_type)
            self.send_file(self.path) # actually sending the file
        else:
            self.send_my_head(404, len(default_page), "text/html")
            self.wfile.write(bytes(default_page, "utf-8"))

    def do_POST(self):
        """
        Process the form posted by the client
        """
        if (self.path == "/player_search"):
            length = int(self.headers['Content-Length'])
            post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))
            ret_data = self.player_query(post_data)
            self.send_my_head(200, len(ret_data), "text/html")
            self.wfile.write(bytes(ret_data,"utf-8"))
            return

        if (self.path == "/pool_search"):
            length = int(self.headers['Content-Length'])
            post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))
            ret_data = self.pool_query(post_data)
            self.send_my_head(200, len(ret_data), "text/html")
            self.wfile.write(bytes(ret_data,"utf-8"))
            return
            
        length = int(self.headers['Content-Length'])
        post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))
        # You now have a dictionary of the post data
        print("post data: ", post_data)
        
        # now you have a dictionary of post data
        ret_data = self.build_data(post_data)
        
        # print the returning data
        print("returning data: ", ret_data)
        print("returning data length: ", len(ret_data))

        self.send_my_head(200, len(ret_data), "text/html")
        self.wfile.write(bytes(ret_data,"utf-8"))
        self.wfile.write(bytes("Lorem Ipsum","utf-8"))

    def send_my_head(self, response_code, length, data_type):
        """
        Send HTTP header
        """
        self.send_response(response_code)
        self.send_header("Server", server_name)
        self.send_header("Content-Length", length)
        self.send_header("Content-Type", data_type)
        self.end_headers()

    def build_data(self, post_data):
        """
        The post_data is in the form of 
        {'key1': ['val1'], 'key2': ['val2'], 'key3': ['val3']}
        e.g., 
        {'SecondInput': ['zx  z'], 'FirstInput': ['124'], 'Submit': ['Submit']}
        """
        ret_str = ""
        for k in post_data:
            ret_str = ret_str + "key : " + str(k) + \
                      "\ndata : " + str(post_data[k]) + "\n"
        ret_str = ret_str + "\n"

        return ret_str

    def player_query(self, post_data):
        """
        Handle a query for a player name
        """
        ret_str = '<table style="width:100%"> <tr>'
        conn = sqlite3.connect("Melee.db")
        name = post_data["Name"][0]
        name = name.replace('*', '%') # Replace * with %, to stick to sqlite wildcard format
        cursor = conn.execute("SELECT Tag, Nationality, Character_1, Rank_2017 FROM players WHERE Tag LIKE ?", (name,))
        ret_str += '<th>Tag</th><th>Nationality</th><th>Character_1</th><th>Rank_2017</th></tr>'
        for row in cursor:
            ret_str += '<tr><td>' + row[0] + '</td><td>' + row[1] + '</td><td>' + row[2] + '</td><td>' + str(row[3]) + '</td></tr>'

        ret_str += '</table>'
        conn.close()        
        return ret_str

    def pool_query(self, post_data):
        """
        Handle a query for a player name
        """
        ret_str = '<table style="width:100%"> <tr>'
        conn = sqlite3.connect("Melee.db")
        amount = post_data["Amount"][0]
        amount = amount.replace('$', '') # If user includes a dollar sign, remove it for them
        try:
            amount = int(amount)
        except:
            ret_str = "Please enter an integer value"
            return ret_str
        cursor = conn.execute("SELECT Name, Entrants, Prize_Pool, Winner FROM tournaments WHERE Prize_Pool > ?", (amount,))
        ret_str += '<th>Name</th><th>Entrants</th><th>Prize_Pool</th><th>Winner</th></tr>'
        for row in cursor:
            ret_str += '<tr><td>' + row[0] + '</td><td>' + str(row[1]) + '</td><td>' + str(row[2]) + '</td><td>' + str(row[3]) + '</td></tr>'

        ret_str += '</table>'
        conn.close()        
        return ret_str

    def build_players(self):
        """
        Build the full list of all players
        """
        ret_str = '<table style="width:100%"> <tr>'
        conn = sqlite3.connect("Melee.db")
        cursor = conn.execute("SELECT * FROM players")
        ret_str += '<th>Tag</th><th>Nationality</th><th>Character1</th><th>Character2</th><th>Character3</th><th>Rank_2013</th><th>Rank_2014</th><th>Rank_2015</th><th>Rank_2016</th><th>Rank_2017</th></tr>'
        for row in cursor:
            ret_str += '<tr><td>' + row[0] + '</td><td>' + row[1] + '</td><td>' + row[2] + '</td><td>' + row[3] + '</td><td>' + row[4] + '</td><td>' + str(row[5]) + '</td><td>' + str(row[6]) + '</td><td>' + str(row[7]) + '</td><td>' + str(row[8]) + '</td><td>' + str(row[9]) + '</td></tr>'

        ret_str += '</table>'
        conn.close()        
        return ret_str

    def build_winner(self):
        """
        Find the player who has won the most tournaments
        """
        ret_str = '<table style="width:100%"> <tr>'
        conn = sqlite3.connect("Melee.db")
        cursor = conn.execute("""Select t.Winner, p.Nationality, p.Character_1, p.Character_2, p.Character_3
                                From Tournaments t, Players p
                                Where t.Winner = p.Tag
                                Group By t.Winner
                                Having Count(t.Winner) = (
						Select Max(c)
						From(
								Select Count(*) as c
								From Tournaments
								Group By Winner
								)
						)""")
        ret_str += '<th>Tag</th><th>Nationality</th><th>Character1</th><th>Character2</th><th>Character3</th></tr>'
        for row in cursor:
            ret_str += '<tr><td>' + row[0] + '</td><td>' + row[1] + '</td><td>' + row[2] + '</td><td>' + row[3] + '</td><td>' + row[4] + '</td></tr>'

        ret_str += '</table>'
        conn.close()        
        return ret_str

    def build_tournaments(self):
        """
        Build the full list of all tournaments
        """
        ret_str = '<table style="width:100%"> <tr>'
        conn = sqlite3.connect("Melee.db")
        cursor = conn.execute("SELECT * FROM tournaments")
        ret_str += '<th>Name</th><th>Entrants</th><th>Country</th><th>City</th><th>State</th><th>Date</th><th>Prize Pool</th><th>Winner</th><th>Place_2</th><th>Place_3</th><th>Place_4</th><th>Place_5</th><th>Place_6</th><th>Place_7</th><th>Place_8</th></tr>'
        for row in cursor:
            ret_str += '<tr><td>' + row[0] + '</td><td>' + str(row[1]) + '</td><td>' + row[2] + '</td><td>' + row[3] + '</td><td>' + row[4] + '</td><td>' + str(row[5]) + '</td><td>' + str(row[6]) + '</td><td>' + str(row[7]) + '</td><td>' + str(row[8]) + '</td><td>' + str(row[9]) + '</td><td>' + str(row[10]) + '</td><td>' + str(row[11]) + '</td><td>' + str(row[12]) + '</td><td>' + str(row[13]) + '</td><td>' + str(row[14]) + '</td></tr>'

        ret_str += '</table>'
        conn.close()        
        return ret_str

    def build_characters(self):
        """
        Build the full list of all characters
        """
        ret_str = '<table style="width:100%"> <tr>'
        conn = sqlite3.connect("Melee.db")
        cursor = conn.execute("SELECT * FROM characters")
        ret_str += '<th>Name</th><th>Series</th><th>Tier</th></tr>'
        for row in cursor:
            ret_str += '<tr><td>' + row[0] + '</td><td>' + row[1] + '</td><td>' + row[2] + '</td></tr>'

        ret_str += '</table>'
        conn.close()        
        return ret_str
        
    def find_file_length(self, path):
        """
        Compute and return the length of the file.
        """
        first = path.find("/")
        if first != 0:    # invalid file name
            return 0

        # now we know the '/' leads the path, remove it
        path = path[1:]
        length = os.path.getsize(path)

        return length

    def check_file(self, path):
        """
        Check to see if file or path exists.
        (for now, we only deal with files, need to handle directories
        """
        first = path.find("/")
        if first != 0:
            return False  # when we handle directory, this needs change

        # now we know the '/' leads the path, remove it
        path = path[1:]

        okay = False
        try:
            okay = os.path.exists(path)
        except OSError:
            pass
        return okay

    def send_file(self, path):
        """
        Read and send the file requested by the client.
        """
        f = None
        data = None
        path = path[1:]
        try:
            f = open(path, "rb")
            data = f.read()
            f.close()
            self.wfile.write(bytes(data))
        except OSError:
            pass

    def check_type(self, path):
        """
        Return the type of the file using some ad-hoc approach.
        """
        file_type = "text/html"  # default
        if path.endswith(".jpg") or \
                path.endswith(".jpeg"):
            file_type = "image/jpeg"      # jpeg image
        elif path.endswith(".png"):
            file_type = "image/png"        # png image
        elif path.endswith(".js"):
            file_type = "text/javascript"  # javascript
        return file_type
        
if __name__ == '__main__':

    httpd = HTTPServer((HOST_NAME, HOST_PORT), MyServer)
    print(time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, HOST_PORT))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, HOST_PORT))
