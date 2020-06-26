# from pymongo import MongoClient
# import logging


# class DataBase:
#     client: MongoClient = None


# client = DataBase()


# def start_db_connection():
#     logging.info("starting connection")
#     client.client = MongoClient(
#         "url"
#     )
#     logging.info("started connection")


# def close_db_connection():
#     logging.info("closing db connection...")
#     client.client.close()
#     logging.info("connection closed！")


# def get_database() -> MongoClient:
#     return client.client
