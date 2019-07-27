#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Use text editor to edit the script and type in valid Instagram username/password

from InstagramAPI import InstagramAPI

api = InstagramAPI("smg7d", "Frmby_89")
if (api.login()):
    api.getSelfUserFeed()  # get self user feed
    #print(api.LastJson)  # print last response JSON
    print("Login success!")
else:
    print("Can't login!")
