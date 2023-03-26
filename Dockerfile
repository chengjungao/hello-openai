FROM python:3.9-alpine

COPY ./rest /hello-openai/rest
COPY ./service /hello-openai/service
COPY ./config /hello-openai/config
COPY ./gunicorn.conf.py /hello-openai/gunicorn.conf.py
COPY ./requirements.txt /hello-openai/requirements.txt
COPY ./main.py /hello-openai/main.py
COPY ./setting.py /hello-openai/setting.py

WORKDIR /hello-openai
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
EXPOSE 8080
CMD ["gunicorn -c gunicorn.conf.py main:app"]
