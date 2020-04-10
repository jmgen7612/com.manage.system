#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file   :views.py
# @time   :2020/4/817:45
# @Author :jmgen
# @Version:1.0
# @Desc   :
from flask import request, jsonify
from . import result
from .. import db
from ..models import TestPlan
from ..models import Project
from ..models import Caseinfo
from ..models import CaseVersion
from ..models import CaseResult
from ..models import TestResult

@result.route("/testresult", methods=['POST'])
def testresult():
    project = request.json.get('project')[0]
    project_id = request.json.get('project')[1]
    caseversion = request.json.get('caseversion')[0]
    caseversion_id = request.json.get('caseversion')[2]
    testplan = request.json.get('testplan')
    testresult_id = TestPlan.query.filter_by(name=testplan, project_id=project_id,
                                             caseversion_id=caseversion_id).first().testresult_id
    testresult = TestResult.query.filter_by(id=testresult_id).first()
    caseinfo = CaseVersion.query.filter_by(project_id=project_id, id=caseversion_id).first().case_info
    totalcase = len(caseinfo)
    passnum = len(CaseResult.query.filter_by(testresult_id=testresult_id, caseresult='Pass').all())
    failnum = len(CaseResult.query.filter_by(testresult_id=testresult_id, caseresult='Fail').all())
    blocknum = len(CaseResult.query.filter_by(testresult_id=testresult_id, caseresult='Block').all())
    notestnum = len(CaseResult.query.filter_by(testresult_id=testresult_id, caseresult='NT').all())
    runcasenum = passnum + failnum + blocknum + notestnum
    versiontableData = []
    modeltableData = []
    model = []
    passdata=[]
    faildata=[]
    blockdata=[]
    notestdata=[]
    modelruncase=[]
    modeltotalcase=[]
    if (testresult is not None):
        testresult.resultpass = passnum
        testresult.resultfail = failnum
        testresult.resultblock = blocknum
        testresult.resultnotest = notestnum
        testresult.runcase = runcasenum
        testresult.totalcase = totalcase
        db.session.commit()
    versiontable = TestResult.query.filter_by(id=testresult_id).first().result_dic()
    versiontableData.append(versiontable)
    for case in caseinfo:
        # modeltotalcase = len(CaseResult.query.filter_by(testresult_id=testresult_id, casemodel=case.model).all())
        # modeltotalcase = len(Caseinfo.query.filter_by(model=case.model).all())
        # 所有符合model结果集和符合项目、版本的用例结果集的交集
        modeltotalcasenum = len(set(Caseinfo.query.filter_by(model=case.model).all()).intersection(set(caseinfo)))
        modelpassnum = len(
            CaseResult.query.filter_by(testresult_id=testresult_id, casemodel=case.model, caseresult='Pass').all())
        modelfailnum = len(
            CaseResult.query.filter_by(testresult_id=testresult_id, casemodel=case.model, caseresult='Fail').all())
        modelblocknum = len(
            CaseResult.query.filter_by(testresult_id=testresult_id, casemodel=case.model, caseresult='Block').all())
        modelnotestnum = len(
            CaseResult.query.filter_by(testresult_id=testresult_id, casemodel=case.model, caseresult='NT').all())
        modelruncasenum = modelpassnum + modelfailnum + modelblocknum + modelnotestnum
        caseresult=CaseResult.query.filter_by(testresult_id=testresult_id, casemodel=case.model).first()
        if case.model not in model:
            model.append(case.model)
            passdata.append(modelpassnum)
            faildata.append(modelfailnum)
            blockdata.append(modelblocknum)
            notestdata.append(modelnotestnum)
            modelruncase.append(modelruncasenum)
            modeltotalcase.append(modeltotalcasenum)
        tester=''
        if(caseresult is not None):
            tester=caseresult.tester
        result = {'project': project, 'caseversion': caseversion, 'testplan': testplan, 'model': case.model,
                  'resultpass': modelpassnum,
                  'resultfail': modelfailnum, 'resultblock': modelblocknum, 'resultnotest': modelnotestnum,
                  'runcase': modelruncasenum, 'totalcase': modeltotalcasenum, 'tester': tester}
        if (result not in modeltableData):
            modeltableData.append(result)
    versionoptions=[passnum,failnum,blocknum,notestnum,runcasenum,totalcase]
    options={'model':model,'passdata':passdata,'faildata':faildata,'blockdata':blockdata,'notestdata':notestdata,'modelruncase': modelruncase, 'modeltotalcase': modeltotalcase}
    return jsonify(
        {'code': 200, 'modeltableData': modeltableData, 'versiontableData': versiontableData,'versionoptions':versionoptions,'options':options, 'msg': '获取数据成功'})

@result.route("/getdata", methods=["GET"])
def getdata():
    # 返回项目名称和项目id
    project = Project.query.with_entities(Project.name, Project.id).all()
    # 返回测试计划名称和对应的项目id
    caseversion = CaseVersion.query.with_entities(CaseVersion.name, CaseVersion.project_id, CaseVersion.id).all()
    # 返回测试计划名称和对应的用例版本id
    testplan = TestPlan.query.with_entities(TestPlan.name, TestPlan.project_id, TestPlan.caseversion_id).all()
    return jsonify(
        {'code': 200, 'projects': project, 'caseversions': caseversion, 'testplans': testplan, 'msg': '获取数据成功'})
