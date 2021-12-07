from fastapi.encoders import jsonable_encoder


def get_updated_obj(db_obj, update_body):
    obj_data = jsonable_encoder(db_obj)
    if isinstance(update_body, dict):
        update_data = update_body
    else:
        update_data = update_body.dict(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    return db_obj
