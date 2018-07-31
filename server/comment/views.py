# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
import json

from django.shortcuts import render

# Create your views here.
#! /usr/local/bin/env python3

import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
from collections import OrderedDict
import time
import json, os
import functools
import datetime
from datetime import datetime as dt


Cache = functools.lru_cache(maxsize=256)

ALL_USER = ('ningz', 'mengc', 'yixuanw', 'minghuiw', 'hhan',
            'jiangx', 'lid', 'luwang', 'huilinw', 'ljingying',
            'dayuw', 'chaofengw', 'yex', 'bdang', 'dpang',
            'yhu')

#START_DATE = datetime.date(2018, 5, 10)
#END_DATE = datetime.date(2018, 6, 10)
now = datetime.datetime.now()
nowe = now.isoweekday()
if nowe<7:
    endDay = now - datetime.timedelta(days = nowe)
#elif nowe ==7:
    #endDay=now - datetime.timedelta(days = 1)
else :
    endDay=now
lastDay = endDay - datetime.timedelta(days = 56)
#print(str(nextDay.year)+":"+str(nextDay.month)+":"+str(nextDay.day))
START_DATE = lastDay
END_DATE = endDay
class User():
    def __init__(self, id, login_name, full_name, mgr):
        self.id = id
        self.login_name = login_name
        self.full_name = full_name
        self.mgr = mgr

    def __str__(self):
        return self.login_name


