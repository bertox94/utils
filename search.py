from __future__ import print_function
import ctypes
import glob
import msvcrt
import os
import re
import subprocess
import sys
import time
from distutils.dir_util import copy_tree
from pathlib import Path
from shutil import copy, copyfile, rmtree

flag = True
filesearchresult = Path("filesearchresult")
foldersearchresult = Path("foldersearchresult")
searchpath = Path("C:/Users/alt/vcpkg")
pattern = None
# pattern = re.compile("([A-Z][0-9]+)+")
searchoption = 'buildtrees/**/src/**/*.lua'


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def _mkdir(kk):
    pk = Path(*(kk.parts[:- 1]))
    if not pk.is_dir():
        _mkdir(pk)
    os.mkdir(kk)


def setupfolders():
    if not os.path.isdir(filesearchresult):
        os.mkdir(filesearchresult)
    else:
        rmtree(filesearchresult)
        os.mkdir(filesearchresult)

    if not os.path.isdir(foldersearchresult):
        os.mkdir(foldersearchresult)
    else:
        rmtree(foldersearchresult)
        os.mkdir(foldersearchresult)


def execfilesearch(path, num):
    print(f"\t{str(path) + '...':<85}", end="", flush=True)
    t2 = Path(*(path.parts[num:]))
    kk = filesearchresult.joinpath(Path(*(path.parts[num: - 1])))
    if not kk.is_dir():
        _mkdir(kk)
    copyfile(str(path), str(filesearchresult.joinpath(t2)))
    print("Successful.")


def searchfiles(regex):
    num = len(searchpath.parts[:])
    paths = searchpath.glob(searchoption)
    flag2 = False
    for path in paths:
        flag2 = True
        if path.is_file():
            if regex:
                f = open(path, 'r', encoding='utf-8')
                content = f.read()
                if bool(re.search(regex, content)):
                    execfilesearch(path, num)
            else:
                execfilesearch(path, num)

    if not flag2:
        print("Nothing has been found.")


def searchfolders():
    paths = searchpath.glob(searchoption)
    flag2 = False
    for path in paths:
        flag2 = True
        if path.is_dir():
            print(f"\t{str(path) + '...':<85}", end="", flush=True)
            copy_tree(str(path), str(foldersearchresult.joinpath(path.name)))
            print("Successful.")

    if not flag2:
        print("Nothing has been found.")


def main():
    global flag
    setupfolders()
    searchfiles(pattern)
    searchfolders()


if __name__ == "__main__":
    if is_admin():
        main()
        print("\n")
        if flag:
            print("Press any key to continue...")
            if msvcrt.getch():
                pass
        else:
            print("==========================")
            print("Done")
            time.sleep(3)
    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, "\"" + sys.argv[0] + "\"", None, 1)
