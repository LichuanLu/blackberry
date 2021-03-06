# coding: utf-8

__author__ = 'chengc017'
import os
import unittest
from DoctorSpring.models.comment import Comment
from DoctorSpring.models.doctor import Doctor
from DoctorSpring.models.user import User
from DoctorSpring.models.patent import Patent
from DoctorSpring.models.pathology import *
from DoctorSpring.models.diagnoseDocument import *
from database import db_session as session
from datetime import  datetime
from DoctorSpring.util.constant import Pagger



import tempfile

class CommentTestCase(unittest.TestCase):

    def test_addcomment(self):
        diagnoseComment=Comment(1,1,1,"诊断很不错，非常感谢")
        session.add(diagnoseComment)
        session.commit()

class DiagnoseTemplateTestCase(unittest.TestCase):

    def test_addcomment(self):
        diagnoseTemplate=DiagnoseTemplate()
        diagnoseTemplate.diagnoseMethod='x线'
        diagnoseTemplate.diagnosePosition='骨关节病变'
        diagnoseTemplate.diagnoseDesc='心肺骨未见异常'
        diagnoseTemplate.imageDesc='左尺桡骨形态，骨密度正常，未见明确骨质增生及破坏，左尺桡骨形态，骨密度正常，未见明确骨质增生及破坏，左尺桡骨形态，骨密度正常，未见明确骨质增生及破坏'
        session.add(diagnoseTemplate)
        session.commit()
    def test_getDiagnosePostion(self):
        diagnoseTemplates=DiagnoseTemplate.getDiagnosePostion('x线')
        print diagnoseTemplates

class UserTestCase(unittest.TestCase):
    def test_addUser(self):
        source='ccheng'
        from DoctorSpring.util.hash_method import getHashPasswd
        passwd=getHashPasswd(source)
        user=User('ccheng',passwd)
        user.sex=0
        user.status=0
        user.email='ccheng2281@126.com'
        user.address='四川省 通江县'
        user.imagePath='http://localhost:5000/static/assets/image/young-m.png'
        User.save(user)
    def test_addPatient(self):
        patient=Patent()
        patient.gender=0
        patient.Name='程成'
        patient.status=0
        patient.userID=1
        Patent.save(patient)

class DoctorTestCase(unittest.TestCase):
    def test_getDoctorById(self):
        doctor=Doctor.getById(1)
        print doctor.name

class DiagnoseTestCase(unittest.TestCase):
    def test_addPosition(self):
        postion=Position()
        postion.name="颈部"
        postion.status=0
        Position.save(postion)

    def test_addPathology(self):
        pathology=Pathology()

        #pathology.diagnoseDocId=1

        #pathology.docmFileId=1
        pathology.hospticalId=1
        pathology.caseHistory="没有病史"
        pathology.status=0
        Pathology.save(pathology)
    def test_addPathologyPostion(self):
        pathologyPostion=PathologyPostion()
        pathologyPostion.pathologyId=1
        pathologyPostion.positionId=2
        PathologyPostion.save(pathologyPostion)

    def test_getPathology(self):
        pathology=Pathology.getById(1)
        from DoctorSpring.util.object2dict import to_json
        pathologyDict=to_json(pathology,pathology.__class__)
        print pathology.id
    def test_addDiagnose(self):
        diagnose=Diagnose()
        diagnose.pathologyId=1
        diagnose.adminId=1

        diagnose.createDate=datetime.now()
        diagnose.doctorId=1
        diagnose.patientId=2
        diagnose.reportId=2
        diagnose.hospitalId=1
        diagnose.status=0
        Diagnose.save(diagnose)
    def test_getDiagnose(self):
        pager=Pagger(1,20)
        diagnoses=Diagnose.getDiagnosesByDoctorId(1,pager,None)
        print len(diagnoses)
    def test_getPatientListByDoctorId(self):
        patients=Diagnose.getPatientListByDoctorId(1)
        print len(patients)










