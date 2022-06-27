FROM tiangolo/uwsgi-nginx:python3.7

ENV UWSGI_INI uwsgi.ini

ENV DJANGO_SETTINGS_MODULE=URLShortener.settings

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip3.7 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY ./ /app

EXPOSE 80
