from fastapi import HTTPException


def check_item(item_id: int, itemModel, itemstr: str, db):
    item = db.query(itemModel).filter(itemModel.id == item_id).first()
    if item:
        return item
    raise HTTPException(status_code=404, detail=f"{itemstr} not found")

