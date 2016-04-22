############################################################
# Dockerfile to build itv-chat container images
############################################################

FROM python:3.5.1-onbuild
MAINTAINER avezhenya

ENV PROD True
EXPOSE 8889
CMD [ "python", "./twaddle-chat/app.py" ]