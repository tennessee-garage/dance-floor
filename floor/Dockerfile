FROM nikolaik/python-nodejs:python3.11-nodejs18

RUN mkdir /app
WORKDIR /app

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  BABEL_CACHE=0

COPY pyproject.toml poetry.lock /
RUN poetry config virtualenvs.create false && \
  poetry install --no-interaction --no-root --no-dev --compile && \
  rm -rf ~/.cache/pypoetry && \
  rm -rf ~/.config/pypoetry
COPY package.json yarn.lock /app/
RUN yarn install --frozen-lockfile --no-cache --production && yarn cache clean

COPY ./ /app/
RUN yarn build-prod && rm -rf node_modules/.cache
RUN ./manage.py collectstatic --noinput --ignore='*.map'

EXPOSE 8000
ENV PORT 8000

CMD /app/bin/prodserver
