# -*- coding:utf-8 -*-
import os.path
def fileCount(rootDir):

    i = 0
    for parent, dirnames, filenames in os.walk(rootDir):
        for filename in filenames:
           i=i+1

    return i
