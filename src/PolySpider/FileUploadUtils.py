#!/usr/bin/env python
#coding:gbk

import urllib2
import urllib
import hashlib
import datetime
import md5
import os
from progressbar import *
from PolySpider import Config

__version__ = '2.1.1'


class Progress(object):
	def __init__(self):
		self._seen = 0.0

	def update(self, pbar, total, size, name):
		if self._seen == 0.0: 
			pbar.start()
			pbar.maxval = total
		self._seen += size
		pbar.update(min(self._seen, total))

class file_with_callback(file):
	def __init__(self, pbar, path, mode, callback, *args):
		file.__init__(self, path, mode)
		self.seek(0, os.SEEK_END)
		self._total = self.tell()
		self.seek(0)
		self._callback = callback
		self._args = args
		self._pbar = pbar

	def __len__(self):
		return self._total

	def read(self, size):
		data = file.read(self, size)
		self._callback(self._pbar, self._total, len(data), *self._args)
		return data

def httpdate_rfc1123(dt):
	"""Return a string representation of a date according to RFC 1123
	(HTTP/1.1).

	The supplied date must be in UTC.

	"""
	weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][dt.weekday()]
	month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
			 "Oct", "Nov", "Dec"][dt.month - 1]
	return "%s, %02d %s %04d %02d:%02d:%02d GMT" % \
		(weekday, dt.day, month, dt.year, dt.hour, dt.minute, dt.second)

class UpYunServiceException(Exception):
	def __init__(self, status, msg, err):
		self.args = (status, msg, err)
		self.status = status
		self.msg = msg
		self.err = err

class UpYunClientException(Exception):
	def __init__(self, msg):
		self.args = (msg)
		self.msg = msg

class UpYun():

        # ���� `bucket` Ϊ�ռ�����,`username` �� `password` �ֱ�Ϊ��Ȩ����Ա�ʺź����룬��ѡ��
        # ���� `timeout` Ϊ HTTP ����ʱʱ�䣬Ĭ�� 60 �룬��ѡ��
        # ���ݹ��ڵ���������������ƴ洢 API Ŀǰ�ṩ�˵��š���ͨ��ͨ���ƶ���ͨ��������㣬
        # �ڳ�ʼ��ʱ���ɲ��� `endpoint` �������ã����ѡ��ֵ�У�
        # v0.api.upyun.com     �������������Զ�ѡ�����㣬Ĭ��
        # v1.api.upyun.com      ���Ž����
        # v2.api.upyun.com      ��ͨ��ͨ�����
        # v3.api.upyun.com      �ƶ���ͨ�����
	def __init__(self):
		self.bucket = Config.UPYUN_BUCKET
		self.username = Config.UPYUN_USERNAME
		self.password = hashlib.md5(Config.UPYUN_PASSWORD).hexdigest()
		self.timeout = 30
		self.endpoint = "v0.api.upyun.com"
		self.user_agent = None


	def put(self, key, filePath, checksum = False):
		file = open(filePath, 'r')
		fileMd5 = md5.new(file.read()).digest()
		file.close()
		
		uri = '/' + self.bucket + (lambda x: x[0] == '/' and x or '/'+x)(key)
		if isinstance(uri, unicode): uri = uri.encode('utf-8')
		uri = urllib.quote(uri, safe="~/")
		method = 'PUT'

		length = os.path.getsize(filePath)

		dt = httpdate_rfc1123(datetime.datetime.utcnow())

		signature = self.__make_signature(method, uri, dt, length)

		userAgent= self.user_agent if self.user_agent else "upyun-python-sdk/" + __version__
		
		url = "http://" + self.endpoint + uri

		widgets = [' <<<', Bar(), '>>> ',Percentage(),' ', ETA() ,' ' ,  FileTransferSpeed()]
		pbar = ProgressBar(widgets=widgets)

		progress = Progress()
		stream = file_with_callback(pbar,filePath, 'rb', progress.update, filePath)
		req = urllib2.Request(url, stream)
		req.add_header('Mkdir', 'true')
		req.add_header('Content-MD5', fileMd5)
		req.add_header('Date', dt)
		req.add_header('Content-Length', length)
		req.add_header('Authorization', signature)
		req.add_header('User-Agent', userAgent)
		req.get_method = lambda: 'PUT'

		try:

			response = urllib2.urlopen(req, timeout=self.timeout)
		except urllib2.HTTPError as e:
			print e.code
			print e.read()
		print "Upload Success"

	def __make_signature(self, method, uri, date, length):
		signstr = '&'.join([method, uri, date, str(length), self.password])
		signature = hashlib.md5(signstr).hexdigest()
		return 'UpYun ' + self.username + ':' + signature