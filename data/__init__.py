# Database functions import:
from sqlalchemy.orm import relationship

from data.companies import *
from data.db_session import *
from data.items import *
from data.types import *
from data.users import *

Item.companies = relationship(Company, order_by=Company.name)
Item.types = relationship(Type, order_by=Type.name)
Item.item_creators = relationship(User, order_by=User.login)

Type.types = relationship(Item, order_by=Item.type)
Type.type_creators = relationship(User, order_by=User.login)

User.item_creators = relationship(Item, order_by=Item.creator)
User.type_creators = relationship(Type, order_by=Type.creator)
User.company_creators = relationship(Company, order_by=Company.creator)

Company.company_creators = relationship(User, order_by=User.login)
