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


class SectionContainer(e._SectionElement):
    """
    The same as block but section, only semantic difference
    """

    def __init__(self):
        super().__init__()
        self._add_class("container")








import unittest


class Test(unittest.TestCase):

    def test_SectionContainer(self):
        self.assertEqual("""<section class="container " style=""></section>""", SectionContainer().__str__())