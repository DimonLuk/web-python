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

debug = False
def prepare_import(*folders):
    import sys
    import __custom_import__ as cm
    cur_dir = (lambda x:"/".join([i for i in x[:-1]]))(cm.__file__.split("/"))
    up_dir = (lambda x:"/".join([i for i in x[:-1]]))(cur_dir.split("/"))
    sys.path.append(cur_dir)
    sys.path.append(up_dir)
    for i in folders:
        sys.path.append(cur_dir+"/"+i)
    if debug:
        print(sys.path)
if __name__ == "__main__":
    prepare_import()
