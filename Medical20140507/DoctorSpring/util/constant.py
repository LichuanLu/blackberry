# coding: utf-8
__author__ = 'chengc017'
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


