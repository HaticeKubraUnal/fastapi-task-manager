# Kullanıcıyla muhatap olduğumuz yerdir. Eskiden tüm rotalar (GET, POST) tek bir yerdeydi. 
# Şimdi "Kullanıcı Kayıt Veznesi" (users.py) ayrı, "Görev Ekleme Veznesi" (tasks.py) ayrı çalışacak.
# Burası tüm dosyaların birleştiği yerdir.

# Kullanıcı Kayıt Veznesi

from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session, select
from fastapi.security import OAuth2PasswordRequestForm

# Diğer sayfalardan çağırdıklarımız:
from app.db.database import engine, SessionDep
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.core.security import get_password_hash, verify_password, create_access_token


# FastAPI'de tüm API endpointlerini tek bir dosyada (main.py) toplamak yerine bu dosyadaki 
# tüm URL'lerin başına otomatik olarak /users ekler ve tüm işlemler Users listesinde toplanır.
router = APIRouter(prefix="/users", tags=["Users"])


# Kayıt işlemi
@router.post("/register", response_model=UserResponse)    # Kullanıcı buraya ulaşmak için tarayıcıda .../users/register adresine gider ve orada kaşısına UserResponse şablonu çıkar.
def register_user(user_in: UserCreate, session: SessionDep):    # Kullanıcıdan gelen kayıt formudur. İçinde sadece email ve password vardır. Ayırca veritabanı bağlantısı açar.
    
    # SQLModel kullanarak bir SQL SELECT sorgusu oluşturuyoruz.
    statement = select(User).where(User.email == user_in.email)    # User tablosunda bu e-posta adresi var mı yok mu?
    existing_user = session.exec(statement).first()    # Sorguyu veritabanında çalıştırır (exec) ve dönen ilk sonucu alır. Eğer eşleşme yoksa sonuç None döner.
    
    if existing_user:   # None değilse;
        raise HTTPException(status_code=400, detail="Bu e-posta zaten kullanımda.")
    # Daha önce sisteme kayıt olunmuş bir e-posta ile tekrar kayıt olunmaya çalışılırsa hata veriyor.
    
    # Kullanıcının şifresini alıp bcrypt algoritmasıyla hash formatına çevirir
    hashed_pw = get_password_hash(user_in.password)
    
    # User tablosunda new_user nesnesi oluşturup; kullanıcının mailini ve hashlenmiş şifresini oraya yazar.
    new_user = User(email=user_in.email, hashed_password=hashed_pw)
    
    session.add(new_user)       # Yeni nesneyi geçici olarak veritabanı oturumuna session'a ekler
    session.commit()            # SQL INSERT komutunu çalıştırır ve veriyi veritabanına kalıcı olarak kaydeder.
    session.refresh(new_user)   # commmit işlemi gerçekleştiğinde veritabanı otomatik bir id atar ve refresh komutuyla değişken güncellenir.
    
    # Kullanıcıya başarıyla kayıt olduğunu gösterir
    return new_user

#---------------------------------------------------------------------


# --- Veritabanı Kapıcısı ---
def get_session():
    with Session(engine) as session:
        yield session


# Gişiş İşlemi
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    # form_data.username, senin kilit ekranına yazdığın e-postayı temsil eder
    user = session.exec(select(User).where(User.email == form_data.username)).first()
    
    # Eski doğrulama mantığımız aynen kalıyor
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Hatalı e-posta veya şifre")
    
    # Kimlik doğrulandı! Kullanıcı ID'si ile JWT üret
    access_token = create_access_token(data={"sub": str(user.id)})  # int olan id 'yi metine çeviriyoruz. ve makinemiz son tarih basıp paetliyor.
    
    return {"access_token": access_token, "token_type": "bearer"}
    # BUrada {} ler Kullanıcıya göndereceğimiz kargo kutusunu (JSON paketini) temsil eder.
    # Pakete; ürettiğimiz uzun şifreyi koyuyoruz ve bearer kısmıyla şunu diyoruz: Bunu üzerinde taşıyan pakete kimlik sorma doğrudan içeri al.



