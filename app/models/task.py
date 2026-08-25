#(Arka Depo/SQLModel): Veritabanındaki "fiziksel" raflarımızdır. Verilerin arka planda nasıl saklanacağını belirleriz. Kullanıcılar bu depoyu asla göremez.


from sqlmodel import SQLModel, Field

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)      # id yapılan görevin numarası, user_id kimin o görevi yaptığı
    title: str = Field(index=True)
    description: str | None = Field(default=None)
    is_completed: bool = Field(default=False)       # yeni eklenen bir görev henüz bitmemiştir, bu yüzden varsayılan olarak False atadık. Kullanıcı görevi bitirince bunu True yapıcaz.
    
    user_id: int = Field(foreign_key="user.id")     # Burası görev tablosu ve Kullanıcı tablosundaki id buraya user_id olarak foreign key olarak getirilmiş.


