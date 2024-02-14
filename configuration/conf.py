from pydantic_settings import BaseSettings
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


class Settings(BaseSettings):
    # Read database configuration
    db_host: str = config.get('database', 'host', fallback='127.0.0.1')
    db_port: int = config.getint('database', 'port', fallback=8000)
    db_name: str = config.get('database', 'database_name')
    #users
    collection_users: str = config.get('database', 'collection_users')
    url_users: str = config.get('database', 'url_users',fallback="")
     #users in process
    collection_usersInprocess: str = config.get('database', 'collection_userInprocess')
    url_usersInprocess: str = config.get('database', 'url_usersInprocess',fallback="")
    #lpns
    collection_lpns: str = config.get('database', 'collection_lpns')
    url_lpns: str = config.get('database', 'url_lpns',fallback="")    
    #logs
    collection_logs: str = config.get('database', 'collection_logs')
    url_logs: str = config.get('database', 'url_logs',fallback="")  
    url_reports: str = config.get('database', 'url_reports',fallback="") 
    #logs
    collection_admins: str = config.get('database', 'collection_admins')
    url_admins: str = config.get('database', 'url_admins',fallback="")  
    # Read server configuration
    server_base_url: str = config.get('server', 'base_ip', fallback='127.0.0.1')
    server_port: int = config.getint('server', 'port')
 


settings = Settings()








