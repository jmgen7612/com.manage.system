#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file   :views.py
# @time   :2020/3/3011:26
# @Author :jmgen
# @Version:1.0
# @Desc   :
import xlrd
from sqlalchemy import or_
from flask import request, jsonify
from . import case
from .. import db
from ..models import Caseinfo
from ..models import Project
from ..models import CaseVersion
from ..models import TestResult
from ..models import CaseResult
from ..models import TestPlan

@case.route("/uploadcase", methods=['POST'])
def uploadcase():
    datafile = request.files['file']
    namelist = request.form['name'].split('_')
    caseversion_name = namelist[1]
    project_name = namelist[2].split('.')[0]
    # 获取文件内容
    f = datafile.read()
    # 指定文件内容
    workbook = xlrd.open_workbook(file_contents=f)
    Data_sheet = workbook.sheets()[0]
    rowNum = Data_sheet.nrows  # sheet行数
    row_data0 = Data_sheet.row_values(0)
    row_list = []
    # 校验上传的excel文件名称是否符合规范
    if (caseversion_name is not None and project_name is not None):
        name = Project.query.filter_by(name=project_name).first()
        project = Project(name=project_name)
        # 如果项目名称不存在，则添加新的项目
        if (name is None):
            db.session.add(project)
            db.session.commit()
            version = CaseVersion.query.filter_by(name=caseversion_name, project_id=project.id).first()
            # 如果版本号不存在，则添加新的版本号
            if (version is None):
                caseversion = CaseVersion(name=caseversion_name, project_id=project.id)
                db.session.add(caseversion)
                db.session.commit()
        # 项目名称存在，则检测该项目下版本号是否存在
        else:
            version = CaseVersion.query.filter_by(name=caseversion_name, project_id=name.id).first()
            if (version is None):
                caseversion = CaseVersion(name=caseversion_name, project_id=name.id)
                db.session.add(caseversion)
                db.session.commit()

        # 校验上传的excel文件格式是否符合规范
        if (row_data0[0] == "用例编号" and row_data0[1] == "主模块" and row_data0[2] == "子模块" and row_data0[3] == "级别" and
                row_data0[4] == "标题" and row_data0[5] == "前提条件" and row_data0[6] == "测试步骤" and row_data0[
                    7] == "预期结果" and
                row_data0[8] == "备注"):
            for i in range(1, rowNum):
                row_data = Data_sheet.row_values(i)
                row_list.append(row_data)
                n = i - 1
                caseinfo = Caseinfo(caseid=row_list[n][0],
                                    model=row_list[n][1],
                                    submodel=row_list[n][2],
                                    level=row_list[n][3],
                                    title=row_list[n][4],
                                    preconditions=row_list[n][5],
                                    step=row_list[n][6],
                                    expectresult=row_list[n][7],
                                    remark=row_list[n][8],
                                    )
                name = Project.query.filter_by(name=project_name).first()
                version = CaseVersion.query.filter_by(name=caseversion_name, project_id=name.id).first()
                # 添加用例和项目的关系
                caseinfo.project_id = [name]
                # 添加用例和版本的关系
                caseinfo.caseversion_id = [version]
                db.session.add(caseinfo)
                db.session.commit()
            return jsonify({'code': 200, 'msg': '文件上传成功'})
        else:
            return jsonify({'code': 40001, 'msg': '上传的文件不符合规范'})
    else:
        return jsonify({'code': 40002, 'msg': '上传的文件名不符合规范'})

