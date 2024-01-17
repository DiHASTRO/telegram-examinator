from . import models

u = models.User(1232422567, 3, 123)
u1 = models.User.get_user_by_id(1)
print(u1)
