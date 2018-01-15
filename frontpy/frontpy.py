"""
This module is the main part of the framework where everything is connected.
Soon, it'll be split up on some modules like containers and etc


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
import sys
sys.path.append(sys.path[0]+"/frontpy")
sys.path.append(sys.path[0]+"/frontpy/core")
import elements as e
from core.core import CoreElement,serve,runApp,Page

class Text(e._TextElement):
    """
    Simple text
    The first argument of constructor is text which will be shown it's nit required
    
    It can be used as wrapper, you can define some simple styles and use it to wrap text
    For example:
    greenText = Text()
    greenText.color = "green" or greenText.addStyle({"color":"green"})
    p = Paragraph("Some %s text" % greenText("green"))
    
    Or you can use this class in usual way
    """
    def __init__(self,text=""):
        super().__init__(text=text)
    def __str__(self):
        import copy
        cop = copy.deepcopy(self)
        cop._render()
        return cop._template
    def __setattr__(self,name,value):
        if name == "color":
            self._addStyle({"color":value})
        elif name == "position" and value == "center":
            self._addClass("mx-auto")#To place in center in .container > .row
            self._addStyle({"text-align":value})#Sometimes it's useful
        else:
            self.__dict__[name] = value
    def addStyle(self,style):
        self._addStyle(self,style)
    def __call__(self,value):
        """
        Implemenation of wrapping syntax
        """
        import copy
        cop = copy.deepcopy(self)
        cop.addContent(value)
        cop._render()
        return cop._template

class Paragraph(e._ParagraphElement):
    """
    Simple paragraph
    The first argument is text which is not required
    """
    def __init__(self,text=""):
        super().__init__(text=text)

class Image(e._ImageElement):
    """
    Simple responsive image
    """
    def __init__(self,href,alt="picture"):
        super().__init__(href,alt=alt)
        self._addClass("img-fluid")
    def __str__(self):
        import copy
        cop = copy.deepcopy(self)
        cop._render()
        return cop._template

class BlockContainer(e._BlockElement):
    """
    Is used to build complex structures, sometimes can be useful for user, so no '_' in the begining of name
    """
    def __init__(self):
        super().__init__()
        self._addClass("container")

class SectionContainer(e._SectionElement):
    """
    The same as block but section, only semantic difference
    """
    def __init__(self):
        super().__init__()
        self._addClass("container")

class BlockRow(e._BlockElement):
    """
    Simple row
    """
    def __init__(self):
        super().__init__()
        self._addClass("row")

class ContainerRow(BlockContainer):
    """
    Creates row inside a BlockContainer
    """
    def __init__(self):
        super().__init__()
        self.row = BlockRow()
    def addContent(self,content):
        self.row.addContent(content)
    def _render(self):
        super().addContent(self.row)
        super()._render()

class SectionRow(SectionContainer):
    """
    Creates a row inside SectionContainer
    """
    def __init__(self):
        super().__init__()
        self.row = BlockRow()
    def addContent(self,content):
        self.row.addContent(content)
    def _render(self):
        super().addContent(self.row)
        super()._render()



class InlineMenu(e._BlockElement):
    """
    Simple inline bootstrap menu

    The first argument is json represantion of background like {"background":"<some color here>"}
    The second is json like links {"Home":"/","Any page":"/any"}
    The third is color of links
    The fourth is BrandText or BrandImage object
    """
    def __init__(self, background, links, linksColor,brand):
        """
        It has been used a lot of bootstrap features here
        Nothing to describe.
        Just create required element and configure according to bootstrap
        """
        self.background = background
        self.links = links
        self.linksColor = linksColor
        self.brand = brand
        super().__init__()
        self._addStyle(background)

        self.header = e._HeaderElement()
        self.header._addClass("container")
        self.header._addStyle(self.background)
        
        
        self.menu = e._MenuElement()
        self.menu._addClass("row")

        self.navigation = e._NavigationElement()
        self.navigation._addClass("navbar","navbar-toggleable-md","navbar-inverse","bg-faded","col-12","mx-auto")
        self.navigation._addStyle(self.background)

        self.collapseButton = e._ButtonElement(text="",attributes=["class","style","type","data-toggle","data-target","aria-controls","aria-expanded","aria-label"])
        self.collapseButton._addClass("navbar-toggler","navbar-toggler-right")
        self.collapseButton._addAttrValue("type","button")
        self.collapseButton._addAttrValue("data-toggle","collapse")
        self.collapseButton._addAttrValue("data-target",".toggleTarget")
        self.collapseButton._addAttrValue("aria-controls","toggleTarget")
        self.collapseButton._addAttrValue("aria-expanded","false")
        self.collapseButton._addAttrValue("aria-label","Toggle navigation")

        self.toggleIcon = e._TextElement()
        self.toggleIcon._addClass("navbar-toggler-icon")
        self._addStyle({"color":"white"})
        self.collapseButton.addContent(self.toggleIcon)
        
        self.navBlock = e._BlockElement()
        self.navBlock._addClass("collapse","navbar-collapse","toggleTarget")

        self.linksList = e._UnnumberedListElement()
        self.linksList._addClass("navbar-nav","mr-left")

        for i in self.links:
            li = e._InListElement()
            li._addClass("nav-item","active")

            href = e._LinkElement(self.links[i])
            href.addContent(i)
            href._addClass("nav-link")
            href._addStyle({"color":self.linksColor})

            li.addContent(href)

            self.linksList.addContent(li)
        self.navBlock.addContent(self.linksList)
        self.navigation.addContent(self.collapseButton,self.brand,self.navBlock)
        self.menu.addContent(self.navigation)
        self.header.addContent(self.menu)
        self.addContent(self.header)




class BrandText(e._LinkElement):
    """
    Company name or other brand short and nice info

    The first argument is text
    The second is color
    """
    def __init__(self,text="",color="#ffffff"):
        super().__init__(href="")
        self.color = color
        self.text = text
        self._addClass("navbar-brand")
        self._addStyle({"color":self.color})
        self._addAttrValue("href","#")
        self.addContent(self.text)

class BrandImage(BrandText):
    """
    Company logo
    The firts arg is name of the picture which is inside the media folder of the project
    The second is text to be displayed if picture can't be loaded
    """
    def __init__(self,imageName,alt):
        super().__init__()
        self.img = e._ImageElement(imageName,alt)
        self.addContent(self.img)

class RowArticles(SectionRow):
    """
    Creates a lot of articles. Each article in one single row
    
    The first argument is title of all articles| not required
    The second is position, now only center or nothing allowed| not required

    Use 'config' method to set your preferences for all articles
    """
    def __init__(self,sectionTitle="",position="center"):
        super().__init__()
        if sectionTitle:
            self.sectionTitle = sectionTitle
            header = e._HeaderElement()
            if position == "center":
                header._addClass("mx-auto")
            h = e._HeaderTextElement(1,self.sectionTitle)
            header.addContent(h)
            self.addContent(header)
    
    def config(self,horizontalDistance="", horizontalLine=False, headersLevel=2):
        """
        Sets preferences which will be used to display all articles
        """
        self.horizontalLine = horizontalLine
        self.headersLevel = headersLevel
        if horizontalDistance:
            self.horizontalDistance = horizontalDistance
    def addArticle(self,headerText="",text="",footer=""):
        article = e._ArticleElement()
        article._addClass("col-12")
        header = {}
        paragraph = {}
        foot = {}
        if headerText:
            header = e._HeaderElement()
            h = e._HeaderTextElement(self.headersLevel,headerText)
            
            header.addContent(h)
            article.addContent(header)
        
        if text:
            paragraph = e._ParagraphElement(text)
            article.addContent(paragraph)
        
        if footer:
            #TODO
            pass
        
        if self.horizontalLine:
            article.addContent(e._HorizontalLine())
        if self.horizontalDistance:
            article._addStyle({"margin-top":self.horizontalDistance})
        self.addContent(article)


class Footer(e._FooterElement):
    def __init__(self,content="",width=30):
        super().__init__()
        self._addClass("footer")
        self.row = ContainerRow()

        if content:
            self.row.addContent(content)
        self.width = width
        self._addStyle({"padding-top":"%spx"% (width/2),"padding-bottom":"%spx"% (width/2)})

    def addContent(self,content):
        self.row.addContent(content)
    def _render(self):
        super().addContent(self.row)
        super()._render()
    def __setattr__(self,name,value):
        if name == "BackgroundColor":
            self._addStyle({"background":value})
        else:
            self.__dict__[name] = value