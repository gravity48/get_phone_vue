import socket
from datetime import datetime
from enum import Enum
from typing import Union
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, Text, Column, ForeignKey, VARCHAR, BigInteger, DateTime
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.orm import relationship, sessionmaker


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


class DocumentStatus(Enum):
    SUCCESS = 1
    TIMEOUT = 2
    UNICODE = 3
    UNEXPECTED = 4
    PROCESS = 5
    NOT_FOUND = 6
    UNDERWAY = 7


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
    date = Column(DateTime, nullable=True)
    status = relationship("DocStatusTable", back_populates="document")
    paragraphs = relationship("ParagraphTable", back_populates="document", cascade='all, delete')

    def __init__(self, filename: str, filepath: str, status_id: int, date: Union[datetime, None]):
        self.filename = filename
        self.filepath = filepath
        self.status_id = status_id
        self.date = date

    pass


class ParagraphTable(Base):
    __tablename__ = 'paragraphs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    doc_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"))
    text = Column(Text)
    document = relationship("DocumentsTable", back_populates="paragraphs")

    telephones = relationship("PhonesTable", back_populates="paragraph", cascade='all, delete')
    surnames = relationship("SurnamesTable", back_populates="paragraph", cascade='all, delete')

    def __init__(self, text):
        self.text = text.replace("\x00", "\uFFFD")

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
        self.name = name.replace("\x00", "\uFFFD")
        self.patronymic = patronymic.replace("\x00", "\uFFFD")
        self.surname = surname.replace("\x00", "\uFFFD")


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


class SqlBase:
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

    def __init__(self, session):
        self.session = session

    def add_record(self, filename, filepath, doc_date=None, status=DocumentStatus.UNDERWAY.value, number_map=None,
                   paragraphs=None,
                   persons_map=None):
        if number_map is None:
            number_map = []
        if paragraphs is None:
            paragraphs = []
        if persons_map is None:
            persons_map = []
        document = DocumentsTable(filename=filename, filepath=filepath, status_id=status, date=doc_date)
        document.paragraphs = self.__generate_paragraph_list(paragraphs, number_map, persons_map)
        self.session.add(document)
        self.session.commit()
        return document.id

    def remove_document(self, doc_id):
        self.session.query(DocumentsTable).filter(DocumentsTable.id == doc_id).delete()
        self.session.commit()

    def get_doc_data(self, record_id):
        document = self.session.get(DocumentsTable, record_id)
        return document.filename, document.filepath

    def update_record(self, document_id, status, number_map, paragraphs, persons_map, doc_date):
        self.session.query(ParagraphTable).filter(ParagraphTable.doc_id == document_id).delete()
        self.session.commit()
        document = self.session.get(DocumentsTable, document_id)
        document.date = doc_date
        document.paragraphs = self.__generate_paragraph_list(paragraphs, number_map, persons_map)
        document.status_id = status
        self.session.commit()

    def update_status(self, id_, status):
        document = self.session.get(DocumentsTable, id_)
        document.status_id = status
        self.session.commit()

    def get_document_by_filter(self, filter_: dict) -> int:
        query_basis = self.session.query(DocumentsTable.id)
        query_basis = query_basis.filter(DocumentsTable.status_id.in_(filter_['doc_status']))
        query_basis = query_basis.filter(DocumentsTable.id > filter_['id'])
        result = query_basis.order_by(DocumentsTable.id).first()
        if result is not None:
            return result[0]
        return 0

    def is_processed(self, filepath) -> bool:
        status = self.session.query(
            self.session.query(DocumentsTable).filter_by(filepath=filepath).exists()).scalar()
        return status


class DataBasesInterface:
    sql_ = SqlBase

    def __init__(self, host, port, connection_string):
        self.connection_string = connection_string
        self.host = host
        self.port = port

    def _try_connect_engine(self):
        engine = create_engine(self.connection_string)
        try:
            connection = engine.connect()
            connection.close()
        finally:
            engine.dispose()

    def try_connection(self) -> bool:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(3)
                sock.connect((self.host, self.port))
            self._try_connect_engine()
            return True
        except Exception:
            return False

    def __enter__(self):
        self.__engine = create_engine(self.connection_string)
        self.session_master = sessionmaker(bind=self.__engine)
        self.session = self.session_master()
        return self.__class__.sql_(self.session)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        self.__engine.dispose()


class PostgresDB(DataBasesInterface):

    def __init__(self, db_path, db_host, db_port='5432', db_login='django', db_password='django', *args, **kwargs):
        self.port: int = int(db_port)
        self.server_ip = db_host
        self.connection_string = f"postgresql+psycopg2://{db_login}:{db_password}@{db_host}:{db_port}/{db_path}"
        super().__init__(self.server_ip, self.port, self.connection_string)


class DataBase:
    instance: DataBasesInterface = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            raise NotImplementedError
        return cls.instance

    @classmethod
    def init_postgres_db(cls, *args, **kwargs):
        cls.instance = PostgresDB(*args, **kwargs)
