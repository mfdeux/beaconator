from sqlalchemy.orm import Session

from . import models, schemas


def get_ga_codes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.GACode).offset(skip).limit(limit).all()


def get_ga_code(db: Session, id: int):
    return db.query(models.GACode).filter(models.GACode.id == id).first()


def delete_ga_code(db: Session, id: int):
    returned = db.query(models.GACode).filter(models.GACode.id == id).delete()
    db.commit()
    return returned


def create_ga_code(db: Session, item: schemas.GACodeChange):
    db_item = models.GACode(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_ga_code(db: Session, id: int, item: schemas.GACodeChange):
    returned = (
        db.query(models.GACode).filter(models.GACode.id == id).update(item.dict())
    )
    db.commit()
    return returned


def get_properties(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Property).offset(skip).limit(limit).all()


def get_property(db: Session, id: int):
    return db.query(models.Property).filter(models.Property.id == id).first()


def get_property_by_code(db: Session, code: str):
    return db.query(models.Property).filter(models.Property.code == code).first()


def create_property(db: Session, item: schemas.PropertyChange):
    db_item = models.Property(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_property(db: Session, id: int, item: schemas.PropertyChange):
    returned = (
        db.query(models.Property).filter(models.Property.id == id).update(item.dict())
    )
    db.commit()
    return returned


def delete_property(db: Session, id: int):
    returned = db.query(models.Property).filter(models.Property.id == id).delete()
    db.commit()
    return returned
