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
from core import elements as e


class BrandText(e._LinkElement):
    """
    Company name or other brand short and nice info

    Parameters
    ----------
    text: str
        name of company or important data to be displayed
    color: str
        color of the text
    """

    def __init__(self, text="", color="#ffffff"):
        super().__init__(href="")
        self.color = color
        self.text = text
        self._add_class("navbar-brand")
        self._add_style({"color": self.color})
        self._add_attr_value("href", "#")
        self.add_content(self.text)


class BrandImage(BrandText):
    """
    Company logo
    The firts arg is name of the picture which is inside the media folder of the project
    The second is text to be displayed if picture can't be loaded

    Parameters
    ----------
    imageName: str
        name of image which is within static/media folder
    alt: str
        alternative text for people who can't see images
    """

    def __init__(self, imageName, alt):
        super().__init__()
        self.img = e._ImageElement(imageName, alt)
        self.add_content(self.img)








import unittest


class Test(unittest.TestCase):

    def test_BrandText(self):
        self.assertEqual("""<a class="navbar-brand " style="color:#ffffff; " href="#"></a>""", BrandText().__str__())

    def test_BrandImage(self):
        self.assertEqual("""<a class="navbar-brand " style="color:#ffffff; " href="#"><img class="" style="" src="test" alt="test" /></a>""", BrandImage("test", "test").__str__())
