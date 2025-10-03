"""
Database connections
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

import mysql.connector
import redis
import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_mysql_conn():
    """Get a MySQL connection using env variables"""
    # No auth_plugin override; mysql-connector supports caching_sha2_password by default
    return mysql.connector.connect(
        host=config.DB_HOST,
        port=int(config.DB_PORT),
        user=config.DB_USER,
        password=config.DB_PASS,
        database=config.DB_NAME,
    )

def get_redis_conn():
    """Get a Redis connection using env variables"""
    return redis.Redis(
        host=config.REDIS_HOST,
        port=int(config.REDIS_PORT),
        db=int(config.REDIS_DB),
        decode_responses=True,
    )

def get_sqlalchemy_session():
    """Get an SQLAlchemy ORM session using env variables"""
    # Do NOT force mysql_native_password or any auth_plugin
    url = (
        f"mysql+mysqlconnector://{config.DB_USER}:{config.DB_PASS}"
        f"@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}?charset=utf8mb4"
    )
    engine = create_engine(url, pool_pre_ping=True, future=True)
    Session = sessionmaker(bind=engine)
    return Session()
