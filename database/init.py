import random
from dataclasses import dataclass

from sqlalchemy.exc import IntegrityError

from database import Category, Session, Item, User, Favourite, Base, engine


def main():
    @dataclass
    class CategoryInit:
        name: str  # label
        value: str  # value
        id: int = None

    @dataclass
    class ItemInit:
        name: str
        description: str
        image_url: str
        price: float
        category: str  # label for category
        on_sale: bool = False
        id: int = None
        category_id: int = None

    @dataclass
    class UserInit:
        first_name: str
        last_name: str
        email: str
        password_hash: str
        id: int = None

    @dataclass
    class FavoriteInit:
        item_name: str  # Item.name
        user_email: str  # User.email
        user_id: int = None
        item_id: int = None
        id: int = None

    categories: [CategoryInit] = [
        CategoryInit(value="nft", name="NFT"),
        CategoryInit(value="learning", name="Learning"),
        CategoryInit(value="programming", name="Programming")
    ]

    items: [ItemInit] = [
        ItemInit(
            name="First Product",
            description="First product description.",
            image_url="https://dummyimage.com/450x300/dee2e6/6c757d.jpg",
            on_sale=False,
            price=80.0,
            category="nft"
        ),
        ItemInit(
            name="Second Product",
            description="Second product description.",
            image_url="https://dummyimage.com/450x300/dee2e6/6c757d.jpg",
            on_sale=False,
            price=40.0,
            category="programming"
        ),
        ItemInit(
            name="Third Product",
            description="Third product description.",
            image_url="https://dummyimage.com/450x300/dee2e6/6c757d.jpg",
            on_sale=False,
            price=40.0,
            category="learning"
        ),
        ItemInit(
            name="Fourth Product",
            description="Fourth product description.",
            image_url="https://dummyimage.com/450x300/dee2e6/6c757d.jpg",
            on_sale=False,
            price=40.0,
            category="learning"
        ),
        ItemInit(
            name="Fifth Product",
            description="Fifth product description.",
            image_url="https://dummyimage.com/450x300/dee2e6/6c757d.jpg",
            on_sale=False,
            price=40.0,
            category="programming"
        ),
        ItemInit(
            name="Sixth Product",
            description="Sixth product description.",
            image_url="https://dummyimage.com/450x300/dee2e6/6c757d.jpg",
            on_sale=False,
            price=40.0,
            category="programming"
        ),
        ItemInit(
            name="Seventh Product",
            description="Seventh product description.",
            image_url="https://dummyimage.com/450x300/dee2e6/6c757d.jpg",
            on_sale=False,
            price=40.0,
            category="nft"
        ),
    ]

    users: [UserInit] = [
        UserInit(
            first_name="Dima",
            last_name="Dzundza",
            email="dzundzadima@gmail.com",
            password_hash="dimadzundza123",
        ),
        UserInit(
            first_name="John",
            last_name="Smith",
            email="johnsmith@gmail.com",
            password_hash="johnsmith123"
        ),
        UserInit(
            first_name="Emma",
            last_name="Johnson",
            email="emmajohnson@gmail.com",
            password_hash="emmajohnson123"
        ),
        UserInit(
            first_name="Alex",
            last_name="Wilson",
            email="alexwilson@gmail.com",
            password_hash="alexwilson123"
        ),
        UserInit(
            first_name="Sarah",
            last_name="Davis",
            email="sarahdavis@gmail.com",
            password_hash="sarahdavis123"
        ),
        UserInit(
            first_name="Michael",
            last_name="Lee",
            email="michaellee@gmail.com",
            password_hash="michaellee123"
        ),
        UserInit(
            first_name="Emily",
            last_name="Rodriguez",
            email="emilyrodriguez@gmail.com",
            password_hash="emilyrodriguez123"
        )
    ]

    favorites: [FavoriteInit] = []
    for user_ in users:
        selected_items: [ItemInit] = random.sample(items, random.randint(0, len(items)))
        for selected_item in selected_items:
            favorites.append(
                FavoriteInit(item_name=selected_item.name, user_email=user_.email)
            )

    print(favorites)
    # favorites: [FavoriteInit] = [
    #     FavoriteInit(item_name="First Product", user_email="dzundzadima@gmail.com"),
    #     FavoriteInit(item_name="Second Product", user_email="dzundzadima@gmail.com"),
    #     FavoriteInit(item_name="Fourth Product", user_email="dzundzadima@gmail.com"),
    #     ###
    #     FavoriteInit(item_name="First Product", user_email="johnsmith@gmail.com"),
    #     FavoriteInit(item_name="Fifth Product", user_email="johnsmith@gmail.com"),
    #     FavoriteInit(item_name="Sixth Product", user_email="johnsmith@gmail.com"),
    #     FavoriteInit(item_name="Seventh Product", user_email="johnsmith@gmail.com"),
    #     ###
    #     FavoriteInit(item_name="First Product", user_email="dzundzadima@gmail.com"),
    #     FavoriteInit(item_name="Second Product", user_email="dzundzadima@gmail.com"),
    #     FavoriteInit(item_name="Fourth Product", user_email="dzundzadima@gmail.com"),
    # ]

    def init_categories():
        session = Session()
        for category_init in categories:
            try:
                category = Category(name=category_init.name, value=category_init.value)
                session.add(category)
                session.commit()
                session.refresh(category)
            except IntegrityError:
                session.rollback()
                print(f"Category integrity Error at name={category_init.name}, value={category_init.value}")
                category = session.query(Category).filter_by(name=category_init.name).first()
            category_init.id = category.id

        session.close()

    def init_items():
        session = Session()
        for item_init in items:
            category_id, = session.query(Category.id).filter_by(value=item_init.category).first()
            try:
                item = Item(
                    name=item_init.name,
                    description=item_init.description,
                    image_url=item_init.image_url,
                    category_id=category_id,
                    on_sale=item_init.on_sale,
                    price=item_init.price
                )
                session.add(item)
                session.commit()
                session.refresh(item)
            except IntegrityError:
                session.rollback()
                print(f"Item integrity Error at name={item_init.name}")
                item = session.query(Item).filter_by(name=item_init.name).first()

            item_init.id = item.id

        session.close()

    def init_users():
        session = Session()
        for user_init in users:
            try:
                user = User(
                    first_name=user_init.first_name,
                    last_name=user_init.last_name,
                    email=user_init.email,
                    password_hash=user_init.password_hash
                )
                session.add(user)
                session.commit()
                session.refresh(user)
            except IntegrityError:
                session.rollback()
                print(f"User integrity Error at email={user_init.email}")
                user = session.query(User).filter_by(email=user_init.email).first()

            user_init.id = user.id

        session.close()

    def init_favorites():
        session = Session()
        for favorite_init in favorites:
            # get user_id
            user_id, = session.query(User.id).filter_by(email=favorite_init.user_email).first()
            favorite_init.user_id = user_id

            # get item_id
            item_id, = session.query(Item.id).filter_by(name=favorite_init.item_name).first()
            favorite_init.item_id = item_id
            try:
                favorite = Favourite(
                    user_id=favorite_init.user_id,
                    item_id=favorite_init.item_id,
                )
                session.add(favorite)
                session.commit()
                session.refresh(favorite)
            except IntegrityError:
                session.rollback()
                print(f"Favorite integrity Error at user_id={favorite_init.user_id}, item_id={favorite_init.item_id}")
                favorite = session.query(Favourite).filter_by(
                    user_id=favorite_init.user_id,
                    item_id=favorite_init.item_id
                ).first()

            favorite_init.id = favorite.id

        session.close()

    def init_db():
        init_categories()
        init_items()
        init_users()
        init_favorites()

    init_db()


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    main()
