FROM python:3.11-bullseye
ARG CHINA_WORKAROUND=false
RUN if [ "${CHINA_WORKAROUND}" = "true" ] ; then \
      pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
      true; \
    fi
RUN python3 -m pip install --verbose uwsgi==2.0.21 poetry==1.4.0 && \
    poetry config virtualenvs.create false

# force poetry using pip. https://github.com/python-poetry/poetry/issues/1632
RUN if [ "${CHINA_WORKAROUND}" = "true" ] ; then \
      poetry config experimental.new-installer false && \
      true; \
    fi

COPY poetry.lock pyproject.toml /opt/src/
WORKDIR /opt/src
RUN poetry install --no-interaction -vvv

COPY . /opt/src/

RUN chmod +x ./entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]