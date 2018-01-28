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