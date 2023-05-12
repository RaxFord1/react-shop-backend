from database.database import Item, Base, Category


class ItemView(Base):
    __table__ = (
        # Join the item and category tables on category_id
        Item.__table__.join(Category.__table__)
        .select()
        .with_only_columns([Item.__table__.c, Category.name.label('category_name'), Category.value.label('category_value')])
        .alias()
    )
