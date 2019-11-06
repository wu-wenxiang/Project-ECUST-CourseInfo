# Project-ECUST-CourseInfo

## 本地运行代码

1. 切换到 Python3 环境，可以用虚拟环境 virtualenv，总之要确认 `python --version` 的输出是 `Python3` 字样

	```console
	$ python --version
	Python 3.7.3
	$ pip --version
	pip 19.3.1 from /usr/local/lib/python3.7/site-packages/pip (python 3.7)
	```

1. 切换到 courseinfo 目录，初始化数据库

	```bash
	python manage.py migrate
	python manage.py flush --noinput
	python initdb.py
	```

1. 运行站点，浏览器访问：`http://127.0.0.1:8000/`

	```console
	$ python manage.py runserver
	...
	Starting development server at http://127.0.0.1:8000/
	Quit the server with CONTROL-C.
	```

## 制作 Docker 镜像

1. 确认本地 Docker Daemon 正常运行

	```console
	$ docker run hello-world

	Hello from Docker!
	...
	```

1. 切换回本项目的根目录，确认目录中包含 Dockerfile 文件，**注意：`auser/djangodemo` 中的 auser 是你 dockerhub 的账户名**

	```console
	$ ls
	Dockerfile    README.md     ansible-u1804 courseinfo    docker-config

	$ docker build -t auser/djangodemo .
	Sending build context to Docker daemon  21.11MB
	Step 1/20 : FROM maodouzi/django:v2.2.6
	 ---> 0e1a814c3248
	Step 2/20 : LABEL purpose='ECUST Course Search'
	 ---> Using cache
	 ---> bff5922c57b5
	Step 3/20 : RUN mkdir -p /home/www/ecustCourseInfo/logs
	 ---> Using cache
	 ---> bffb926b0f6d
	Step 4/20 : RUN mkdir -p /home/www/ecustCourseInfo/tool
	 ---> Using cache
	 ---> 360859de08ea
	Step 5/20 : RUN mkdir -p /home/www/ecustCourseInfo/src
	 ---> Using cache
	 ---> 62dd70a4ea4b
	Step 6/20 : WORKDIR /home/www/ecustCourseInfo
	 ---> Using cache
	 ---> 3eee6ba2d4bf
	Step 7/20 : COPY courseinfo /home/www/ecustCourseInfo/src/courseinfo
	 ---> 49fcb3705f3b
	Step 8/20 : RUN pip install -r /home/www/ecustCourseInfo/src/courseinfo/requirements.txt
	 ---> Running in a68f17c6f076
	Requirement already satisfied: gevent in /usr/local/lib/python3.8/site-packages (from -r /home/www/ecustCourseInfo/src/courseinfo/requirements.txt (line 1)) (1.4.0)
	Requirement already satisfied: django==2.2.6 in /usr/local/lib/python3.8/site-packages (from -r /home/www/ecustCourseInfo/src/courseinfo/requirements.txt (line 2)) (2.2.6)
	Requirement already satisfied: django-filter in /usr/local/lib/python3.8/site-packages (from -r /home/www/ecustCourseInfo/src/courseinfo/requirements.txt (line 3)) (2.2.0)
	Requirement already satisfied: monthdelta in /usr/local/lib/python3.8/site-packages (from -r /home/www/ecustCourseInfo/src/courseinfo/requirements.txt (line 4)) (0.9.1)
	Requirement already satisfied: Pillow in /usr/local/lib/python3.8/site-packages (from -r /home/www/ecustCourseInfo/src/courseinfo/requirements.txt (line 5)) (6.2.1)
	Requirement already satisfied: xlrd in /usr/local/lib/python3.8/site-packages (from -r /home/www/ecustCourseInfo/src/courseinfo/requirements.txt (line 6)) (1.2.0)
	Requirement already satisfied: xlsxwriter in /usr/local/lib/python3.8/site-packages (from -r /home/www/ecustCourseInfo/src/courseinfo/requirements.txt (line 7)) (1.2.2)
	Requirement already satisfied: pypinyin in /usr/local/lib/python3.8/site-packages (from -r /home/www/ecustCourseInfo/src/courseinfo/requirements.txt (line 8)) (0.36.0)
	Requirement already satisfied: greenlet>=0.4.14; platform_python_implementation == "CPython" in /usr/local/lib/python3.8/site-packages (from gevent->-r /home/www/ecustCourseInfo/src/courseinfo/requirements.txt (line 1)) (0.4.15)
	Requirement already satisfied: pytz in /usr/local/lib/python3.8/site-packages (from django==2.2.6->-r /home/www/ecustCourseInfo/src/courseinfo/requirements.txt (line 2)) (2019.3)
	Requirement already satisfied: sqlparse in /usr/local/lib/python3.8/site-packages (from django==2.2.6->-r /home/www/ecustCourseInfo/src/courseinfo/requirements.txt (line 2)) (0.3.0)
	Removing intermediate container a68f17c6f076
	 ---> 9459c50dd97d
	Step 9/20 : RUN rm -rf /home/www/ecustCourseInfo/src/courseinfo/db.sqlite3
	 ---> Running in 4d8709a89ec3
	Removing intermediate container 4d8709a89ec3
	 ---> 20e8b08f694e
	Step 10/20 : RUN cd /home/www/ecustCourseInfo/src/courseinfo && python manage.py migrate && python initdb.py
	 ---> Running in 6ce5af2592bb
	Operations to perform:
	  Apply all migrations: admin, auth, classroom, contenttypes, sessions
	Running migrations:
	  Applying contenttypes.0001_initial... OK
	  Applying auth.0001_initial... OK
	  Applying admin.0001_initial... OK
	  Applying admin.0002_logentry_remove_auto_add... OK
	  Applying admin.0003_logentry_add_action_flag_choices... OK
	  Applying contenttypes.0002_remove_content_type_name... OK
	  Applying auth.0002_alter_permission_name_max_length... OK
	  Applying auth.0003_alter_user_email_max_length... OK
	  Applying auth.0004_alter_user_username_opts... OK
	  Applying auth.0005_alter_user_last_login_null... OK
	  Applying auth.0006_require_contenttypes_0002... OK
	  Applying auth.0007_alter_validators_add_error_messages... OK
	  Applying auth.0008_alter_user_username_max_length... OK
	  Applying auth.0009_alter_user_last_name_max_length... OK
	  Applying auth.0010_alter_group_name_max_length... OK
	  Applying auth.0011_update_proxy_permissions... OK
	  Applying classroom.0001_initial... OK
	  Applying sessions.0001_initial... OK
	Removing intermediate container 6ce5af2592bb
	 ---> e9752e141bff
	Step 11/20 : RUN rm -rf /home/www/ecustCourseInfo/src/courseinfo/static
	 ---> Running in 575f58f5be82
	Removing intermediate container 575f58f5be82
	 ---> 863cabbd0ebd
	Step 12/20 : RUN cd /home/www/ecustCourseInfo/src/courseinfo && python manage.py collectstatic
	 ---> Running in e666948b1df0

	170 static files copied to '/home/www/ecustCourseInfo/src/courseinfo/static'.
	Removing intermediate container e666948b1df0
	 ---> 63d16b0cc029
	Step 13/20 : RUN rm /etc/nginx/sites-enabled/default
	 ---> Running in c1ba0c45f34b
	Removing intermediate container c1ba0c45f34b
	 ---> 218deaabca35
	Step 14/20 : ADD docker-config/nginx.conf /etc/nginx/sites-available/ecustCourseInfo.conf
	 ---> 3892915668aa
	Step 15/20 : RUN ln -s /etc/nginx/sites-available/ecustCourseInfo.conf /etc/nginx/sites-enabled/ecustCourseInfo.conf
	 ---> Running in d4d603cc3dc5
	Removing intermediate container d4d603cc3dc5
	 ---> 9d6f70675a76
	Step 16/20 : ADD docker-config/supervisord.conf /etc/supervisor/supervisord.conf
	 ---> 478a19c6e17f
	Step 17/20 : ADD docker-config/supervisor.conf /etc/supervisor/conf.d/ecustCourseInfo.conf
	 ---> 0e890caf97d3
	Step 18/20 : ADD docker-config/start.sh /tmp/start.sh
	 ---> b95699597b0c
	Step 19/20 : EXPOSE 80
	 ---> Running in f109d2f10bcc
	Removing intermediate container f109d2f10bcc
	 ---> f9af7b33a4de
	Step 20/20 : CMD [ "sh", "/tmp/start.sh" ]
	 ---> Running in 25bedf25c059
	Removing intermediate container 25bedf25c059
	 ---> 52c793bdcd5a
	Successfully built 52c793bdcd5a
	Successfully tagged auser/djangodemo:latest
	```

