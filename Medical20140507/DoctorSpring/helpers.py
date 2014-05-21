# coding: utf-8

import os
import re
from hashlib import md5
import time
import config

config = config.rec()


def getDay(timestamp):
	FORY = '%d'
	#os.environ["TZ"] = config.default_timezone
	#time.tzset()
	str = time.strftime(FORY, time.localtime(timestamp))
	return str


def getMonth(timestamp):
	FORY = '%b'
	#os.environ["TZ"] = config.default_timezone
	#time.tzset()
	str = time.strftime(FORY, time.localtime(timestamp))
	return str


def formatDate(timestamp):
	FORY = '%Y-%m-%d @ %H:%M'
	FORM = '%m-%d @ %H:%M'
	FORH = '%H:%M'
	#os.environ["TZ"] = config.default_timezone
	#time.tzset()
	rtime = time.strftime(FORM, time.localtime(timestamp))
	htime = time.strftime(FORH, time.localtime(timestamp))
	now = int(time.time())
	t = now - timestamp
	if t < 60:
		str = '刚刚'
	elif t < 60 * 60:
		min = t / 60
		str = '%d 分钟前' % min
	elif t < 60 * 60 * 24:
		h = t / (60 * 60)
		str = '%d 小时前 %s' % (h,htime)
	elif t < 60 * 60 * 24 * 3:
		d = t / (60 * 60 * 24)
		if d == 1:
			str = '昨天 ' + rtime
		else:
			str = '前天 ' + rtime
	else:
		str = time.strftime(FORY, time.localtime(timestamp))
	return str


def formatDate2(timestamp):
	FORY = '%Y-%m-%d @ %H:%M'
	#os.environ["TZ"] = config.default_timezone
	#time.tzset()
	str = time.strftime(FORY, time.localtime(timestamp))
	return str


def getAvatar(email, size=48):
    return \
            'http://gravatar.com/avatar/%s?d=identicon&s=%d&d=http://feather.im/static/img/gravatar.png' \
% (md5(email.strip().lower().encode('utf-8')).hexdigest(), size)

