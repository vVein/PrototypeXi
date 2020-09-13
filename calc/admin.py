from django.contrib import admin
from .models import Structures
from .models import Pipes
from .models import Project
from .models import Generic_Structures

# Register your models here.

admin.site.register(Structures)
admin.site.register(Pipes)
admin.site.register(Project)
admin.site.register(Generic_Structures)