@case.route("/excutecase", methods=['POST'])
def excutecase():
    projects = request.json.get('project')
    caseversions = request.json.get('caseversion')
    testplan = request.json.get('testplan')
    model = request.json.get('model')
    key = request.json.get('key')
    list = []
    if (len(projects)!=0 and len(caseversions)!=0 and len(testplan)!=0):
        # 通过project获取其id值
        project=projects[0]
        caseversion=caseversions[0]
        project_id = Project.query.filter_by(name=project).first().id
        case_info = CaseVersion.query.filter_by(name=caseversion, project_id=project_id).first().case_info
        testresult_id = TestPlan.query.filter_by(name=testplan,project_id=project_id,caseversion_id=caseversions[2]).first().testresult_id
        if (len(model)!=0):
            if (key !=''):
                caseinfo = Caseinfo.query.filter(or_(Caseinfo.caseid.like("%" + key + "%"),
                                                     Caseinfo.model.like("%" + key + "%"),
                                                     Caseinfo.submodel.like("%" + key + "%"),
                                                     Caseinfo.title.like("%" + key + "%"),
                                                     Caseinfo.preconditions.like("%" + key + "%"),
                                                     Caseinfo.step.like("%" + key + "%"),
                                                     Caseinfo.expectresult.like("%" + key + "%"),
                                                     Caseinfo.remark.like("%" + key + "%"),
                                                     )).all()
                #取key值匹配结果的用例和项目和版本匹配结果的用例的交集
                cases=set(caseinfo).intersection(set(case_info))
                for case in cases:
                    if (model == case.model):
                        case_result = CaseResult.query.filter_by(caseid=case.id, testresult_id=testresult_id).first()
                        if (case_result is not None):
                            casedata = dict(case.case_dic(), **case_result.caseresult_dic())
                            list.append(casedata)
                        else:
                            list.append(case.case_dic())
                return jsonify(
                    {'code': 200, 'tableData': list, 'msg': '用例查询完成'})
            else:
                for case in case_info:
                    if(model == case.model):
                        case_result = CaseResult.query.filter_by(caseid=case.id, testresult_id=testresult_id).first()
                        if (case_result is not None):
                            casedata = dict(case.case_dic(), **case_result.caseresult_dic())
                            list.append(casedata)
                        else:
                            list.append(case.case_dic())
                return jsonify(
                    {'code': 200, 'tableData': list, 'msg': '用例查询完成'})
        else:
            if(key !=''):
                caseinfo = Caseinfo.query.filter(or_(Caseinfo.caseid.like("%" + key + "%"),
                                                     Caseinfo.model.like("%" + key + "%"),
                                                     Caseinfo.submodel.like("%" + key + "%"),
                                                     Caseinfo.title.like("%" + key + "%"),
                                                     Caseinfo.preconditions.like("%" + key + "%"),
                                                     Caseinfo.step.like("%" + key + "%"),
                                                     Caseinfo.expectresult.like("%" + key + "%"),
                                                     Caseinfo.remark.like("%" + key + "%"),
                                                     )).all()
                # 取key值匹配结果的用例和项目和版本匹配结果的用例的交集
                cases = set(caseinfo).intersection(set(case_info))
                for case in cases:
                    case_result = CaseResult.query.filter_by(caseid=case.id, testresult_id=testresult_id).first()
                    if (case_result is not None):
                        casedata = dict(case.case_dic(), **case_result.caseresult_dic())
                        list.append(casedata)
                    else:
                        list.append(case.case_dic())
                return jsonify(
                    {'code': 200, 'tableData': list, 'msg': '用例查询完成'})
            else:
                for case in case_info:
                    case_result = CaseResult.query.filter_by(caseid=case.id, testresult_id=testresult_id).first()
                    if (case_result is not None):
                        casedata = dict(case.case_dic(), **case_result.caseresult_dic())
                        list.append(casedata)
                    else:
                        list.append(case.case_dic())
                return jsonify(
                    {'code': 200, 'tableData': list, 'msg': '用例查询完成'})
    else:
        return jsonify(
            {'code': 40001, 'msg': '请选择项目、版本和测试计划'})

@case.route("/datainfo", methods=['GET'])
def datainfo():
    #返回项目名称和项目id
    project = Project.query.with_entities(Project.name, Project.id).all()
    #返回用例版本名称、id和对应的项目id
    caseversion = CaseVersion.query.with_entities(CaseVersion.name, CaseVersion.project_id,CaseVersion.id).all()
    # 返回测试计划名称和对应的用例版本id
    testplan = TestPlan.query.with_entities(TestPlan.name, TestPlan.project_id,TestPlan.caseversion_id).all()
    models=[]
    if(caseversion is not None and project is not None):
        for projec in project:
            for version in caseversion:
                case_version = CaseVersion.query.filter_by(name=version[0], project_id=projec[1]).first()
                if(case_version is not None):
                    case_info=case_version.case_info
                    for case in case_info:
                        model=[case.model,projec[1],case_version.id]
                        if model not in models:
                            models.append(model)
    return jsonify(
        {'code': 200, 'projects': project, 'caseversions': caseversion, 'testplans': testplan, 'models': models,
         'msg': '获取数据成功'})

