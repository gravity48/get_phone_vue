import datetime

import sqlalchemy, psycopg2
import socket
from collections import namedtuple
from sqlalchemy import text
from sqlalchemy import create_engine, select
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, Text, Column, ForeignKey, Sequence, String, VARCHAR, BigInteger, DateTime, BLOB
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import or_, and_
from typing import NamedTuple
import time
import os
from loguru import logger

Base = declarative_base()


class PersonDataView:

    def __init__(self, full_name, paragraph, filepath, filename, doc_date):
        self.full_name = full_name
        self.paragraph = paragraph
        self.filepath = filepath
        self.filename = filename
        self.doc_date = doc_date


class PhoneView:
    def __init__(self, phone, paragraph, filename, filepath, date):
        self.phone = phone
        self.paragraph = paragraph
        self.filename = filename
        self.filepath = filepath
        self.date = date


document_status = {
    'success': 1,
    'timeout': 2,
    'unicode': 3,
    'unexpected': 4,
    'process': 5,
}


class DocStatusTable(Base):
    __tablename__ = 'doc_status'
    id = Column(Integer, primary_key=True, autoincrement=True)
    status_name = Column(VARCHAR(100))
    document = relationship("DocumentsTable", back_populates='status')


class DocumentsTable(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True, autoincrement=True)
    status_id = Column(Integer, ForeignKey("doc_status.id"))
    filename = Column(VARCHAR(500))
    filepath = Column(VARCHAR(1000))
    date = Column(DateTime)
    status = relationship("DocStatusTable", back_populates="document")
    paragraphs = relationship("ParagraphTable", back_populates="document", cascade='all, delete')

    def __init__(self, filename, path, status_id, date):
        self.filename = filename
        self.filepath = path
        self.status_id = status_id
        if date is None:
            self.date = datetime.datetime.now()

    pass


class ParagraphTable(Base):
    __tablename__ = 'paragraphs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    doc_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"))
    text = Column(BLOB)
    document = relationship("DocumentsTable", back_populates="paragraphs")

    telephones = relationship("PhonesTable", back_populates="paragraph", cascade='all, delete')
    surnames = relationship("SurnamesTable", back_populates="paragraph", cascade='all, delete')

    def __init__(self, text):
        self.text = text

    pass


class PhonesTable(Base):
    __tablename__ = 'telephones'
    id = Column(Integer, primary_key=True, autoincrement=True)
    paragraph_id = Column(Integer, ForeignKey("paragraphs.id", ondelete="CASCADE"))
    number = Column(VARCHAR(50))
    number_integer = Column(BigInteger, nullable=False)
    paragraph = relationship("ParagraphTable", back_populates="telephones")

    def __init__(self, number):
        self.number = number
        self.number_integer = int(number)

    pass


class SurnamesTable(Base):
    __tablename__ = 'surnames'
    id = Column(Integer, primary_key=True, autoincrement=True)
    paragraph_id = Column(Integer, ForeignKey("paragraphs.id", ondelete="CASCADE"))
    name = Column(VARCHAR(100))
    patronymic = Column(VARCHAR(100))
    surname = Column(VARCHAR(100))
    paragraph = relationship("ParagraphTable", back_populates="surnames")

    def __init__(self, name, patronymic, surname):
        self.name = name
        self.patronymic = patronymic
        self.surname = surname


class SettingsTable(Base):
    __tablename__ = 'settings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    db_ip = Column(INET)
    db_port = Column(Integer)
    db_path = Column(VARCHAR(300))

    def __init__(self, db_ip, db_port, db_path):
        self.db_ip = db_ip
        self.db_port = db_port
        self.db_path = db_path


