from django.db import models
from django.contrib.auth.models import User

import json

class Account(models.Model):
    """
    from django.db import models
    from django.contrib.auth.models import User
    from postmaker.models import Publics
    142223503, 124367984, 124367240
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=100, null=True, blank=True)
    publics = models.CharField(max_length=500, null=True, blank=True)

    def stringalize(self, publics):
        self.publics = json.dumps(publics)

    def destringalize(self):
        return json.loads(self.publics)

    def get_clear_pubs(self):
        publics = self.publics[1:]
        publics = publics[:-1]
        return publics