@case.route("/createplan", methods=['POST'])
def createplan():
    name = request.json.get('plan')
    project = request.json.get('project')[0]
    caseversion = request.json.get('caseversion')[0]
    result_name=project+"_"+caseversion+"_"+name+'_结果统计'
    # name ='合版测试'
    # project = "服务端"
    # caseversion = "1.0.2"
    project_id = Project.query.filter_by(name=project).first().id
    version = CaseVersion.query.filter_by(name=caseversion,project_id=project_id).first()
    testresult=TestResult(name=result_name,resultpass=0,resultfail=0,resultblock=0,resultnotest=0,runcase=0,totalcase=0)
    db.session.add(testresult)
    db.session.commit()
    testresult_id= TestResult.query.filter_by(name=result_name).first().id
    testplan = TestPlan(name=name, project_id=project_id,
                        caseversion_id=version.id,testresult_id=testresult_id)
    plan = TestPlan.query.filter_by(name=name,project_id=project_id,
                        caseversion_id=version.id,testresult_id=testresult_id).first()
    if(plan is None):
        db.session.add(testplan)
        db.session.commit()
        return jsonify({'code': 200, 'msg': "测试计划创建成功"})
    else:
        return jsonify({'code': 40001, 'msg': "测试计划创建失败"})

@case.route("/upresult", methods=['POST'])
def upresult():
    project = request.json.get('project')[0]
    caseversion = request.json.get('caseversion')[0]
    testplan = request.json.get('testplan')
    model = request.json.get('model')
    key = request.json.get('key')
    caseid = request.json.get('caseid')
    casemodel = request.json.get('casemodel')
    result = request.json.get('result')
    tester = request.json.get('tester')
    testtime = request.json.get('testtime')
    project_id = Project.query.filter_by(name=project).first().id
    case_info = CaseVersion.query.filter_by(name=caseversion, project_id=project_id).first().case_info
    caseversion_id=CaseVersion.query.filter_by(name=caseversion,project_id=project_id).first().id
    testresult_id=TestPlan.query.filter_by(name=testplan,project_id=project_id,caseversion_id=caseversion_id).first().testresult_id
    caseresult=CaseResult(caseid=caseid,casemodel=casemodel,caseresult=result,tester=tester,testtime=testtime,testresult_id=testresult_id)
    case_result=CaseResult.query.filter_by(caseid=caseid,testresult_id=testresult_id).first()
    list = []
    if(case_result is None):
        db.session.add(caseresult)
        db.session.commit()
    else:
        case_result.caseresult=result
        case_result.tester=tester
        case_result.testtime=testtime
        db.session.commit()
    if (len(model)!=0):
        if (key != ''):
            caseinfo = Caseinfo.query.filter(or_(Caseinfo.caseid.like("%" + key + "%"),
                                                 Caseinfo.model.like("%" + key + "%"),
                                                 Caseinfo.submodel.like("%" + key + "%"),
                                                 Caseinfo.title.like("%" + key + "%"),
                                                 Caseinfo.preconditions.like("%" + key + "%"),
                                                 Caseinfo.step.like("%" + key + "%"),
                                                 Caseinfo.expectresult.like("%" + key + "%"),
                                                 Caseinfo.remark.like("%" + key + "%"),
                                                 )).all()
            # 取key值匹配结果的用例和项目和版本匹配结果的用例的交集
            cases = set(caseinfo).intersection(set(case_info))
            for case in cases:
                if (model == case.model):
                    case_result = CaseResult.query.filter_by(caseid=case.id, testresult_id=testresult_id).first()
                    if (case_result is not None):
                        casedata = dict(case.case_dic(), **case_result.caseresult_dic())
                        list.append(casedata)
                    else:
                        list.append(case.case_dic())
            return jsonify(
                {'code': 200, 'tableData': list, 'msg': '测试结果更新成功'})
        else:
            for case in case_info:
                if (model == case.model):
                    case_result = CaseResult.query.filter_by(caseid=case.id, testresult_id=testresult_id).first()
                    if (case_result is not None):
                        casedata = dict(case.case_dic(), **case_result.caseresult_dic())
                        list.append(casedata)
                    else:
                        list.append(case.case_dic())
            return jsonify(
                {'code': 200, 'tableData': list, 'msg': '测试结果更新成功'})
    else:
        if (key != ''):
            caseinfo = Caseinfo.query.filter(or_(Caseinfo.caseid.like("%" + key + "%"),
                                                 Caseinfo.model.like("%" + key + "%"),
                                                 Caseinfo.submodel.like("%" + key + "%"),
                                                 Caseinfo.title.like("%" + key + "%"),
                                                 Caseinfo.preconditions.like("%" + key + "%"),
                                                 Caseinfo.step.like("%" + key + "%"),
                                                 Caseinfo.expectresult.like("%" + key + "%"),
                                                 Caseinfo.remark.like("%" + key + "%"),
                                                 )).all()
            # 取key值匹配结果的用例和项目和版本匹配结果的用例的交集
            cases = set(caseinfo).intersection(set(case_info))
            for case in cases:
                case_result = CaseResult.query.filter_by(caseid=case.id, testresult_id=testresult_id).first()
                if (case_result is not None):
                    casedata = dict(case.case_dic(), **case_result.caseresult_dic())
                    list.append(casedata)
                else:
                    list.append(case.case_dic())
            return jsonify(
                {'code': 200, 'tableData': list, 'msg': '用例查询完成'})
        else:
            for case in case_info:
                case_result = CaseResult.query.filter_by(caseid=case.id, testresult_id=testresult_id).first()
                if (case_result is not None):
                    casedata = dict(case.case_dic(), **case_result.caseresult_dic())
                    list.append(casedata)
                else:
                    list.append(case.case_dic())
        return jsonify(
            {'code': 200, 'tableData': list, 'msg': '测试结果更新成功'})

