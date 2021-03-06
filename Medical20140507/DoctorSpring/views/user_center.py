# coding: utf-8
__author__ = 'ccheng'

from flask import Flask, request, session, g, redirect, url_for, Blueprint, jsonify
from flask import abort, render_template, flash
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import LoginForm, RegisterForm ,CommentsForm ,MessageForm,UserFavortiesForm
from DoctorSpring import lm
from database import  db_session
from sqlalchemy.exc import IntegrityError
from DoctorSpring.models import User,Patent,Doctor,Diagnose ,DiagnoseTemplate
from DoctorSpring.models import User,Comment,Message,UserFavorites
from DoctorSpring.util import result_status as rs,object2dict
from DoctorSpring.util.constant import MessageUserType,Pagger

import  data_change_service as dataChangeService
import json

import config
config = config.rec()

uc = Blueprint('user_center', __name__)


@uc.route('/doctor/<int:doctorId>/home',  methods = ['GET', 'POST'])
def endterDoctorHome(doctorId):

    doctor=Doctor.getById(doctorId)
    if doctor is None:
        return redirect(url_for('/300'))

    resultDate={}
    messageCount=Message.getMessageCountByReceiver(doctorId)
    resultDate['messageCount']=messageCount

    diagnoseCount=Diagnose.getNewDiagnoseCountByDoctorId(doctorId)
    resultDate['diagnoseCount']=diagnoseCount

    resultDate['doctor']=doctor
    pager=Pagger(1,20)
    diagnoses=Diagnose.getDiagnosesByDoctorId(doctorId,pager)
    diagnoseDict=dataChangeService.userCenterDiagnoses(diagnoses)
    resultDate['diagnoses']=diagnoseDict
    return render_template("doctorHome.html",data=resultDate)

@uc.route('/doctor/<int:doctorId>/patientList',  methods = ['GET', 'POST'])
def getPatients(doctorId):
     patients=Diagnose.getPatientListByDoctorId(doctorId)
     patientsDict=object2dict.objects2dicts(patients)
     resultStatus=rs.ResultStatus(rs.SUCCESS.status,rs.SUCCESS.msg,patientsDict)
     resultDict=resultStatus.__dict__
     return json.dumps(resultDict,ensure_ascii=False)
@uc.route('/diagnoseTemplate/postionList',  methods = ['GET', 'POST'])
def getPostionList():
    diagnoseMethod=request.args.get('diagnoseMethod')
    diagnosePositions=DiagnoseTemplate.getDiagnosePostion(diagnoseMethod)
    resultStatus=rs.ResultStatus(rs.SUCCESS.status,rs.SUCCESS.msg,diagnosePositions)
    resultDict=resultStatus.__dict__
    return json.dumps(resultDict,ensure_ascii=False)
@uc.route('/diagnoseTemplate/diagnoseAndImageDesc',  methods = ['GET', 'POST'])
def getDiagnoseAndImageDescList():
    diagnoseMethod=request.args.get('diagnoseMethod')
    diagnosePostion=request.args.get('diagnosePostion')
    diagnoseAndImageDescs=DiagnoseTemplate.getDiagnoseAndImageDescs(diagnoseMethod,diagnosePostion)
    resultStatus=rs.ResultStatus(rs.SUCCESS.status,rs.SUCCESS.msg,diagnoseAndImageDescs)
    resultDict=resultStatus.__dict__
    return json.dumps(resultDict,ensure_ascii=False)

@uc.route('/userFavorties/add',  methods = ['GET', 'POST'])
def addUserFavorties():
    form =  UserFavortiesForm(request.form)
    formResult=form.validate()
    if formResult.status==rs.SUCCESS.status:
        #session['remember_me'] = form.remember_me.data
        # login and validate the user...
        userFavorites=UserFavorites(form.userId,form.type,form.doctorId,form.hospitalId,form.docId)
        UserFavorites.save(userFavorites)
        #flash('成功添加诊断评论')
        return json.dumps(formResult.__dict__,ensure_ascii=False)
    return json.dumps(formResult.__dict__,ensure_ascii=False)
@uc.route('/userFavorties/<int:id>/cancel',  methods = ['GET', 'POST'])
def cancleUserFavorties(id):
    UserFavorites.cancleFavorites(id)
    return json.dumps(rs.SUCCESS.__dict__,ensure_ascii=False)
@uc.route('/userFavorties/<int:id>/cancel',  methods = ['GET', 'POST'])
def getUserFavorties(id):
    type=request.args.get('type')
    userFavorites=UserFavorites.getUserFavorties(id,type)
    userFavoritesDict=object2dict.objects2dicts(userFavorites)
    resultStatus=rs.ResultStatus(rs.SUCCESS.status,rs.SUCCESS.msg,userFavoritesDict)
    return json.dumps(resultStatus.__dict__,ensure_ascii=False)
