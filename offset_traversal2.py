import os
from sys import argv
import threading
from signal import signal
from os import path
from configobj import ConfigObj
import logging  as log
from time import sleep


class CSTracertPrepare(object): # prepare configs
    def __init__(self, config_file):
        if path.exists(config_file):
                CONFIG = ConfigObj(config_file)

class STAT:
	def __init__(self,cl):
		self.cl = cl
		_file = path.join('~','.cloudsearch_upload_tracert')
		_file = path.expanduser(_file) # ~/.cloudsearch_upload_tracert directory
		if not path.exists(_file) or not path.isdir(_file):
			log.critical('.cloudsearch_upload_tracert path does not exist')
		_file = path.join(_file, "-".join(cl.fd.name.split(path.sep))) 
		log.debug('the tracking file name : ' + _file)
		self.fd = 0
		self.eof = -1
		self.pos = -1
		self.inode = -1
		self.UNTRACKED = 0
		self.ACCOMPLISHED = 1
		self.INPROGRESS = 2
		self.status = self.UNTRACKED
		self.fd = open(_file, 'rw+')   #os.O_CREAT|os.O_RDWR|os.O_TRUNC)
		_data = self.fd.read()
		print("Data is")
		print(_data)
		print("Eval cond")
		print(filter(lambda i : i , map(lambda s : s.isdigit(), _data.split(','))))
		print(len(filter(lambda i : i , map(lambda s : s.isdigit(), _data.split(',') ))) )
		if len(_data) != 0 and _data.find(',') != -1 and len(filter(lambda i : i , map(lambda s : s.isdigit(), _data.split(',') ))) == 2 :
		    self.pos ,self.eof ,self.inode = map(int, _data.split(','))
		else :
			log.error('bad content of tracking file %s', self.fd.name)
			log.error('re-create it .')
			self.fd.write("{},{},{}".format(0,0,0))
			self.fd.flush()
		del(_data)
		if os.stat(cl.fd.name).st_ino != int(self.inode) :
		    self.status == self.UNTRACKED
		    return
		if os.stat(cl.fd).ST_INO == int(self.inode) and self.eof == cl.eof:
		    self.status == self.ACCOMPLISHED
		    return
		if os.stat(cl.fd).ST_INO == int(self.inode) and self.eof != cl.eof:
		    self.status == self.INPROGRESS
		    return
	def sync(self):
		self.fd.seek(0)
		self.fd.write("{},{},{}".format(self.cl.pos, self.cl._eof, os.stat(self.cl.fd.name).st_ino))
	def __del__(self) :
	    self.fd.close()


class FILE_TRACERT : #T.D : portability to MS windows OS
	def __init__(self, _file, relaunch=False, follow=True):
		self.follow = follow
		self.relaunch = relaunch
		self.fd = open(_file, 'r')
		self._pos = -1
		self._eof = -1
		self.stat = STAT(self)
		if self.relaunch or self.stat.status == self.stat.UNTRACKED:
		    self.pos = 0
		    self.stat.sync()
		# ACCOMPLISHED
		elif stat.status == stat.ACCOMPLISHED :
		    log.critical("This file have been processed successfully") # T.D : Add date of processing
		# INPROGRESS
		elif stat.status == stat.INPROGRESS :
		    self.pos = stat.pos
	@property
	def eof(self):
	    if self._eof == -1 or self.follow :
	        _cur_eof = self.get_eof()
	        if self._eof < _cur_eof :
	            self.stat.sync()
	        self._eof = _cur_eof
	        return _cur_eof
	    elif not self.follow :
	        return self._eof
	@eof.setter
	def eof(self, val):
	    self._eof = val
	@property
	def pos(self):
	    self.fd.tell()
	    self.stat.sync()
	@pos.setter
	def pos(self, offset):
	    self.fd.seek(offset, 0)
	    self.stat.sync()
	def get_eof(self) :
			cur = self.fd.tell()
			self.fd.seek(0,2)
			self._eof = self.fd.tell()
			self.fd.seek(cur,0)
			return self._eof
	def __del__(self) :
            self.fd.close()

# while .. .. . ..
def cs_upload(fake_arg):
	log.info("uploading file " + fake_arg)
	sleep(2)

def main(_file, relaunch=False, follow=False, disc=None):
	if disc == None :
		count = 0
		log.debug("inside main loop")
		alog = FILE_TRACERT(_file)
		log.debug("alog.eof = " + str(alog.eof) )
		log.debug("after alog start")
		with open('.cd_uploader.part', 'w+') as out_fd :
		    while alog.pos <= alog.eof and count < 100 :
		        data = alog.fd.readline()
		        out_fd.write(data)
		        count = count + 1
		cs_upload('.cd_uploader.part')
		if alog.pos == alog.eof :
		    print("Done. ")
		    return
		alog.stat.sync()
		main(_file, relaunch, follow, disc)

def cmd_exec(args):
	""" $argv[0] [ [-f|--follow]|[--relaunch] ] filename \n while filename is the log file to trace """
	_file = args[1]
	main(_file)


if __name__ == "__main__" :
    cmd_exec(argv)

