from django.contrib import admin
from .models import Administration, ComplexeSportif, Hall, EpreuveSportive, CustomUser, Tarif, Ticket, Achat

admin.site.register(Administration)
admin.site.register(ComplexeSportif)
admin.site.register(Hall)
admin.site.register(EpreuveSportive)
admin.site.register(CustomUser)
admin.site.register(Tarif)
admin.site.register(Ticket)
admin.site.register(Achat)