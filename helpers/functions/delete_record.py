from fastapi import HTTPException
from models.models import User


def check_user_permissions(user, db):
    #Hacemos la consulta del user en la BD
    user_data = db.query(User).filter(User.user == user).first()
    """
    Verifica si el usuario tiene el rol necesario para realizar la operación.
    """
    if user_data.role == 'user':
        raise HTTPException(status_code=403, detail="Permiso denegado")
    else:
        return user_data.role

def delete_record(record, db, id):
    """
    Elimina un registro de la base de datos.
    """
    db.delete(record)
    db.commit()
    return {"message": f"Se procede a eliminar el registro {id} de la base de datos"}

def deactivate_record(record, db, id):
    """
    Desactiva un registro estableciendo su estado a False.
    """
    record.status = False
    db.commit()
    return {"message": f"Se procede a dar de baja al registro {id} en la base de datos"}

def get_record_by_id(model, id, db):
    """
    Obtiene un registro por su ID desde la base de datos.
    """
    return db.query(model).filter(model.id == id).first()