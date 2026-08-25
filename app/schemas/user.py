#(Ön Vitrin/Pydantic): Güvenlik filtresidir. Kullanıcıdan veri gelirken veya veri giderken nelerin gösterilip nelerin gizleneceğini burada belirleriz. 
# Mesela veritabanından veri çıkarken "Şifreyi gizle, sadece e-postayı göster" kuralını buraya yazarız.


from pydantic import BaseModel, EmailStr    # BaseModel = Pydantic kütüphanesinin "Şablon" oluşturma aracıdır
                                            # Emailstr = @ var mı yada alan adı geçerli mi diye kontrol eder. Hatalıysa otomatik hata gönderir.

# kullanıcıya sunulan ondan girmesini istediğimiz şeyler (yani mesela kullanıcı kendi id'sini girmez.)

class UserCreate(BaseModel):    # Kullanıcıdan kayıt olurken alınacak bilgiler
    email: EmailStr
    password: str

class UserResponse(BaseModel):  # Kullanıcı profiline bakınca göreceği şeyler
    id: int
    email: EmailStr
    is_active: bool     # Aktiflik


