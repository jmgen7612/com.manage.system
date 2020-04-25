一、项目介绍

1、架构介绍

整个项目采用前后端分离实现，后端采用的是flask+sqlalchemy+Blueprint，前端采用的
vue+element ui+vxe-table+echarts来实现

2、环境部署

a、如果使用mysql，先安装mysqls数据库，配置对应的数据库账号密码，然后进行数据库初始化，进入到前端项目的路径路径下，执行以下3条命令：

python3 manage.py db init

python3 manage.py db migrate

python3 manage.py db upgrade

b、如果使用sqlite数据库，不需要安装数据库

执行python3 db_create,便可以初始化数据库

3、运行

后端：进入后端项目路径下，执行：manage.py runserver -h 172.22.70.204(本机ip)
前端：进入前端项目路径下，执行：npm run dev(或build)

4、功能介绍

主要实现了用例添加，用例修改，用例执行，执行结果统计的功能