from . import models

u = models.User(1232422567, 3, 123)
u1 = models.User.get_user_by_tg_user_id(1234)
print(u1)
