"""
Copyright (C) 2018  Dima Lukashov github.com/DimonLuk
    
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
      
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from http.server import BaseHTTPRequestHandler

class Core_http_process(BaseHTTPRequestHandler):
    """
    Class that handles requests from the users
    Now it can process only GET requests but of course it will process both GET and POST requests
    addresses can be pattern like. For example /page/<any> handles any address like /page/123, /page/Dima,
    but not /sth/page/sth and etc.
    
    """
    def __init__(self,a,b,c):
        super().__init__(a,b,c)
    def do_GET(self):
        """
        Handles GET request.
        At first try to download files from static/media folder
        Then from user hardly defined addresses(that not include <any> in argument for serve decorator)
        Then addresses that contain <any>
        """
        self._find = self.path.split(".")#Files in media are sth like this name.extension
        self.request = _request(self.path,"GET")#Create request parametr that can be used by user
        if self._find[-1] in AVALIABLE_FORMATS:
            with open("static/media%s" % self.path,"rb") as sth:
                self._response = sth.read()
                if self._find[-1] == "map":
                    self._send_response("application/json")
                else:
                    if self._find[-1] == "ico":
                        self._send_response("image/x-icon")
                    else:
                        self._send_response("image/"+self._find[-1])
                self.wfile.write(self._response)
            return "OK"
        self.name = make_name(self.path)#Okey, it's not a file from media, it may be user hardly defined address
        self._response = b""#Has to be bytes
        try:#Check if the required function exists
            self._resp = self.__class__.__dict__[self.name](self.request)#Call it
            if type(self._resp) is tuple:#If core defined function has been called, it's tuple 0 - file itself, 1 - mimetype
                self._response = bytes(self._resp[0].encode("utf-8"))
                self._send_response(self._resp[1])
                self.wfile.write(self._response)
            elif type(self._resp) is Page:#If it's user defined function, than its type is WebPage
                self._resp._render()
                self._response = bytes(self._resp._template.encode("utf-8"))
                self._send_response(self._resp._mimetype)
                self.wfile.write(self._response)
            else:
                raise Unsupported_feature(INVALID_INSERTION_MESSAGE % self._resp)
        except KeyError as kr:
            self._anys = [i for i in self.__class__.__dict__ if "<any>" in i]#Find all fuctions that contains <any>
            tmp1 = make_name(self.path).split("_aa")#And make name from path
            for i in self._anys:
                tmp2 = i.split("_aa")
                specific = True
                #Let's take for example self.path = /page/123 and i = /page/<any>
                #so tmp1 = ["_aapage","_aa123"] tmp2=["_aapage","_aa<any>"]
                if len(tmp1) == len(tmp2):#So lengths are equals
                    for j in range(0,len(tmp1)):
                        if tmp1[j] != tmp2[j] and not "<any>" in tmp2[j]:#If arguments are not equals but not in places where tmp2 is "_aa<any>"
                            specific = False#We don't have to process such request 
                else:
                    specific = False
                if specific:
                    self._resp = self.__class__.__dict__[i](self.request)
                    self._resp._render()
                    self._response = bytes(self._resp._template.encode("utf-8"))
                    self._send_response(self._resp._mimetype)
                    self.wfile.write(self._response)
                    return "OK"
    def _send_response(self,typ):
        self.send_response(200)#Nothing interesting here
        self._send_headers(typ)
    def _send_headers(self,typ):
        self.send_header("Content-type",typ)
        self.end_headers()

class _request:
    """
    To incapsulate request
    Nothing interestig right now
    """
    def __init__(self,path,method,headers={},body={}):
        self.path = path
        self.method = method
        self.headers = headers
        self.body = body
