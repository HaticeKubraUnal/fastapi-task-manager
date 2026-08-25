#(Kasa ve Güvenlik Odası): Projenin beynidir. JWT Token üretildiği,
# şifrelerin kırılmaz hale (hash) getirildiği çok gizli güvenlik mekanizmaları bu odada yer alır.

from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from app.core.config import settings

# ... -> str = çalışması bittiğinde sonuç olarak string çıkacak.
# ... -> bool = çalışması bittiğinde sonuç olarak boolean çıkacak. ...

# 1. ŞİFRELEME AYARLARI
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")   # pwd_context adında bir makinemiz var ve bcrypt şifrelemesi kullanıyor. Ayrıca eski bir sistem varsa bunu otomatik yeniliyor.

def get_password_hash(password: str) -> str:
    # Kullanıcının girdiği düz şifreyi karmaşık bir koda çevirir.
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Giriş yaparken girilen şifre ile veritabanındaki karmaşık şifre eşleşiyor mu diye bakar.
    return pwd_context.verify(plain_password, hashed_password)


# 2. JWT AYARLARI
# Token = Kullanıcı her görev eklediğinde veya sildiğinde şifre sormayız. Girişte ona bir "Token" veririz ve sistemde dolaşırken bunu kullanır.
# JWT (JSON Web Token) = Token'in akıllı halidir.
# Bu bilekliğin (JWT'nin) üzerinde şunlar yazar: 
#           Kime ait olduğu, 
#           Bitiş süresi, 
#           Gizli Mühür (İmza) - sahtelik kontrolü


SECRET_KEY = "super_secret_key_123"     # Mühürdür - Gerçekte bu şifre .env dosyasında gizlenir!
ALGORITHM = "HS256"                     # Mührü basarken kullandığımız makinenin/matematiğin adıdır.
ACCESS_TOKEN_EXPIRE_MINUTES = 30        # Geçerlilik süresi (30 dakika)

# Token'i oluşturan fonksiyon
def create_access_token(data: dict) -> str:
    to_encode = data.copy()     # Orijinal veriyi yedekleriz ve to_encode paketine koyarız
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)    # Şuanki saate geçerlilik süresini ekleyip bitiş süresini hesaplar
    to_encode.update({"exp": expire})   # Paketimize hesapladığımız bitiş tarihini yazar.

    # Her şeyin birleştiği paketleme motorudur.
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)    # encoded_jwt = to_encode + SECRET_KEY + ALGORITHM   ->  Tüm bunları tek bir pakette birleştirir.
    return encoded_jwt



# FastAPI'ye tokenlerin nereden dağıtıldığını söylüyoruz
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login") # Bir uygulama korumalı bir işlem yapmak istediğinde (örneğin görev eklemek), isteğin "HTTP Header" (Başlık) kısmına bir token koymak zorundadır. Bu kod, o başlıkta Bearer kelimesiyle başlayan token'ı arayıp bulma işini otomatik yapar.

def get_current_user_id(token: str = Depends(oauth2_scheme)): # Depends(...) -> istemcinin başlığından gelen token'ı metin (str) olarak alıp buradaki token değişkeninin içine koyar.

    # Kullanıcının getirdiği token'i okur, geçerliyse içindeki ID numarasını (sub) geri verir.

    try: # Kod düzgün çalışıyorsa buraya girer.

        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm]) # Daha önce jwt.encode ile kilitlediğimiz veriyi, şimdi jwt.decode ile aynı gizli şifreyi kullanarak geri açıyoruz.

        user_id_str: str = payload.get("sub") # "sub" etiketiyle koyduğumuz kullanıcı ID'sini çıkarıyoruz.
        
        if user_id_str is None: # Paketin şifresi çözülse bile içinde "sub" verisi yoksa işlemi iptal edip hata gönderiyoruz.
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Biletin içinde kimlik bilgisi yok."
            )
            
        return int(user_id_str) # JWT standartları gereği veriyi metin olarak koymuştuk ("1") Veritabanındaki id formatımız integer olduğu için, int() fonksiyonuyla bunu tekrar 1 sayısına çevirip geri döndürüyoruz.
        
    except jwt.PyJWTError: # Kod bozuksa direkt buraya atlar.
        raise HTTPException( # Bilet sahteyse, süresi dolmuşsa veya bozuksa anında hata verir
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Geçersiz veya süresi dolmuş bilet."
        )


    