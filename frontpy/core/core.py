"""
This is core module of application. It contains all exceptions types, Core_meta and Core_element which is the main feature of the framework
which makes it possible to build html tags in python objects.


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
JQUERY_3_2_1_MIN_JS = "234c8514654bb7ed8a60ea905b6f98f0"
BOOTSTRAP_MIN_JS = "13b2a30e265e18a6fd0792cc3fd7a09c"
SCRIPT_JS = "9a9569e9d73f33740eada95275da7f30"
BOOTSTRAP_CSS = "e3202aea761d3d587dfcfc43c6982565"

INVALID_INSERTION_MESSAGE = "You can't use '%s', please try some object from the framework library"
class Invalid_insertion(Exception):
    def __init__(self,message):
        super().__init__(message)
class Empty_web_page(Exception):
    def __init__(self):
        super().__init__("You can't leave page empty, try to add some content with add_element method")
class Unlinked_elements_error(Exception):
    def __init__(self,message):
        super().__init__(message)
class Missing_parameter_error(Exception):
    def __init__(self,message):
        super().__init__(message)
class Unsupported_feature(Exception):
    def __init__(self,message):
        super().__init__(message)
class Core_meta(type):
    """
    This metaclass add special methods of replacing and cleaning after replacing elements.
    It's because simple '%s' usage is not comfortable
    """
    def __new__(cls,name,bases,dct):
        dct["_replace"] = _replace
        dct["_clean"] = _clean
        dct["_generate_trigger"] = _generate_trigger
        dct["_generate_target"] = _generate_target
        return super(Core_meta,cls).__new__(cls,name,bases,dct)

def _replace(self,it,content,index):
    """
    'it' object that contains 'template' field where 'content' will be inserted in place of replacement expression which index is equals to 'index'
    """
    toRm = 0 #Position where the content to be inserted
    count = 0 #Shows which replacement expression has been found
    for i in range(len(it._template)):
        if it._template[i-2]=="|" and it._template[i-1] == "|" and it._template[i]=="|":#Finding replacment expr
            toRm = i-2
            if count == index:#If it's the required expression stop
                break
            else:
                count = count + 1
    if toRm != 0:#If we found sth
        it._template = it._template[:toRm] + content + "|||" + it._template[toRm+3:]

def _clean(self,it,index):
    """
    'it' is object that contains 'template' field and 'index' is the index of replacement expression to be removed
    """
    toRm = 0#Position in the 'template' where the replacement expremession to be removed
    count = 0#Shows current expression
    for i in range(len(it._template)): 
        if it._template[i-2] == "|" and it._template[i-1] == "|" and it._template[i]=="|":#Found some expression
            toRm = i-2#Remeber its position
            if count == index:#If it's the one is required
                break
            else:
                count = count +1
    if toRm != 0:#If sth has been found
        it._template = it._template[:toRm] + it._template[toRm+3:]

def _generate_trigger(self):
    """
    Generetaes classname for html element which will be trigger for some event
    """
    import datetime
    trigger = "%s" % datetime.datetime.now()
    trigger = trigger.split(" ")
    trigger = trigger[0].split("-") + trigger[1].split(".")
    trigger = trigger[0:3] + trigger[3].split(":") + trigger[4:]
    trigger = "".join(trigger) #All operations just remove all signs which is not numbers and creates one unique string
    return trigger
def _generate_target(self,trigger):
    """
    Generates classname for html element which will be changed during the event
    """
    return trigger+"Target"


class Core_element(metaclass=Core_meta):
    """
    This class presents is used to build core elements which is simple html tags
    Private methods (user mustn't use this methods):
        _add_style - to add css style to html element
        _add_class - to add class to html element
        _render - removes all replacement expression
        This list may be extended
    Private fields (user mustn't use this variables):
        _element - shows which html element to be created
        _is_closing - shows if the element has closing tag or not. True - has
        _is_add_attrs - shows if the method has to have attributes. True - has to
        _attributes - list or tuple of attributes that has to be added to the element
        _template - DOM representation of the object
    Public fields:
        add_content - adds any content into element if it's possible
    """
    def __init__(self,element="",is_closing=True,is_add_attrs=True,attributes=[]):
        self._element = element
        self._is_closing = is_closing
        self._attributes = attributes
        self._index = 0#Shows which attribute from _attributes is now in processing
        self._is_add_attrs = is_add_attrs
        self._indexes_list = dict()#Dictionary which will contain {nameOfAttribute:indexToInsertContent}
        if self._is_closing:#If tag has to be closed
            self._template = """<%s|||>|||</%s>""" % (element,element)
        else:#If tag doesn't have to be closed
            self._template = """<%s|||>""" % element
        if self._is_add_attrs:
            for i in attributes:
                self._replace(self," "+i+'="|||"',self._index) #Add attribute
                self._indexes_list[i] = self._index#Save the name of attribute and its index(for _replace method)
                self._index += 1
            self._clean(self,self._index)#And clean replacement expression which has been used to add attributes
            if self._is_closing:#If tag has to be closed then
                self._indexes_list["content"] = self._index#It can have some content
        else:
            self._clean(self,self._index)#If no attributes just clean replacement expression for attributes
            if self._is_closing:
                self._indexes_list["content"] = self._index#If tag has to be closed then save index for _replace method
    def __str__(self):
        import copy
        cop = copy.deepcopy(self)
        cop._render()
        return cop._template

    def __call__(self,*content):
        import copy
        cop = copy.deepcopy(self)
        cop.add_content(*content)
        cop._render()
        return cop._template
    
    def _add_style(self,styles):
        """
        Add style to html element
        styles - JSON like object which contains css properties like {"name":"value"}
        """
        self._styles = styles
        if "style" in self._indexes_list:
            for i in self._styles:
                self._replace(self,"%s:%s; " % (i,self._styles[i]),self._indexes_list["style"])
    def _add_class(self,*cls):
        """
        Add classes
        *cls - tuple of classes to be added
        """
        self._cls = cls#represents classes of html tag
        if "class" in self._indexes_list:
            for i in self._cls:
                self._replace(self,"%s " % i,self._indexes_list["class"])
    def _add_attr_value(self,attr,value):
        if attr in self._indexes_list:
            self._replace(self,value,self._indexes_list[attr])

                    
    def add_content(self,*content):
        """
        Add content which is str or any object that contains _template field
        """
        self._content = content#Represents content to be added to 'self' object
        for i in self._content:
            if type(i) is str:#If content is str
                if "content" in self._indexes_list:#and it's field to add content
                    self._replace(self,i,self._indexes_list["content"])
            else:#If content is some object
                if "content" in self._indexes_list:
                    try:
                        import copy
                        cop = copy.deepcopy(i)#Deep copy because original object can be chenged later
                        cop._render()
                        self._replace(self,cop._template,self._indexes_list["content"])
                    except AttributeError:
                        raise Invalid_insertion(INVALID_INSERTION_MESSAGE % i)
    def _render(self):
        """
        Preparing object to be used. REQURIED METHOD
        """
        for i in self._indexes_list:#Clean all replacement expressions
            self._clean(self,0)
    def _link_elements(self,targets=[]):
        """
        Links number of elemnts to make them avaliable to add event. self is a trigger, other elements are targets
        """
        self._trigger = self._generate_trigger() #classname for tag which will emit the event
        self._target = self._generate_target(self._trigger)#classname for tag which will be changed during the event
        if targets:
            for i in targets:
                try:#If sth not from framework has been passed
                    if "class" in i._indexes_list:
                        i._replace(i, "%s " % self._target,i._indexes_list["class"])
                    else:
                        raise Missing_parameter_error("Add attribute 'class' for html element %s" % i)
                except AttributeError:
                    raise Invalid_insertion(INVALID_INSERTION_MESSAGE % i)
        else:
            raise Unlinked_elements_error("You haven't linked any elements to create events between them")
        if "class" in self._indexes_list:
            try:#Just for safety
                self._replace(self,"%s " % self._trigger,self._indexes_list["class"])
            except AttributeError:
                raise Invalid_insertion(INVALID_INSERTION_MESSAGE % self)
        else:
            raise Missing_parameter_error("Add attribute 'class' for html element %s" % i)
    def _add_script(self,toDo):
        """
        Creates jquery interpritation of event for browsers
        """
        with open("./pages/scripts/script.js","a") as script:
            script.write(toDo)
    def on_click(self,toDo,targets=[],params={}):
        """
        Args:
        the first - some predefined word
        the second - elemetns which have to be involved as targets
        the third - dictionary with parametres if they are required
        """
        self._link_elements(targets)
        self._on_clickParams = params
        if toDo == "changeColor":
            self._add_script(";(function(){var changed = false;var color = $('.%s').css('color');$('.%s').click(function(event){event.stopPropagation();if(changed){$('.%s').css({'color':color});changed = false;}else{$('.%s').css({'color':'%s'});changed = true;}});})();"%(self._target,self._trigger,self._target,self._target,self._on_clickParams["color"]))
        else:
            raise Unsupported_feature("'%s' event for click is unsupported, please write to author lds4ever2000@gmail.com" % toDo)


class Page(Core_element):
    def __init__(self,title,encoding,background={}):
        self._mimetype = "text/html"
        self.title = title
        self.encoding = encoding
        super().__init__("div",True,True,["class","style"])
        self._add_class("global")
        if background:
            self._add_style(background)
        self._tmp = """
<!DOCTYPE html>
<!--
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
-->
<html>
        <head>             
        <title>%s</title>
        <meta charset="%s">
        <base href="/">
        <link rel="icon" href="favicon.ico" type="image/x-icon"/>
        <link rel="shortcut icon" href="favicon.ico" type="image/x-icon"/>
        <link rel="stylesheet" type="text/css" href="%s">
    </head>            
    <body style="margin-top:-16px;">
            %s
        <script src="%s"></script>
        <script src="%s"></script>
        <script src="%s"></script>
        <script>hljs.initHighlightingOnLoad();</script>
    </body>
</html>
        """
    def add_element(self,*content):
        for i in content:
            self.add_content(i)
    def set_titile(self,title):
        self.title = title
    def set_background(self,background):
        self._add_style(background)
    def _render(self):
        self._template = self._tmp % (self.title,self.encoding,BOOTSTRAP_CSS,self._template,JQUERY_3_2_1_MIN_JS,BOOTSTRAP_MIN_JS,SCRIPT_JS)
        super()._render()



###############################################################
"""
Server Side
"""
JQUERY_3_2_1_MIN_JS = "234c8514654bb7ed8a60ea905b6f98f0"#Constants which encode filenames with required scripts
BOOTSTRAP_MIN_JS = "13b2a30e265e18a6fd0792cc3fd7a09c" 
SCRIPT_JS = "9a9569e9d73f33740eada95275da7f30"
BOOTSTRAP_CSS = "e3202aea761d3d587dfcfc43c6982565"

AVALIABLE_FORMATS = ("jpg","png","svg","map","ico","js","css") #Formats of files that can be loaded automatically from pages/media folder

from http.server import HTTPServer, BaseHTTPRequestHandler
def make_name(address):
    """
    Make unique name for function from request.path
    """
    address = address.split("/")
    address = "_aa".join(address)
    return address
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

def serve(address):
    """
    Function is used to put user definded function to the request handler
    """
    def decorator(fn,address=address):
        def decorated(address=address):
            address = make_name(address)
            setattr(Core_http_process,address,fn)
        decorated()
        return decorated
    return decorator

#This functions is used to load special scripts
@serve("/%s"%BOOTSTRAP_CSS)
def je3202aea761d3d587dfcfc43c6982565(request):
    #createResponse(request,200,"text/css")
    with open("static/styles/bootstrap.css","r") as bootstrap:
        return (bootstrap.read(),"text/css")


@serve("/%s"%JQUERY_3_2_1_MIN_JS)
def j234c8514654bb7ed8a60ea905b6f98f0(request):
    with open("static/scripts/jquery-3.2.1.min.js","r") as jquery:
        return(jquery.read(),"script/javascript")


@serve("/%s"%BOOTSTRAP_MIN_JS)
def j13b2a30e265e18a6fd0792cc3fd7a09c(request):
    with open("static/scripts/bootstrap.min.js","r") as bootstrap:
        return(bootstrap.read(),"script/javascript")


@serve("/%s" % SCRIPT_JS)
def j9a9569e9d73f33740eada95275da7f30(request):
    with open("static/scripts/script.js","r") as script:
        return(script.read(),"script/javascript")


def run_app(address="localhost",server=HTTPServer,handler=Core_http_process,port=8000):
    server_address = (address,port)
    http = server(server_address,handler)
    print("""
Front-py  Copyright (C) 2018  Dima Lukashov <lds4ever2000@gmail.com>
This program comes with ABSOLUTELY NO WARRANTY; for details see LICENSE.md.
This is free software, and you are welcome to redistribute it
under certain conditions; For details see LICENSE.md.\n""")
    print("Started server at %s on port %s" % (address,port))
    http.serve_forever()
