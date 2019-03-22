from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item, User

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

User1 = User(name="Tom Jones", email="tom@tomjones.com")
session.add(User1)
session.commit()

category1 = Category(name = "Soccer")
session.add(category1)
session.commit()

item1 = Item(name = "Ball", description = "An inflated ball used in playing soccer", category = category1, user_id=1)
session.add(item1)
session.commit()

item2 = Item(name = "Cleats", description = "Football boots, called cleats or soccer shoes in North America, are an item of footwear worn when playing football. Those designed for grass pitches have studs on the outsole to aid grip.", category = category1, user_id=1)
session.add(item2)
session.commit()

item3 = Item(name = "Goal", description = "A net", category = category1, user_id=1)
session.add(item3)
session.commit()

item4 = Item(name = "Jersey", description = "A shirt", category = category1, user_id=1)
session.add(item4)
session.commit()

category2 = Category(name = "Basketball")
session.add(category2)
session.commit()

category3 = Category(name = "Baseball")
session.add(category3)
session.commit()

item1 = Item(name = "Baseball", description = "The ball used in baseball", category = category3, user_id=1)
session.add(item1)
session.commit()

item2 = Item(name = "Bat", description = "A long wooden or metal bat used to hit a baseball.", category = category3, user_id=1)
session.add(item2)
session.commit()

category4 = Category(name = "Frisbee")
session.add(category4)
session.commit()

category5 = Category(name = "Snowboarding")
session.add(category5)
session.commit()

category6 = Category(name = "Rock Climbing")
session.add(category6)
session.commit()

category7 = Category(name = "Football")
session.add(category7)
session.commit()

category8 = Category(name = "Skating")
session.add(category8)
session.commit()

category9 = Category(name = "Hockey")
session.add(category9)
session.commit()

print ("Complete.  Database populated.")
