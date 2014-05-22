# coding: utf-8
__author__ = 'ccheng'

from flask import Flask, request, session, g, redirect, url_for, Blueprint, jsonify
from flask import abort, render_template, flash
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import LoginForm, RegisterForm ,CommentsForm ,MessageForm
from DoctorSpring import lm
from database import  db_session
from sqlalchemy.exc import IntegrityError
from DoctorSpring.models import User,Patent
from DoctorSpring.models import User,Comment,Message
from DoctorSpring.util import result_status as rs,object2dict
import json

import config
config = config.rec()

mc = Blueprint('message_comment', __name__)


# @app.before_request
# def before_request():
#     g.user = current_user
@mc.route('/addDiagnoseComment.json', methods = ['GET', 'POST'])
def addDiagnoseComment():
    form = CommentsForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        #session['remember_me'] = form.remember_me.data
        # login and validate the user...
        diagnoseComment=Comment(form.userId.data,form.receiverId.data,form.diagnoseId.data,form.content.data)
        db_session.add(diagnoseComment)
        db_session.commit()
        db_session.flush()
        #flash('成功添加诊断评论')
        return jsonify(rs.SUCCESS.__dict__)
    return jsonify(rs.FAILURE.__dict__)
@mc.route('/observer/<int:userId>/diagnoseCommentList.json', methods = ['GET', 'POST'])
def diagnoseCommentsByObserver(userId):

    diagnoseComments=Comment.getCommentByUser(userId)
    if diagnoseComments is None or len(diagnoseComments)<1:
        return jsonify(rs.SUCCESS.__dict__)
    diagnoseCommentsDict=object2dict.objects2dicts(diagnoseComments)
    resultStatus=rs.ResultStatus(rs.SUCCESS.status,rs.SUCCESS.msg,diagnoseCommentsDict)
    resultDict=resultStatus.__dict__
    return jsonify(resultDict)
@mc.route('/receiver/<int:receiverId>/diagnoseCommentList.json', methods = ['GET', 'POST'])
def diagnoseCommentsByReceiver(receiverId):

    diagnoseComments=Comment.getCommentByReceiver(receiverId)
    if diagnoseComments is None or len(diagnoseComments)<1:
        return jsonify(rs.SUCCESS.__dict__)
    diagnoseCommentsDict=object2dict.objects2dicts(diagnoseComments)
    resultStatus=rs.ResultStatus(rs.SUCCESS.status,rs.SUCCESS.msg,diagnoseCommentsDict)
    resultDict=resultStatus.__dict__
    return jsonify(resultDict)

@mc.route('/diagnose/<int:diagnoseId>/diagnoseCommentList.json', methods = ['GET', 'POST'])
def diagnoseCommentsByDiagnose(diagnoseId):

    diagnoseComments=Comment.getCommentBydiagnose(diagnoseId)
    if diagnoseComments is None or len(diagnoseComments)<1:
        return jsonify(rs.SUCCESS.__dict__)
    diagnoseCommentsDict=object2dict.objects2dicts(diagnoseComments)
    resultStatus=rs.ResultStatus(rs.SUCCESS.status,rs.SUCCESS.msg,diagnoseCommentsDict)
    resultDict=resultStatus.__dict__
    return jsonify(resultDict)

@mc.route('/message/add', methods = ['GET', 'POST'])
def addMessage():
    form = MessageForm(request.form, csrf_enabled=False)
    if form.validate():
        #session['remember_me'] = form.remember_me.data
        # login and validate the user...
        message=Message(form.senderId.data,form.receiverId.data,form.title.data,form.content.data,form.type.data)
        Message.save(message)
        #flash('成功添加诊断评论')
        return redirect(url_for('homepage'))
    return render_template('message.html', form=form)

@mc.route('/receiver/<int:receiverId>/messageList.json', methods = ['GET', 'POST'])
def messagesByReceiver(receiverId):

    status=request.args.get('status')

    messages=None
    if status:
        messages=Message.getMessageByReceiver(receiverId,status)
    else:
        messages=Message.getMessageByReceiver(receiverId)
    if messages is None or len(messages)<1:
        return jsonify(rs.SUCCESS.__dict__)
    messagesDict=object2dict.objects2dicts(messages)
    resultStatus=rs.ResultStatus(rs.SUCCESS.status,rs.SUCCESS.msg,messagesDict)
    resultDict=resultStatus.__dict__
    return jsonify(resultDict)


@mc.route('/sender/<int:senderId>/messageList.json', methods = ['GET', 'POST'])
def messagesBySender(senderId):
    status=request.args.get('status')

    messages=None
    if status:
        messages=Message.getMessageByReceiver(senderId,status)
    else:
        messages=Message.getMessageByReceiver(senderId)
    if messages is None or len(messages)<1:
        return jsonify(rs.SUCCESS.__dict__)
    messagesDict=object2dict.objects2dicts(messages)
    resultStatus=rs.ResultStatus(rs.SUCCESS.status,rs.SUCCESS.msg,messagesDict)
    resultDict=resultStatus.__dict__
    return jsonify(resultDict)

@mc.route('/message/<int:messageId>/remark.json', methods = ['GET', 'POST'])
def remarkMessage(messageId):
    status=request.args.get('status')
    result=None
    if status:
        result=Message.remarkMessage(messageId,status)
    else:
        result=Message.remarkMessage(Message)
    resultStatus=rs.ResultStatus(rs.SUCCESS.status,rs.SUCCESS.msg,result)
    resultDict=resultStatus.__dict__
    return jsonify(resultDict)

