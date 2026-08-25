from sqlmodel import SQLModel, Session, create_engine
from typing import Annotated
from fastapi import Depends

sqlite_file_name = "task_manager.db"            # Veritabanı ismi
sqlite_url = f"sqlite:///{sqlite_file_name}"    # Veritabanı yeri

connect_args = {"check_same_thread": False}     # Multithred kullanım
engine = create_engine(sqlite_url, connect_args=connect_args)     # Kod ve veritabanı arasındaki bağlantı

def create_db_and_tables():                     # .metadata = kullanıcının oluşturduğu tabloların yazıldığı yer(kroki)
    SQLModel.metadata.create_all(engine)        # krokileri al, engine'i çalıştır ve tüm krokileri veritabanına fiziksel olarak inşa et

def get_session():
    with Session(engine) as session:            # engine'i kullanarak bir session aç - (with: işim bitince burayı otomatik olarak kapat ve temizle)
        yield session                           # session şimdilik FastAPI ye verir. İstek bitene kadar bekler, işlem bitince de kapıyı kilitler.

SessionDep = Annotated[Session, Depends(get_session)]       # İleride herhangi bir yere SessionDep yazarsak; bunun bir Session olduğunu anla. 
                                                            # Yanındaki Depends notunu da oku ve bana veritabanı kapısını o şekilde aç."

                                                            