#(Vezneler/Departmanlar): Müşteriyle muhatap olduğumuz yerdir. Eskiden tüm rotalar (GET, POST) tek bir yerdeydi. 
# Şimdi "Kullanıcı Kayıt Veznesi" (users.py) ayrı, "Görev Ekleme Veznesi" (tasks.py) ayrı çalışacak.

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.db.database import engine
from app.models.task import Task
from app.core.security import get_current_user_id


# Yönlendiriciyi oluşturuyoruz
router = APIRouter(prefix="/tasks", tags=["Tasks"])

# Veritabanı bağlantısı açıyoruz
def get_session():
    with Session(engine) as session:
        yield session


# POST
@router.post("/", response_model=Task)
def create_task(
    task_in: Task,
    session: Session = Depends(get_session),
    current_user_id: int = Depends(get_current_user_id) # kullanıcının biletini (JWT) okur ve id numarasını current_user_id değişkeninin içine koyar.
):
    # Görevi Kullanıcıya Bağlıyoruz
    task_in.user_id = current_user_id
    
    # Veritabanına Kaydediyrouz
    session.add(task_in)      # Görevi veritabanı listesine ekliyoruz
    session.commit()          # işlemi kesinleştirip kaydediyoruz
    session.refresh(task_in)  # son halini veritabanından geri çekiyoruz
    
    return task_in

#-----------------

# GET
@router.get("/", response_model=list[Task])
def get_tasks(
    session: Session = Depends(get_session),
    current_user_id: int = Depends(get_current_user_id)
):
    
    statement = select(Task).where(Task.user_id == current_user_id)   # Sadece user_id'si bu kişi olan görevleri getir
    
    tasks = session.exec(statement).all()   # Sorguyu çalıştırıp eşleşen tüm görevleri bir liste (all) olarak alıyoruz
    
    return tasks


#-----------------

# PUT
@router.put("/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    task_in: Task,
    session: Session = Depends(get_session),
    current_user_id: int = Depends(get_current_user_id)
):
    # Görevi veritabanında aricaz ama sadece bu kullanıcıya aitse bulucaz
    statement = select(Task).where(Task.id == task_id, Task.user_id == current_user_id)
    db_task = session.exec(statement).first()
    
    # Eğer görev yoksa veya başkasının göreviyse hata ver
    if not db_task:
        raise HTTPException(
            status_code=404, 
            detail="Görev bulunamadı veya bu görevi değiştirmeye yetkiniz yok."
            )

    # Kullanıcının gerçekten gönderdiği (boş bırakmadığı) verileri bir sözlüğe alıyoruz
    task_data = task_in.model_dump(exclude_unset=True)
    
    # Sadece gönderilen bu verileri eski görevin üzerine yazıyoruz
    for key, value in task_data.items():
        setattr(db_task, key, value)
    
    # Değişiklikleri kaydet
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    
    return db_task

#-----------------

# DELETE
@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    session: Session = Depends(get_session),
    current_user_id: int = Depends(get_current_user_id)
):
    # Kullanıcıya ait olan görevi bulur
    statement = select(Task).where(Task.id == task_id, Task.user_id == current_user_id)
    db_task = session.exec(statement).first()    


    # Görev yoksa veya yetkisi yoksa hata verir
    if not db_task:
        raise HTTPException(status_code=404, detail="Görev bulunamadı veya silmeye yetkiniz yok.")

    
    session.delete(db_task)
    session.commit()
        
    return {"message": f"Görev {task_id} başarıyla silindi."} 