1. 在本地测试和运行 Docker 镜像，然后在浏览器上访问: `http://localhost`

	```console
	$ docker run -d -p 80:80 auser/djangodemo:latest
	221fc877103e55b6a452e8d69838232e122a357972aa08ac4421212395b892bf
	```

1. 停止 Docker 镜像

	```console
	docker stop 221fc877103e55b6a452e8d69838232e122a357972aa08ac4421212395b892bf
	```

1. 镜像上传到 Docker hub

	```bash
	docker login
	docker push auser/djangodemo:latest
	```

## 部署到远端站点

1. 配置 ~/.ssh/config 文件，HostName 可以直接写 IP 地址，IdentityFile 是密钥文件，可以用 ssh-keygen 生成，然后通过 ssh-copy-id 拷贝到远端机器上取。

	```
	Host course
	    HostName        demo-course-search.trystack.cn
	    User            root
	    IdentityFile    ~/.ssh/id_rsa_test
	```

	```console
	$ ssh-keygen
	Generating public/private rsa key pair.
	Enter file in which to save the key (/Users/wuwenxiang/.ssh/id_rsa): /Users/wuwenxiang/.ssh/id_rsa_test
	Enter passphrase (empty for no passphrase):
	Enter same passphrase again:
	Your identification has been saved in /Users/wuwenxiang/.ssh/id_rsa_test.
	Your public key has been saved in /Users/wuwenxiang/.ssh/id_rsa_test.pub.
	The key fingerprint is:
	SHA256:InvociMYhpxxK+FObSyvLYKDA5+GW3SYckqEHyrhbZY wuwenxiang@wuwenxiangdembp
	The key's randomart image is:
	+---[RSA 2048]----+
	|                 |
	|.                |
	|o..              |
	|o*.=.            |
	|Bo&E+ . S        |
	|*&o* + .         |
	|O=*.o .          |
	|O+Boo.           |
	|o*o=..           |
	+----[SHA256]-----+

	$ ssh-copy-id root@demo-course-search.trystack.cn -i ~/.ssh/id_rsa_test.pub
	/usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/Users/wuwenxiang/.ssh/id_rsa_test.pub"
	/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
	/usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys

	Number of key(s) added:        1

	Now try logging into the machine, with:   "ssh 'root@demo-course-search.trystack.cn'"
	and check to make sure that only the key(s) you wanted were added.
	```

1. 确认能不用用户名密码，直接访问远端机器

	```console
	$ ssh course
	Welcome to Ubuntu 18.04.3 LTS (GNU/Linux 4.15.0-52-generic x86_64)
	...
	Last login: Wed Nov  6 18:47:17 2019 from 116.238.98.242
	```

1. 切换到 ansible-u1804目录，复制 `inventory/inventory.ini.example`，并修改 webserver 的名字

	```console
	$ ls
	README.md inventory playbooks

	$ cp inventory/inventory.ini.example inventory/inventory.ini

	$ cat inventory/inventory.ini
	[all:vars]
	image_name="auser/djangodemo"

	[webserver]
	course
	```

1. 执行部署

	```console
	$ ansible-playbook -i inventory/inventory.ini playbooks/deploy.yml

	PLAY [webserver] *****************************************************************************************************************

	TASK [Gathering Facts] ***********************************************************************************************************
	ok: [course]

	TASK [init01_pre_install : apt-get update] ***************************************************************************************

	...
	```

1. 执行完毕后，可以通过浏览器访问远程机器