class DataBase:

    def try_connection(self) -> bool:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(3)
                sock.connect((self.server_ip, self.port))
            connection = self.__engine.connect()
            connection.close()
        except DatabaseError as e:
            e = repr(e)
            logger.debug(f'DataBase error: {e}')
            return False
        except socket.timeout as e:
            e = repr(e)
            logger.debug(f'SocketTimeout error: {e}')
            return False
        except Exception as e:
            e = repr(e)
            logger.debug(f'Unexpected error: {e}')
            return False
        return True

    def __init__(self, path2db, server_ip, port='5432', login='django', password='django'):
        self.port: int = int(port)
        self.server_ip = server_ip
        self.connect_string = f"postgresql+psycopg2://{login}:{password}@{server_ip}:{port}/{path2db}"
        self.__engine = create_engine(self.connect_string)
        self.session_master = sessionmaker(bind=self.__engine)

    def create_tables(self):
        Base.metadata.create_all(self.__engine)

    def __enter__(self):
        self.session = self.session_master()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    @staticmethod
    def __generation_numbers_requestion(numbers_list):
        numbers_requestion_list = []
        for number in numbers_list:
            numbers_requestion_list.append(PhonesTable(number))
        return numbers_requestion_list

    @staticmethod
    def __generation_personal_requestion(personal_list):
        personal_requestions_list = []
        for personal in personal_list:
            personal_requestions_list.append(SurnamesTable(personal['first'], personal['middle'], personal['last']))
        return personal_requestions_list

    def __generate_paragraph_list(self, paragraphs, number_map, persons_map):
        paragraph_list = []
        for item in range(0, len(paragraphs)):
            if len(number_map[item]) or len(persons_map[item]):
                paragraph = ParagraphTable(text=paragraphs[item])
                paragraph.telephones = self.__generation_numbers_requestion(number_map[item])
                paragraph.surnames = self.__generation_personal_requestion(persons_map[item])
                paragraph_list.append(paragraph)
            else:
                continue
        return paragraph_list

    def add_record(self, filename, filepath, status=document_status['process'], number_map=None, paragraphs=None,
                   persons_map=None, doc_date=None):
        if number_map is None:
            number_map = []
        if paragraphs is None:
            paragraphs = []
        if persons_map is None:
            persons_map = []
        document = DocumentsTable(filename=filename, path=filepath, status_id=status, date=doc_date)
        document.paragraphs = self.__generate_paragraph_list(paragraphs, number_map, persons_map)
        self.session.add(document)
        self.session.commit()

    def update_record(self, document_id, status, number_map, paragraphs, persons_map, doc_date):
        session = self.session_master()
        session.query(PARAGRAPH).filter(PARAGRAPH.doc_id == document_id).delete()
        document: DOCUMENTS = session.query(DOCUMENTS).get(document_id)
        document.date = doc_date
        document.paragraphs = self.__generate_paragraph_list(paragraphs, number_map, persons_map)
        document.status_id = status
        session.commit()
        session.close()

    def delete_record(self, document_id):
        session = self.session_master()
        session.query(DOCUMENTS).filter_by(id=document_id).delete()
        session.commit()
        session.close()

    def retrieving_numbers_information_integer(self, number_list_int, limit, offset=0):
        phone_view_list = list()
        number_int_string = ', '.join(str(item) for item in number_list_int)
        session = self.session_master()
        query_number = session.execute(
            f"""SELECT FIRST {limit} SKIP {offset} TELEPHONES."NUMBER", PARAGRAPH.TEXT, DOCUMENTS.FILENAME, DOCUMENTS.PATH2DOC, DOCUMENTS."Date" 
            from TELEPHONES 
            left join PARAGRAPH on PARAGRAPH.id = TELEPHONES.PARAGRAPH_ID 
            left join DOCUMENTS on DOCUMENTS.ID = PARAGRAPH.DOC_ID
            where TELEPHONES.NUMBER_INTEGER IN ({number_int_string}) and DOCUMENTS.STATUS_ID = 1
            group by TELEPHONES."NUMBER", PARAGRAPH.TEXT, DOCUMENTS.FILENAME, DOCUMENTS.PATH2DOC, DOCUMENTS."Date" 
            order by  DOCUMENTS."Date" desc """).fetchall()
        for number, text, filename, path, doc_date in query_number:
            if not isinstance(text, str):
                text = text.read()
            phone_view_list.append(
                PhoneView(number, text, filename, path, doc_date.strftime("%d.%m.%Y")))
        record_count = session.execute(
            f"""
            select count(*) 
            from (
            select TELEPHONES."NUMBER", PARAGRAPH.TEXT, DOCUMENTS.FILENAME, DOCUMENTS.PATH2DOC, DOCUMENTS."Date" 
            from TELEPHONES 
            left join PARAGRAPH on PARAGRAPH.id = TELEPHONES.PARAGRAPH_ID 
            left join DOCUMENTS on DOCUMENTS.ID = PARAGRAPH.DOC_ID
            where TELEPHONES.NUMBER_INTEGER IN ({number_int_string}) and DOCUMENTS.STATUS_ID = 1
            group by TELEPHONES."NUMBER", PARAGRAPH.TEXT, DOCUMENTS.FILENAME, DOCUMENTS.PATH2DOC, DOCUMENTS."Date"
            order by  DOCUMENTS."Date" desc
            ) t1
            """).fetchone()
        session.close()
        return phone_view_list, record_count[0]

    def get_personal_data(self, last_name, first_name, patronymic, limit, offset=0):
        personal_data_list = list()
        session = self.session_master()
        filter_string = f"""SURNAMES.SURNAME = '{last_name}'"""
        if first_name: filter_string = f"""{filter_string} and SURNAMES."NAME" = '{first_name}'"""
        if patronymic: filter_string = f"""{filter_string} and SURNAMES.PATRONYMIC = '{patronymic}'"""
        query_basis = f"""
        select first {limit} skip {offset}  SURNAMES."NAME", SURNAMES.PATRONYMIC, SURNAMES.SURNAME, PARAGRAPH.TEXT, DOCUMENTS.FILENAME, DOCUMENTS.PATH2DOC, DOCUMENTS."Date"
        from SURNAMES
        left join PARAGRAPH on PARAGRAPH.id = SURNAMES.PARAGRAPH_ID
        left join DOCUMENTS on DOCUMENTS.ID = PARAGRAPH.DOC_ID
        where {filter_string} and DOCUMENTS.STATUS_ID = 1
        group by SURNAMES."NAME", SURNAMES.PATRONYMIC, SURNAMES.SURNAME, PARAGRAPH.TEXT, DOCUMENTS.FILENAME, DOCUMENTS.PATH2DOC, DOCUMENTS."Date"
        order by  DOCUMENTS."Date" desc
        """
        query_personal_data = session.execute(query_basis).fetchall()
        for name, patronymic, surname, text, filename, filepath, doc_date in query_personal_data:
            if not isinstance(text, str):
                text = text.read()
            personal_data_list.append(
                PersonDataView(f'{surname} {name} {patronymic}', text, filepath,
                               filename, doc_date.strftime("%d.%m.%Y")))
        q_pers_data_count = f"""
        select count (*) from (
        select SURNAMES."NAME", SURNAMES.PATRONYMIC, SURNAMES.SURNAME, PARAGRAPH.TEXT, DOCUMENTS.FILENAME, DOCUMENTS.PATH2DOC, DOCUMENTS."Date"
        from SURNAMES
        left join PARAGRAPH on PARAGRAPH.id = SURNAMES.PARAGRAPH_ID
        left join DOCUMENTS on DOCUMENTS.ID = PARAGRAPH.DOC_ID
        where {filter_string} and DOCUMENTS.STATUS_ID = 1
        group by SURNAMES."NAME", SURNAMES.PATRONYMIC, SURNAMES.SURNAME, PARAGRAPH.TEXT, DOCUMENTS.FILENAME, DOCUMENTS.PATH2DOC, DOCUMENTS."Date"
        order by  DOCUMENTS."Date" desc ) t1
        """
        record_count = session.execute(q_pers_data_count).fetchone()
        session.close()
        return personal_data_list, record_count[0]

    def get_documents_by_status(self, status_array: dict, doc_id, limit, offset=0):
        session = self.session_master()
        doc_query = session.query(DOCUMENTS).join(DOCSTATUS).filter(DOCUMENTS.id > doc_id).filter(
            DOCSTATUS.status_name.in_(status_array.keys())).limit(limit).offset(offset).all()
        session.close()
        return doc_query

    def get_error_documents(self, limit, offset=0):
        session = self.session_master()
        error_documents = session.query(DOCUMENTS.id, DOCUMENTS.filename, DOCUMENTS.path2doc).join(
            DOCUMENTS.status).filter(DOCSTATUS.id > 1).limit(limit).offset(offset).all()
        session.close()
        return error_documents

    def test_select(self):
        session = self.session_master()
        result = session.execute('SELECT * FROM GET_DATA_BY_NUMBER(9803489928)').fetchall()
        documents = session.query(DOCUMENTS).all()
        paragraphs = session.query(PARAGRAPH).all()
        for document in documents:
            print(document.filename)
        for paragraph in paragraphs:
            print(paragraph.text)
        session.close()

    def test_insert(self):
        session = self.session_master()
        new_doc = DOCUMENTS('test.doc', '/home/gravity/Temp/test.doc', document_status['success'])
        session.add(new_doc)
        session.commit()
        session.close()

    def is_processed(self, filepath):
        session = self.session_master()
        status = session.query(session.query(DOCUMENTS).filter_by(path2doc=filepath).exists()).scalar()
        session.close()
        return status


if __name__ == '__main__':
    records_number_on_page = 5
    page = 1
    with DataBase('osa_extra', '127.0.0.1', '5432', 'django', 'django') as db:
        db.try_connection()
        db.add_record('123', '/mnt/123.txt')

    # db.create_tables()
    db.test_select()
    # db.test_insert()
    print(db.is_processed('1_2'))
    numbers_list = [9803489928, 5555555555]
    rezult = db.retrieving_numbers_information_integer(numbers_list, records_number_on_page, page)
    print(rezult)
    result = db.get_personal_data('КОВЫРШИН', '', '', records_number_on_page, 0)
    pass
