# coding: utf-8
__author__ = 'ccheng'

from flask import Flask, request, session, g, redirect, url_for, Blueprint, jsonify
from flask import abort, render_template, flash
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import LoginForm, RegisterForm ,CommentsForm ,MessageForm
from DoctorSpring import lm
from database import  db_session
from sqlalchemy.exc import IntegrityError
from DoctorSpring.models import User,Patent,Doctor,Diagnose
from DoctorSpring.models import User,DiagnoseComment,Message
from DoctorSpring.util import result_status as rs,object2dict
from DoctorSpring.util.constant import MessageUserType
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

    diagnoseCount=Diagnose.getDiagnoseCountByDoctorId(doctorId)
    resultDate['diagnoseCount']=diagnoseCount

    resultDate['doctor']=doctor
    diagnoses=Diagnose.getDiagnosesByDoctorId(doctorId)
    diagnoseDict=dataChangeService.userCenterDiagnoses(diagnoses)
    resultDate['diagnoses']=diagnoseDict
    return render_template("doctorHome.html",data=resultDate)
