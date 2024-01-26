from .orm import models

import logging

user = models.User(123)
user.save()
s = models.Subject("Math", user.id)
print(s)
print(s.owner_user)
