# FROM python
# LABEL author='wu-wenxiang@outlook.com'

# RUN apt-get update
# RUN apt-get install -y nginx supervisor systemd vim
# RUN pip install gunicorn
# RUN pip install setuptools

# RUN pip install gevent
# RUN pip install django==2.2.6
# RUN pip install django-filter
# RUN pip install monthdelta
# RUN pip install Pillow
# RUN pip install xlrd
# RUN pip install xlsxwriter
# RUN pip install pypinyin

# ENV PYTHONIOENCODING=utf-8

FROM maodouzi/django:v2.2.6
LABEL purpose='ECUST Course Search'

# Build folder
RUN mkdir -p /home/www/ecustCourseInfo/logs
RUN mkdir -p /home/www/ecustCourseInfo/tool
RUN mkdir -p /home/www/ecustCourseInfo/src
WORKDIR /home/www/ecustCourseInfo
COPY courseinfo /home/www/ecustCourseInfo/src/courseinfo
RUN rm -rf /home/www/ecustCourseInfo/src/courseinfo/db.sqlite3
# RUN cd /home/www/ecustCourseInfo/src/courseinfo && python manage.py migrate && python initdb.py && rm -rf initdb.py
RUN rm -rf /home/www/ecustCourseInfo/src/courseinfo/static
RUN pip install -r /home/www/ecustCourseInfo/src/courseinfo/requirements.txt
RUN cd /home/www/ecustCourseInfo/src/courseinfo && python manage.py collectstatic

# Setup nginx
RUN rm /etc/nginx/sites-enabled/default
ADD docker-config/nginx.conf /etc/nginx/sites-available/ecustCourseInfo.conf
RUN ln -s /etc/nginx/sites-available/ecustCourseInfo.conf /etc/nginx/sites-enabled/ecustCourseInfo.conf
# RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# # Setup supervisord
# RUN mkdir -p /var/log/supervisor
# COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
# COPY gunicorn.conf /etc/supervisor/conf.d/gunicorn.conf

# run sh. Start processes in docker-compose.yml
#CMD ["/usr/bin/supervisord"]
ADD docker-config/supervisord.conf /etc/supervisor/supervisord.conf
ADD docker-config/supervisor.conf /etc/supervisor/conf.d/ecustCourseInfo.conf
ADD docker-config/start.sh /tmp/start.sh
EXPOSE 80
CMD [ "sh", "/tmp/start.sh" ]



