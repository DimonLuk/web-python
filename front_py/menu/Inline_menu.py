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

class Inline_menu(e._Block_element):
    """
    Simple inline bootstrap menu

    The first argument is json represantion of background like {"background":"<some color here>"}
    The second is json like links {"Home":"/","Any page":"/any"}
    The third is color of links
    The fourth is Brand_text or Brand_image object

    If you call this object you'll get deepcopy of it
    """
    def __init__(self, background, links, links_color,brand):
        """
        It has been used a lot of bootstrap features here
        Nothing to describe.
        Just create required element and configure according to bootstrap
        """
        self.background = background
        self.links = links
        self.links_color = links_color
        self.brand = brand
        super().__init__()
        self._add_style(background)

        self.header = e._Header_element()
        self.header._add_class("container")
        self.header._add_style(self.background)
        
        
        self.menu = e._Menu_element()
        self.menu._add_class("row")

        self.navigation = e._Navigation_element()
        self.navigation._add_class("navbar","navbar-toggleable-md","navbar-inverse","bg-faded","col-12","mx-auto")
        self.navigation._add_style(self.background)

        self.collapse_button = e._Button_element(text="",attributes=["class","style","type","data-toggle","data-target","aria-controls","aria-expanded","aria-label"])
        self.collapse_button._add_class("navbar-toggler","navbar-toggler-right")
        self.collapse_button._add_attr_value("type","button")
        self.collapse_button._add_attr_value("data-toggle","collapse")
        self.collapse_button._add_attr_value("data-target",".toggleTarget")
        self.collapse_button._add_attr_value("aria-controls","toggleTarget")
        self.collapse_button._add_attr_value("aria-expanded","false")
        self.collapse_button._add_attr_value("aria-label","Toggle navigation")

        self.toggle_icon = e._Text_element()
        self.toggle_icon._add_class("navbar-toggler-icon")
        self._add_style({"color":"white"})
        self.collapse_button.add_content(self.toggle_icon)
        
        self.nav_block = e._Block_element()
        self.nav_block._add_class("collapse","navbar-collapse","toggleTarget")

        self.links_list = e._Unnumbered_list_element()
        self.links_list._add_class("navbar-nav","mr-left")

        for i in self.links:
            li = e._In_list_element()
            li._add_class("nav-item","active")
            for j in i:
                href = e._Link_element(i[j])
                href.add_content(j)
                href._add_class("nav-link")
                href._add_style({"color":self.links_color})
                li.add_content(href)

            self.links_list.add_content(li)
    def _render(self):
        self.nav_block.add_content(self.links_list)
        self.navigation.add_content(self.collapse_button,self.brand,self.nav_block)
        self.menu.add_content(self.navigation)
        self.header.add_content(self.menu)
        self.add_content(self.header)
        super()._render()
    
    def _add_link(self,links,color=""):
        for link in links:
            li = e._In_list_element()
            li._add_class("nav-item","active")

            href = e._Link_element(links[link])
            href.add_content(link)
            href._add_class("nav-link")
            if color:
                href._add_style({"color":color})
            else:
                href._add_style({"color":self.links_color})
            
            li.add_content(href)
            self.links_list.add_content(li)
    def __call__(self,links={},color=""):
        import copy
        cop = copy.deepcopy(self)
        if links:
            cop._add_link(links,color)
        return cop
    
    def add_links(self,links,color=""):
        return self(links,color)
