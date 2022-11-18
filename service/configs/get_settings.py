from service.configs.fastapi import FastapiSettings
from service.configs.postgres import PostgresSettings


def get_postgres_settings() -> PostgresSettings:
    return PostgresSettings()


def get_fastapi_settings() -> FastapiSettings:
    return FastapiSettings()
