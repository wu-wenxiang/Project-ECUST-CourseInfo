FROM python
LABEL author='wu-wenxiang@outlook.com'
LABEL purpose='ECUST Course Search'

RUN apt-get update
RUN apt-get install -y nginx supervisor systemd
RUN pip install gunicorn
RUN pip install setuptools

ENV PYTHONIOENCODING=utf-8

# Build folder
RUN mkdir -p /home/www/ecustCourseInfo/logs
RUN mkdir -p /home/www/ecustCourseInfo/tool
RUN mkdir -p /home/www/ecustCourseInfo/src
WORKDIR /home/www/ecustCourseInfo
COPY courseinfo /home/www/ecustCourseInfo/src/courseinfo
RUN pip install -r /home/www/ecustCourseInfo/src/courseinfo/requirements.txt

RUN cd /home/www/ecustCourseInfo/src/courseinfo && python3 manage.py collectstatic

# Setup nginx
RUN rm /etc/nginx/sites-enabled/default
COPY nginx_ecust_course_info.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/nginx_ecust_course_info.conf /etc/nginx/sites-enabled/nginx_ecust_course_info.conf
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# Setup supervisord
RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY gunicorn.conf /etc/supervisor/conf.d/gunicorn.conf

# run sh. Start processes in docker-compose.yml
#CMD ["/usr/bin/supervisord"]
ADD docker-config/supervisord.conf /etc/supervisor/supervisord.conf
ADD docker-config/supervisor.conf /etc/supervisor/conf.d/ecustCourseInfo.conf
ADD docker-config/nginx.conf /etc/nginx/conf.d/ecustCourseInfo.conf
ADD docker-config/start.sh /tmp/start.sh
EXPOSE 80
CMD [ "sh", "/tmp/start.sh" ]



