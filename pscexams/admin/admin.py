
# Register your models here.

from django.contrib import admin
from pscexams.admin.models import *

admin.site.register(State)
admin.site.register(Exam)
admin.site.register(Subject)
admin.site.register(Topics)
admin.site.register(Question)