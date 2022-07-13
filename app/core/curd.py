from fastapi import HTTPException


def check_item(item_id: int, itemModel, itemstr: str, db):
    item = db.query(itemModel).filter(itemModel.id == item_id).first()
    if item:
        return item
    raise HTTPException(status_code=404, detail=f"{itemstr} not found")


def upsert(itemModel, identifier: dict, update_data: dict, db):
    item = db.query(itemModel).filter_by(**identifier).first()
    identifier.update(update_data)
    if item:
        db.query(itemModel).filter_by(**identifier).update(identifier)
    else:
        item = itemModel(**identifier)
        db.add(item)
        
    db.commit()
    db.refresh(item)
    return item
