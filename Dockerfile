FROM snakepacker/python:all
WORKDIR /code
COPY . .
RUN ['make', 'prepare']
RUN ['make', 'migrate']
CMD ['make', 'run']