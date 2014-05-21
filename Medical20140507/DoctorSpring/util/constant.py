# coding: utf-8
__author__ = 'chengc017'
from datetime import  datetime
class ModelStatus(object):
      Normal=0
      Del=1
class MessageStatus(ModelStatus):
      Readed=2
class CommentType(object):
    DiagnoseComment=0
    Normal=1
class MessageType(object):
    pass
class MessageUserType(object):
    user=0
    hospitalUser=1
    patient=2
    doctor=3
class SystemTimeLimiter(object):
    startTime=datetime(2014,5,20)
    endTime=datetime(3014,5,20)
class Pagger(object):
    pageNo=1
    pageSize=20
    count=0
    def __init__(self,pageNo,pageSize):
        self.pageNo=pageNo
        self.pageSize=pageSize
        #self.count=count
    def getOffset(self):
        offset=(self.pageNo-1)*self.pageSize
        if offset<=self.count:
            return offset
    def getLimitCount(self):
        offset=(self.pageNo-1)*self.pageSize
        if offset+self.pageSize<=self.count:
            return self.pageSize
        else:
            return self.count-offset