class DataBase():
    """
    """
    def __init__(self):
        self.cursor = self.ConnectDatabase()
        self.user_id_map = OrderedDict()  #{'login_name': Class of User}

    def ConnectDatabase(self):
        """
        @param host - server name
        @param user - mts
        @param passwd - ***
        @param db - database
        """
        conn =  MySQLdb.connect(host='bz3-db3.eng.vmware.com',
                                user = 'mts',
                                passwd = 'mts' ,
                                db = 'bugzilla'
                                )
        cursor = conn.cursor()
        return cursor

    def GetSqlOutput(self, cmd):
        """

        :param cmd:
        :return:
        """
        self.cursor.execute(cmd)
        return self.cursor.fetchall()

    @Cache
    def get_user_by_login_name(self, username):
        """
        @param username: e.g. ningz
        :return: True/False
        """
        id_query = 'select userid, login_name, realname, manager_id from profiles' \
                   ' where login_name="%s"' % username
        users = self.GetSqlOutput(id_query)
        #print (users)
        if not users:
            print ('Can not get %s user info from database.' % username)
            return False
        user = users[0]
        try:
            one_user = User(user[0], user[1], user[2], user[3])
            return one_user
        except:
            print ('Check output (%s) failed.' % user)
            return False

    def SetupAllUsers(self, login_users):
        """
        @param login_users: ['ningz', 'jiangx', 'yixuanw']
        :return:
        """
        for login_id in login_users:
            user = self.get_user_by_login_name(login_id)
            if not user:
                print ('Can not search %s from database.' % login_id)
                continue
            self.user_id_map[login_id] = user

    def GetBugNum(self, users, start_date, end_date):
        """

        :param users:
        :param start_date:
        :param end_date:
        :return:
        """
        data = {} # {'date':{'user1':number, 'user2':number}}
        query_t = 'select b.bug_id, l.thetext '\
                  'from longdescs l, bugs b '\
                  'where b.bug_id=l.bug_id and l.who=%s ' \
                  'and l.bug_when >= "%s" and l.bug_when < "%s"'
        all_weeks = get_week_days(start_date, end_date)
        for week_start, week_end in all_weeks:
            day = week_end.split()[0] #The Sunday date
            data[day] = {}
            for user in users:
                query = query_t % (self.user_id_map[user].id, week_start, week_end)
                info = self.GetSqlOutput(query)
                data[day][user] = len(info)
        return data

    def GetAllPeopleData(self, users, start_date, end_date):
        """

        :param users: login username list.
        :param start_date: datetime.date type date. e.g. datetime.date(2018, 4, 1)
        :param end_date: Same as start_date
        :return:
        """
        self.SetupAllUsers(ALL_USER)
        data = self.GetBugNum(self.user_id_map.keys(), START_DATE, END_DATE)
        return data

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders it's content into JSON.
    """

    def __init__(self, data, **kwargs):
        self.data = data
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

def Draw16in1Picture(data, users):
    """

    :param data: {date1:{user1:c_num, user2:c_num}}
    :param users: {'login_name': Class of User}
    :return:
    """
    # libraries and data
    #import matplotlib.pyplot as plt
    #import numpy as np
    #import pandas as pd

    # Make a data frame

    # df=pd.DataFrame({'x': range(1,11), 'y1': np.random.randn(10), 'y2': np.random.randn(10)+range(1,11), 'y3': np.random.randn(10)+range(11,21),
    #                 'y4': np.random.randn(10)+range(6,16), 'y5': np.random.randn(10)+range(4,14)+(0,0,0,0,0,0,0,-3,-8,-6), 'y6': np.random.randn(10)+range(2,12),
    #                 'y7': np.random.randn(10)+range(5,15), 'y8': np.random.randn(10)+range(4,14), 'y9': np.random.randn(10)+range(4,14) })
    #print(data)         'dates': [],
    dates = data.keys()
    dates = sorted(dates)
    names = list(users.keys())
    res = {
        'y01': [],
        'y02': [],
        'y03': [],
        'y04': [],
        'y05': [],
        'y06': [],
        'y07': [],
        'y08': [],
        'y09': [],
        'y10': [],
        'y11': [],
        'y12': [],
        'y13': [],
        'y14': [],
        'y15': [],
        'y16': [],
	
    }
    #print(df)
    # Initialize the figure
#    res['dates']=[dt.strptime(d, '%Y-%m-%d').date() for d in dates]
    res['y01']= [data[d][names[0]] for d in dates]
    res['y02']= [data[d][names[1]] for d in dates]
    res['y03']= [data[d][names[2]] for d in dates]
    res['y04']= [data[d][names[3]] for d in dates]
    res['y05']= [data[d][names[4]] for d in dates]
    res['y06']= [data[d][names[5]] for d in dates]
    res['y07']= [data[d][names[6]] for d in dates]
    res['y08']= [data[d][names[7]] for d in dates]
    res['y09']= [data[d][names[8]] for d in dates]
    res['y10']= [data[d][names[9]] for d in dates]
    res['y11']= [data[d][names[10]] for d in dates]
    res['y12']= [data[d][names[11]] for d in dates]
    res['y13']= [data[d][names[12]] for d in dates]
    res['y14']= [data[d][names[13]] for d in dates]
    res['y15']= [data[d][names[14]] for d in dates]
    res['y16']= [data[d][names[15]] for d in dates]
    r=[res]
    return res
    
def get_week_days(start_date, end_date):
    """
    :param start_date: the start day.
    @param end_date: the end day.
    :return: week day list start from start_date and end of end_date.
            Start from Sunday 00:00:00 to next Sunday 00:00:00
            e.g. [('2018-05-06 00:00:00', '2018-05-13 00:00:00'),
                ('2018-05-13 00:00:00', '2018-05-20 00:00:00')]
    """
    if not start_date or not end_date:
        print ('You need to input start date and end date.')
        return []
    if (end_date - start_date).days < 0:
        return []
    result = []
    from_date = start_date
    to_date = find_next_sunday(start_date)
    while (end_date-to_date).days > 0:
        result.append(('%s 00:00:00' % from_date.strftime("%Y-%m-%d"),
                       '%s 00:00:00' % to_date.strftime("%Y-%m-%d")))
        from_date = to_date
        to_date = find_next_sunday(from_date)
    result.append(('%s 00:00:00' % from_date.strftime("%Y-%m-%d"),
                   '%s 00:00:00' % end_date.strftime("%Y-%m-%d")))
    return result

def find_next_sunday(date):
    """
    :param date:
    :return: The next sunday
    """
    days_ahead = 6 - date.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return date + datetime.timedelta(days_ahead)

#if __name__ == "__main__":
def main(self):
    db = DataBase()
    data = db.GetAllPeopleData(ALL_USER, START_DATE, END_DATE)
    #for test data = {'2018-05-07': {'ningz': 11, 'mengc': 13, 'zlai': 30, 'yixuanw': 6, 'yex': 1, 'minghuiw': 13, 'hhan': 3, 'jiangx': 4, 'sganamur': 8}, '2018-05-14': {'ningz': 19, 'mengc': 14, 'zlai': 43, 'yixuanw': 15, 'yex': 5, 'minghuiw': 38, 'hhan': 7, 'jiangx': 10, 'sganamur': 14}, '2018-05-21': {'ningz': 11, 'mengc': 14, 'zlai': 19, 'yixuanw': 23, 'yex': 8, 'minghuiw': 26, 'hhan': 2, 'jiangx': 10, 'sganamur': 6}, '2018-05-28': {'ningz': 2, 'mengc': 1, 'zlai': 3, 'yixuanw': 12, 'yex': 1, 'minghuiw': 1, 'hhan': 2, 'jiangx': 1, 'sganamur': 1}, '2018-05-31': {'ningz': 1, 'mengc': 1, 'zlai': 1, 'yixuanw': 1, 'yex': 1, 'minghuiw': 1, 'hhan': 1, 'jiangx': 1, 'sganamur': 1}}
    db.SetupAllUsers(ALL_USER)
    resp=Draw16in1Picture(data, db.user_id_map)
    return HttpResponse(json.dumps(resp), content_type="application/json")