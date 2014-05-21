# coding: utf-8
__author__ = 'Jeremy'

import sqlalchemy as sa
from  sqlalchemy import distinct

from database import Base
from sqlalchemy.orm import  relationship,backref


# class Post(Base):
#     __tablename__ = 'diagnose'
#     __table_args__ = {
#         'mysql_charset': 'utf8',
#         }
#
#     id = sa.Column(sa.Integer, primary_key = True, autoincrement = True)
#     userId  = sa.Column(sa.Integer)
#     pathologyId = sa.Column(sa.INTEGER)  #病理信息表ID
#     patientId = sa.Column(sa.INTEGER)    #病人表ID
#     createDate = sa.Column(sa.DATETIME)
#     reviewDate = sa.Column(sa.DATETIME)
#     adminId = sa.Column(sa.INTEGER)     #审查adminID
#     reportId = sa.Column(sa.INTEGER)    #生成reportID
#     hospitalId = sa.Column(sa.INTEGER)  #医院ID，用于医院批量提交诊断信息
#     status = sa.Column(sa.INTEGER)      #标记状态 未提交，待审查，待诊断，待审核，结束
# coding: utf-8
__author__ = 'chengc017'

import sqlalchemy as sa
from DoctorSpring.util.constant import ModelStatus
from datetime import datetime
from database import Base,db_session as session
from sqlalchemy.orm import relationship,backref

class Diagnose(Base):
    __tablename__ = 'diagnose'
    __table_args__ = {
        'mysql_charset': 'utf8',
        }

    id = sa.Column(sa.Integer, primary_key = True, autoincrement = True)
    patientId  = sa.Column(sa.Integer,sa.ForeignKey('patent.id'))
    patient = relationship("Patent", backref=backref('diagnose', order_by=id))

    doctorId  = sa.Column(sa.Integer,sa.ForeignKey('doctor.id'))
    doctor = relationship("Doctor", backref=backref('diagnose', order_by=id))

    adminId = sa.Column(sa.INTEGER)

    uploadUserId  = sa.Column(sa.Integer,sa.ForeignKey('User.id'))
    uploadUser = relationship("User", backref=backref('diagnose', order_by=id))

    pathologyId  = sa.Column(sa.Integer,sa.ForeignKey('pathology.id'))
    pathology = relationship("Pathology", backref=backref('diagnose', order_by=id))

    reportId = sa.Column(sa.Integer)

    createDate=sa.Column(sa.DateTime)
    reviewDate = sa.Column(sa.DATETIME)

    hospitalId = sa.Column(sa.INTEGER)  #医院ID，用于医院批量提交诊断信息
    status = sa.Column(sa.INTEGER)

    @classmethod
    def save(cls,diagnose):
        if diagnose:
            session.add(diagnose)
            session.commit()
            session.flush()
    @classmethod
    def getDiagnosesByDoctorId(cls,doctorId,status=None):
        if doctorId:
            if status:
                return session.query(Diagnose).filter(Diagnose.doctorId==doctorId,Diagnose.status==status).all()
            else:
                return session.query(Diagnose).filter(Diagnose.doctorId==doctorId,Diagnose.status!=ModelStatus.Del).all()
    @classmethod
    def getDiagnoseCountByDoctorId(cls,doctorId):
        if doctorId:
            return session.query(Diagnose).filter(Diagnose.doctorId==doctorId,Diagnose.status==ModelStatus.Normal).count()
    @classmethod
    def getPatientListByDoctorId(cls,doctorId):
        if doctorId:
            return session.query(Diagnose).filter(Diagnose.doctorId==doctorId,Diagnose.status==ModelStatus.Normal).group_by(Diagnose.patientId).all()




'''
    def __init__(self, title=title, content=content, origin_content=None,
                 created_date=None, update_date=None):
        self.title = title
        self.content = content
        self.update_date = update_date
        if created_date == None:
            self.created_date = time.time()
        else:
            self.created_date = created_date
        if origin_content == None:
            self.origin_content = content
        else:
            self.origin_content = origin_content


    def __repr__(self):
        return '<Post %s>' % (self.title)
'''