@case.route('/autosave',methods=['POST'])
def autosave():
    project_id = request.json.get('project')[1]
    caseversion_id = request.json.get('caseversion')[2]
    testplan = request.json.get('testplan')
    caseid = request.json.get('caseid')
    bugid = request.json.get('bugid')
    bugremark =request.json.get('bugremark')
    bugtitle = request.json.get('bugtitle')
    testresult_id=TestPlan.query.filter_by(name=testplan,project_id=project_id,caseversion_id=caseversion_id).first().testresult_id
    caseresult=CaseResult.query.filter_by(caseid=caseid,testresult_id=testresult_id).first()
    if (caseresult is not None):
        caseresult.bugid = bugid
        caseresult.bugremark = bugremark
        caseresult.bugtitle = bugtitle
        db.session.commit()
        return jsonify(
            {'code': 200, 'msg': 'BUG信息更新成功'})
    else:
        return jsonify(
            {'code': 40001, 'msg': '先标记测试结果，然后更新bug信息'})

@case.route("/querycase", methods=['POST'])
def querycase():
    projects = request.json.get('project')
    caseversions = request.json.get('caseversion')
    model = request.json.get('model')
    key = request.json.get('key')
    list = []
    if (len(projects)!=0 and len(caseversions)!=0):
        # 通过project获取其id值
        project=projects[0]
        caseversion=caseversions[0]
        project_id = Project.query.filter_by(name=project).first().id
        case_info = CaseVersion.query.filter_by(name=caseversion, project_id=project_id).first().case_info
        if (len(model)!=0):
            if (key !=''):
                caseinfo = Caseinfo.query.filter(or_(Caseinfo.caseid.like("%" + key + "%"),
                                                     Caseinfo.model.like("%" + key + "%"),
                                                     Caseinfo.submodel.like("%" + key + "%"),
                                                     Caseinfo.title.like("%" + key + "%"),
                                                     Caseinfo.preconditions.like("%" + key + "%"),
                                                     Caseinfo.step.like("%" + key + "%"),
                                                     Caseinfo.expectresult.like("%" + key + "%"),
                                                     Caseinfo.remark.like("%" + key + "%"),
                                                     )).all()
                #取key值匹配结果的用例和项目和版本匹配结果的用例的交集
                cases=set(caseinfo).intersection(set(case_info))
                for case in cases:
                    if (model == case.model):
                        list.append(case.case_dic())
                return jsonify(
                    {'code': 200, 'tableData': list, 'msg': '用例查询完成'})
            else:
                for case in case_info:
                    if(model == case.model):
                        list.append(case.case_dic())
                return jsonify(
                    {'code': 200, 'tableData': list, 'msg': '用例查询完成'})
        else:
            if(key !=''):
                caseinfo = Caseinfo.query.filter(or_(Caseinfo.caseid.like("%" + key + "%"),
                                                     Caseinfo.model.like("%" + key + "%"),
                                                     Caseinfo.submodel.like("%" + key + "%"),
                                                     Caseinfo.title.like("%" + key + "%"),
                                                     Caseinfo.preconditions.like("%" + key + "%"),
                                                     Caseinfo.step.like("%" + key + "%"),
                                                     Caseinfo.expectresult.like("%" + key + "%"),
                                                     Caseinfo.remark.like("%" + key + "%"),
                                                     )).all()
                # 取key值匹配结果的用例和项目和版本匹配结果的用例的交集
                cases = set(caseinfo).intersection(set(case_info))
                for case in cases:
                    list.append(case.case_dic())
                return jsonify(
                    {'code': 200, 'tableData': list, 'msg': '用例查询完成'})
            else:
                for case in case_info:
                    list.append(case.case_dic())
                return jsonify(
                    {'code': 200, 'tableData': list, 'msg': '用例查询完成'})
    else:
        return jsonify(
            {'code': 40001, 'msg': '请选择用例的项目、版本'})

