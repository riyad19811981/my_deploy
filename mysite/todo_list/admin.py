from django.contrib import admin
from .models import List, Topic, WebPage, AccessRecord, Country, City, Person, UserProfileInfo

admin.site.register(List)
admin.site.register(Topic)
admin.site.register(WebPage)
admin.site.register(AccessRecord)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Person)
admin.site.register(UserProfileInfo)

