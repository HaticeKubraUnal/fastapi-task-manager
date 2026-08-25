from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlmodel import SQLModel
from app.db.database import engine
from app.routers import users, tasks

# 1. Ana Uygulamayı Oluştur
app = FastAPI(title="Görev Yöneticisi API")


# Dışarıdan gelen tarayıcı bağlantılarına izin veren ayardır
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Geliştirme aşamasında her yerden gelen isteği kabul et
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE hepsine izin ver
    allow_headers=["*"],
)


# 2. Uygulama Başlarken Veritabanı Tablolarını Kur
@app.on_event("startup")    # Terminalde komutu yazıp Enter'a bastığım an hemen altındaki fonksiyonu sadece bir kere çalıştır.
def on_startup():
    SQLModel.metadata.create_all(engine)    # models klasöründe yazdığımız User ve Task tablolarına bak. Eğer veritabanı dosyasında bu tablolar henüz yoksa, onları sıfırdan oluştur.

# .metadata: Bu, SQLModel'in hafızasında tuttuğu otomatik bir katalogdur. 
# Biz kodumuzun herhangi bir yerinde table=True diyerek bir sınıf oluşturduğumuzda, 
# SQLModel bunu anında algılar ve adını bu metadata kataloğuna yazar.

# .create_all(engine): Bu komut, az önce bahsettiğimiz kataloğu eline alır. 
# İçindeki her bir tablo ismi için SQLite veritabanı engine'e standart bir SQL komutu gönderir. 
# CREATE TABLE IF NOT EXISTS user ... (Eğer 'user' adında bir tablo yoksa oluştur)

# 3. Vezneleri Ana Binaya Kaydet
app.include_router(users.router)    # users.py dosyasının içinde tanımladığımız tüm API endpoint'leri, yani /register ve /login rotalarını ana uygulamamıza (FastAPI) entegre eder.
app.include_router(tasks.router)    # tasks.py dosyasının içinde tanımladığımız tüm API endpoint'leri, yani /register ve /login rotalarını ana uygulamamıza (FastAPI) entegre eder.


# Frontend Kısmı
@app.get("/", response_class=FileResponse)
def serve_frontend():
    # frontend klasöründeki index.html dosyasını tarayıcıya gönder
    return "frontend/index.html"


#------------------------------------------------------------------------------------------
# 1. main.py sistemi başlatır ve gelen isteği routers'a gönderir.
# 2. routers, gelen veriyi schemas ile kontrol edip süzer.
# 3. Eğer güvenlik/şifre işlemi varsa core altındaki araçlar kullanılır.
# 4. Süzülmüş ve güvenli veri, models kalıplarına sokulur.
# 5. Son olarak db aracılığıyla SQLite veritabanına kalıcı olarak yazılır.
# 6. İşlem bittiğinde aynı yol tersten izlenerek frontend'e "İşlem Başarılı" yanıtı döner.
#------------------------------------------------------------------------------------------

