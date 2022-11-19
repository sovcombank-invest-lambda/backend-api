FROM python:3.10
WORKDIR /code
COPY . .
RUN ["apt", "update"]
RUN ["apt", "install", "make"]
RUN ["apt", "install", "python3-psycopg2"]
RUN ["make", "prepare"]
RUN ["make", "migrate"]
CMD ["make", "run"]