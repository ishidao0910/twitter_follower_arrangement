FROM python:3.9

# pipアップグレード
RUN pip install --upgrade pip
RUN pip install flask
RUN pip install config
RUN pip install requests
RUN pip install requests_oauthlib

# 作業ディレクトリ指定
WORKDIR /workdir

# 公開ポート指定
EXPOSE 8000