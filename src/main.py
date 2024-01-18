from . import models

import logging

s = models.Subject.get_by_id(8)
print(s)
print(s.owner_user)
