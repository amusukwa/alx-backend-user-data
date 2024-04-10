#!/usr/bin/env python3
"""
Module for Log filtering
"""

import logging
import csv
from typing import List
import os
import mysql.connector


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    def __init__(self, fields=tuple()):
        self.fields = fields
        super().__init__()

    def format(self, record: logging.LogRecord) -> str:
        record.msg = self.filter_datum(record.msg)
        return super().format(record)

    def filter_datum(self, message):
        for field in self.fields:
            message = message.replace(field, "****")
        return message

class StreamHandler(logging.StreamHandler):
    """ StreamHandler class """

    def __init__(self, stream=None):
        super().__init__(stream)
        self.setFormatter(RedactingFormatter(PII_FIELDS))

PII_FIELDS = ("name", "email", "phone", "ssn", "password")

def get_logger() -> logging.Logger:
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = StreamHandler()
    logger.addHandler(stream_handler)

    return logger

def get_db():
    # Get database credentials from environment variables or set defaults
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME", "my_db")
    
    # Connect to the database
    try:
        connection = mysql.connector.connect(
            user=username,
            password=password,
            host=host,
            database=database
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to the database: {err}")
        return None

def main():
    logger = get_logger()
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users;")
    for row in cursor:
        filtered_row = {key: "****" if key in PII_FIELDS else value for key, value in row.items()}
        logger.info("{}".format(filtered_row))

    cursor.close()
    db.close()