@case.route("/updatecase", methods=['POST'])
def updatecase():
    caseinfos=request.json.get('caseinfo')
    caseinfo=Caseinfo.query.filter_by(caseid=caseinfos.get('caseid')).first()
    if(caseinfo is not None):
        caseinfo.caseid=caseinfos.get('caseid')
        caseinfo.model=caseinfos.get('model')
        caseinfo.submodel=caseinfos.get('submodel')
        caseinfo.level=caseinfos.get('level')
        caseinfo.preconditions=caseinfos.get('preconditions')
        caseinfo.title=caseinfos.get('title')
        caseinfo.step=caseinfos.get('step')
        caseinfo.expectresult=caseinfos.get('expectresult')
        caseinfo.remark=caseinfos.get('remark')
        db.session.commit()
        return jsonify({'code': 200, 'msg': '用例更新成功'})
    else:
        return jsonify({'code': 40001, 'msg': '用例更新失败'})

@case.route("/removecase", methods=['POST'])
def removecase():
    caseinfos = request.json.get('caseinfo')
    caseinfo = Caseinfo.query.filter_by(caseid=caseinfos.get('caseid')).first()
    if (caseinfo is not None):
        db.session.delete(caseinfo)
        db.session.commit()
        return jsonify({'code': 200, 'msg': '用例删除成功'})
    else:
        return jsonify({'code': 40001, 'msg': '用例删除失败'})

@case.route("/addcase", methods=['POST'])
def addcase():
    caseinfos = request.json.get('caseinfo')
    project_name=caseinfos.get('project')
    caseversion_name=caseinfos.get('version')
    caseid=caseinfos.get('caseid')
    if(project_name is not None and caseversion_name is not None and caseid is not None):
        name = Project.query.filter_by(name=project_name).first()
        project = Project(name=project_name)
        # 如果项目名称不存在，则添加新的项目
        if (name is None):
            db.session.add(project)
            db.session.commit()
            version = CaseVersion.query.filter_by(name=caseversion_name, project_id=project.id).first()
            # 如果版本号不存在，则添加新的版本号
            if (version is None):
                caseversion = CaseVersion(name=caseversion_name, project_id=project.id)
                db.session.add(caseversion)
                db.session.commit()
        # 项目名称存在，则检测该项目下版本号是否存在
        else:
            version = CaseVersion.query.filter_by(name=caseversion_name, project_id=name.id).first()
            if (version is None):
                caseversion = CaseVersion(name=caseversion_name, project_id=name.id)
                db.session.add(caseversion)
                db.session.commit()
        caseinfo = Caseinfo(caseid=caseid,
                        model=caseinfos.get('model'),
                        submodel=caseinfos.get('submodel'),
                        level=caseinfos.get('level'),
                        title=caseinfos.get('title'),
                        preconditions=caseinfos.get('preconditions'),
                        step=caseinfos.get('step'),
                        expectresult=caseinfos.get('expectresult'),
                        remark=caseinfos.get('remark'),
                        )
        print(project)
        name = Project.query.filter_by(name=project_name).first()
        version = CaseVersion.query.filter_by(name=caseversion_name, project_id=name.id).first()
        # 添加用例和项目的关系
        caseinfo.project_id = [name]
        # 添加用例和版本的关系
        caseinfo.caseversion_id = [version]
        db.session.add(caseinfo)
        db.session.commit()
        return jsonify({'code': 200, 'msg': '用例添加成功'})
    else:
        return jsonify({'code': 40001, 'msg': '用例添加失败，请正确填写项目，用例版本，用例编号'})