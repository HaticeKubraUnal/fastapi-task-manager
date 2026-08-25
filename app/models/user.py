#(Arka Depo/SQLModel): Veritabanındaki "fiziksel" raflarımızdır. Verilerin arka planda nasıl saklanacağını belirleriz. Kullanıcılar bu depoyu asla göremez.


from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = Field(default=True)       # Bir kullanıcı hesabını dondurmak istediğinde bunu false yaparız böylece hesabını silmemiş oluruz.


    