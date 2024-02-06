from pydantic_settings import BaseSettings
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


class Settings(BaseSettings):
    # Read database configuration
    db_host: str = config.get('database', 'host', fallback='127.0.0.1')
    db_port: int = config.getint('database', 'port', fallback=8000)
    db_name: str = config.get('database', 'database_name')
    collection_user: str = config.get('database', 'collection_user')
    url_user: str = config.get('database', 'url_user',fallback="")
    # database mongo url
    mongo_uri: str = f"{db_host}:{db_port}"
    print(mongo_uri)
    # Read server configuration
    server_base_url: str = config.get('server', 'base_ip', fallback='127.0.0.1')
    server_port: int = config.getint('server', 'port')
 


settings = Settings()








