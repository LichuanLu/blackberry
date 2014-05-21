# coding: utf-8
__author__ = 'chengc017'
import sqlalchemy as sa
from datetime import datetime
from DoctorSpring.util import constant
from database import db_session as session
from DoctorSpring.util.constant import ModelStatus

from database import Base
class Comment(Base):
    __tablename__ = 'commend'
    __table_args__ = {
        'mysql_charset': 'utf8',
    }
    id= sa.Column(sa.BigInteger, primary_key = True, autoincrement = True)
    observer=sa.Column(sa.Integer)
    receiver=sa.Column(sa.Integer )
    title=sa.Column(sa.String(256))
    content=sa.Column(sa.String(51200))
    createTime=sa.Column(sa.DateTime)
    type=sa.Column(sa.Integer)
    status=sa.Column(sa.Integer)
    parent_commend_id=sa.Column(sa.BigInteger)
class DiagnoseComment(Base):

    __tablename__ = 'diagnose_commend'
    __table_args__ = {
        'mysql_charset': 'utf8',
        }
    id= sa.Column(sa.BigInteger, primary_key = True, autoincrement = True)
    observer=sa.Column(sa.Integer)
    receiver=sa.Column(sa.Integer )
    observerType=sa.Column(sa.SmallInteger)
    receiverType=sa.Column(sa.SmallInteger)
    title=sa.Column(sa.String(256))
    content=sa.Column(sa.String(51200))
    createTime=sa.Column(sa.DateTime)
    type=sa.Column(sa.Integer)
    status=sa.Column(sa.Integer)
    parent_commend_id=sa.Column(sa.BigInteger)

    diagnoseId=sa.Column(sa.BigInteger)
    def __init__(self,observer,receiver,diagnoseId,content):
        self.observer=observer
        self.receiver=receiver
        #self.title=title
        self.diagnoseId=diagnoseId
        self.content=content
        self.createTime=datetime.now()
        self.status=constant.ModelStatus.Normal
        self.type=constant.CommentType.DiagnoseComment
    @classmethod
    def getCommentByUser(cls,observerId,status=ModelStatus.Normal):
        return session.query(DiagnoseComment).filter(DiagnoseComment.observer == observerId,DiagnoseComment.status==status).all()
    @classmethod
    def getCommentByReceiver(cls,receiverId,status=ModelStatus.Normal):
        return session.query(DiagnoseComment).filter(DiagnoseComment.receiver==receiverId,DiagnoseComment.status==status).all()
    @classmethod
    def getCommentBydiagnose(cls,diagnoseId,status=ModelStatus.Normal):
        return session.query(DiagnoseComment).filter(DiagnoseComment.diagnoseId==diagnoseId,DiagnoseComment.status==status).all()

