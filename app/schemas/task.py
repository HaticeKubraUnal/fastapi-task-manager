#(Ön Vitrin/Pydantic): Güvenlik filtresidir. Kullanıcıdan veri gelirken veya veri giderken nelerin gösterilip nelerin gizleneceğini burada belirleriz. 
# Mesela veritabanından veri çıkarken "Şifreyi gizle, sadece e-postayı göster" kuralını buraya yazarız.

from pydantic import BaseModel

class TaskCreate(BaseModel):    # Kullanıcı yeni bir görev eklerken
    title: str
    description: str | None = None  # Kullanıcı burada seçim yapmak sorunda -> ya bir şey yazacak/seçecek ya da boş bırak seçecek.

class TaskResponse(BaseModel):  # Kullanıcı "Görevlerimi listele" dediğinde
    id: int
    title: str
    description: str | None   # Kullanıcı burada ister seçim yapar ister tamamen görmezden gelip boş bırakabilir. Sistem otomatik none doldurur.
    is_completed: bool
    user_id: int




# JSON None=none                                JSON None
# {                                             {
#   "title": "Market Alışverişi",                   "title": "Market Alışverişi"
#   "description": null                         }
# }


