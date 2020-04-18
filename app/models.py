#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file   :views.py
# @time   :2020/3/2017:00
# @Author :jmgen
# @Version:1.0
# @Desc   :
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    avatar_hash = db.Column(db.String(32))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email is not None and self.avatar_hash is not None:
            self.avatar_hash = hashlib.md5(self.email.encode("utf-8")).hexdigest()

    @property
    def password(self):
        raise ArithmeticError(u"密码不可读")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def gravatar(self, size=40, default='identicon', rating='g'):
        url = 'https://gravatar.loli.net/avatar'
        hash = self.avatar_hash or hashlib.md5(self.email.encode('utf-8')).hexdigest()

        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(url=url, hash=hash, size=size, default=default,
                                                                     rating=rating)
# 项目用例--多对多关系映射表
project_caseinfo = db.Table('project_caseinfo',
                            db.Column("project_id", db.Integer, db.ForeignKey('project.id')),
                            db.Column("caseinfo_id", db.Integer, db.ForeignKey('caseinfo.id'))
                            )

# 用例版本用例表--多对多关系映射表
caseversion_caseinfo = db.Table('caseversion_caseinfo',
                                db.Column("caseversion_id", db.Integer, db.ForeignKey('caseversion.id')),
                                db.Column("caseinfo_id", db.Integer, db.ForeignKey('caseinfo.id'))
                                )

# 用例信息表
class Caseinfo(db.Model):
    __tablename__ = 'caseinfo'
    # 主键
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    # 用例编号
    caseid = db.Column(db.String(32), nullable=False, unique=True)
    # 主模块
    model = db.Column(db.String(256), nullable=False)
    # 子模块
    submodel = db.Column(db.String(256))
    # 优先级
    level = db.Column(db.String(256))
    # 标题
    title = db.Column(db.String(1024))
    # 前提条件
    preconditions = db.Column(db.String(256))
    # 测试步骤
    step = db.Column(db.String(1024))
    # 期望结果
    expectresult = db.Column(db.String(256))
    # 备注
    remark = db.Column(db.String(256))

    # 添加和project关联
    project_id = db.relationship('Project', secondary=project_caseinfo,
                                 backref='case_info',
                                 lazy='dynamic')
    #添加和caseversion关联
    caseversion_id = db.relationship('CaseVersion', secondary=caseversion_caseinfo,
                                     backref='case_info',
                                     lazy='dynamic')

    def case_dic(self):
        caseinfo_dic={
            'id':self.id,
            'caseid':self.caseid,
            'model':self.model,
            'submodel':self.submodel,
            'level':self.level,
            'preconditions':self.preconditions,
            'title':self.title,
            'step':self.step,
            'expectresult':self.expectresult,
            'remark':self.remark
        }
        return caseinfo_dic

# 项目表
class Project(db.Model):
    __tablename__ = "project"
    # 主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    # 项目名称
    name = db.Column(db.String(128), nullable=False, unique=True)
    # 新建了一个名叫testplan_id的属性用来表示当前项目中包含的测试计划列表.
    testplan_id = db.relationship("TestPlan", backref="project_info", lazy="dynamic")

# 用例版本表
class CaseVersion(db.Model):
    __tablename__ = "caseversion"
    # 主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    # 用例版本名称
    name = db.Column(db.String(128), nullable=False)
    # 创建一个外键属性，并关联project的id字段
    project_id=db.Column(db.Integer, db.ForeignKey("project.id"))
    # 在SQLAlchemy建模中,我们需要在被关联的模型CaseVersion中添加关系.这其实是面向对象的思想,
    # testplan_id被定义成一个db.relationship对象,该对象的构造函数由两部分组成
    # 'TestPlan'表示关系的另一端模型的名称.
    # backref的参数,叫做反向关系,我们将其设置成'version_info',它会像TestPlan模型中添加一个名叫做version_info的属性,
    # 这个属性可以替代caseversion_id访问CaseVersion模型,但是它获取的是CaseVersion模型的对象,而非CaseVersion模型对应的id的值
    # 新建了一个名叫testplan_id的属性用来表示当前用例版本中包含的测试计划列表.
    testplan_id = db.relationship("TestPlan", backref="version_info", lazy="dynamic")

#测试结果表
class TestResult(db.Model):
    __tablename__ = "testresult"
    # 主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    #结果统计名称
    name=db.Column(db.String(128), nullable=False)
    #通过测试结果统计
    resultpass=db.Column(db.Integer)
    # 测试失败结果统计
    resultfail=db.Column(db.Integer)
    #用例锁定结果统计
    resultblock=db.Column(db.Integer)
    #没有测试的用例结果统计
    resultnotest=db.Column(db.Integer)
    #执行用例数
    runcase=db.Column(db.Integer)
    #总用例数
    totalcase=db.Column(db.Integer)
    # 新建了一个名叫testplan_id的属性用来表示当前测试结果中关联的测试计划.
    testplan_id = db.relationship("TestPlan", backref="testresult_info", uselist=False)
    # 新建了一个名叫caseresult_id的属性用来表示当前测试结果中关联的用例测试结果.
    caseresult_id = db.relationship("CaseResult", backref="testresult_info", uselist=False)

    def result_dic(self):
        result_dic={
            'id': self.id,
            'name': self.name,
            'resultpass': self.resultpass,
            'resultfail': self.resultfail,
            'resultblock': self.resultblock,
            'resultnotest': self.resultnotest,
            'runcase': self.runcase,
            'totalcase': self.totalcase,
        }
        return result_dic

#用例测试结果表
class CaseResult(db.Model):
    __tablename__ = "caseresult"
    # 主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    #用例id
    caseid=db.Column(db.Integer)
    #用例模块
    casemodel=db.Column(db.String(32))
    #结果标记
    caseresult=db.Column(db.String(32))
    # 缺陷ID
    bugid = db.Column(db.String(128))
    # 缺陷标题
    bugtitle = db.Column(db.String(128))
    # 缺陷备注
    bugremark = db.Column(db.String(128))
    # 测试提交人
    tester = db.Column(db.String(32))
    # 测试提交时间
    testtime = db.Column(db.String(32))
    # 创建一个外键属性，并关联testresult的id字段
    testresult_id = db.Column(db.Integer, db.ForeignKey("testresult.id"))

    def caseresult_dic(self):
        result_dic = {
            'caseresult': self.caseresult,
            'bugid': self.bugid,
            'bugtitle': self.bugtitle,
            'bugremark': self.bugremark,
            'tester': self.tester,
            'testtime': self.testtime,
        }
        return result_dic

# 测试计划表
class TestPlan(db.Model):
    __tablename__ = "testplan"
    # 主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    # 测试计划名称
    name = db.Column(db.String(128), nullable=False)
    # 创建一个外键属性，并关联caseversion的id字段
    caseversion_id = db.Column(db.Integer, db.ForeignKey("caseversion.id"))
    # 创建一个外键属性，并关联project的id字段
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))
    # 创建一个外键属性，并关联testresult的id字段
    testresult_id = db.Column(db.Integer, db.ForeignKey("testresult.id"))