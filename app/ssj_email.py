#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#@file   :ssj_email.py
#@time   :2018/6/25 21:02
#@Author :jmgen
#@Version:1.0
#@Desc   :
import smtplib,re,os,shutil
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import parseaddr,formataddr
from email.mime.multipart import MIMEMultipart
from config.email_info import EmailInfo

class Email:
    def sendEmail(self,path,subject):
        from_addr = EmailInfo.FROM_ADDR
        password = EmailInfo.PASSWORD
        msg = MIMEMultipart()
        msg['From'] = self._format_addr('Android UI自动化测试<%s>' % from_addr)
        filenames = self._get_file(path)
        to_addr = EmailInfo.TO_ADDR_NORMAL
        cc_addr = EmailInfo.CC_ADDR_NORMAL
        for filename in filenames:
            name = '随手记Android V%s自动化回归测试报告%s.html' % (self._get_version(filename), self._get_device(filename))
            with open(filename, 'rb') as f:
                mime = MIMEBase('file', 'html', filename=name)
                mime.add_header('Content-Disposition', 'attachment', filename=name)
                mime.set_payload(f.read())
                encoders.encode_base64(mime)
                msg.attach(MIMEText(self._get_content(filename), 'html', 'utf-8'))
                msg.attach(mime)
            if self._get_passrate(filename) <= 95:
                to_addr = EmailInfo.TO_ADDR_ABNORMAL
                cc_addr = EmailInfo.CC_ADDR_ABNORMAL
        msg['To'] = to_addr
        msg['Cc'] = cc_addr
        msg['Subject'] = Header(subject, 'utf-8').encode()
        smtp_server = EmailInfo.SMTP_SERVER
        server = smtplib.SMTP_SSL(smtp_server, 465)
        server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, to_addr.split(','), msg.as_string())
        server.quit()
        self._backup_file(path)

    def _get_content(self,filename):
        with open(filename, 'r',encoding='utf-8') as f:
            lines=f.readlines()
            text=[]
            title='<title>随手记Android回归测试执行报告'
            chart='id="chart"'
            position = 'position:absolute'
            for line in lines:
                if title in line:
                    text.append(self._get_text(filename))
                    text.append(line)
                elif chart in line:
                    pass
                elif position in line:
                    text.append('position:relative;')
                else:
                    text.append(line)
            content='\r\n'.join(text)+'<hr><br>'
        return content

    def _get_text(self,filename):
        style='<style type="text/css">h2{ text-indent:2em;}</style> '
        title='<h1>Dear All,</h1>'
        main='<h2>这个是随手记Android V%s版本%s的UI自动化测试报告，其中执行的用例总数为%s，成功%s，失败%s，用例的测试通过率为%s%%，请各位查收！谢谢！</h2>'%(self._get_version(filename), self._get_device(filename),self._get_count(filename),self._get_pass(filename),self._get_fail(filename),self._get_passrate(filename))
        text=style+'\r\n'+title+'\r\n'+main+'<hr><br>'
        return  text

    def _get_count(self,filename):
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            text = []
            name='>全部'
            for line in lines:
                if name in line:
                    text=line
                    break
            count=int(re.findall(r"全部\((.+?)\)</button>",text)[0])
            return count

    def _get_fail(self,filename):
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            text = []
            name='>失败'
            for line in lines:
                if name in line:
                    text=line
                    break
            failcount=int(re.findall(r"失败\((.+?)\)</button>",text)[0])
            return failcount

    def _get_pass(self,filename):
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            text = []
            name='>成功'
            for line in lines:
                if name in line:
                    text=line
                    break
            passcount=int(re.findall(r"成功\((.+?)\)</button>",text)[0])
            return passcount

    def _get_passrate(self,filename):
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            text = []
            name='状态'
            for line in lines:
                if name in line:
                    text=line
                    break
            passrate=float(re.findall(r"成功率 (.+?)%</p>",text)[0])
            return passrate

    def _get_device(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            text = []
            name='测试设备信息'
            for line in lines:
                if name in line:
                    text=line
                    break
            version=re.findall(r"/strong> (.+?)</p>",text)[0]
            return version

    def _get_version(self,filename):
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            text = []
            name='软件版本'
            for line in lines:
                if name in line:
                    text=line
                    break
            version=re.findall(r"/strong> (.+?)</p>",text)[0]
            return version

    def _format_addr(self,s):
        name,addr=parseaddr(s)
        return formataddr((Header(name,'utf-8').encode(),addr))

    def _get_file(self,path):
        listfile = [x for x in os.listdir(path) if os.path.isfile(os.path.join(path, x))]
        filenames=[]
        for f in listfile:
            name=os.path.join(path, f)
            filenames.append(name)
        return filenames

    def _backup_file(self,path):
        listfile = [x for x in os.listdir(path) if os.path.isfile(os.path.join(path, x))]
        for f in listfile:
            src=os.path.join(path, f)
            dst=os.path.join(path, "backup")
            shutil.move(src,os.path.join(dst, f))

if __name__ == '__main__':
    PATH = lambda p: os.path.abspath(
        os.path.join(os.path.dirname(__file__), p)
    )
    email=Email()
    email.sendEmail(PATH('../report/'), "随手记Android UI自动化测试报告")

