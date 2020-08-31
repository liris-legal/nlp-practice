FROM python:3.7

ENV APP_PATH /app
ENV PYTHONPATH ${PYTHONPATH}:${APP_PATH}
ENV JUPYTER_PATH ${JUPYTER_PATH}:${APP_PATH}
ENV DATAPATH ${APP_PATH}/data
ENV LOG_SAVE_PATH ${APP_PATH}/logs

WORKDIR ${DATAPATH}
WORKDIR ${LOG_SAVE_PATH}
WORKDIR ${APP_PATH}

COPY ./ ./

RUN chmod +x run.sh

RUN apt-get update -q && \
    apt-get install -y -q --no-install-recommends nodejs npm && \
    unzip -q data.zip && \
    python -m pip install --upgrade pip && \
    pip install -q -r ./requirements.txt && \
    python -m nltk.downloader all && \
    jupyter serverextension enable --py jupyterlab && \
    jupyter labextension install @jupyterlab/toc && \
    jupyter labextension install @lckr/jupyterlab_variableinspector

CMD ["./run.sh"]
