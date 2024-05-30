from django.contrib import admin
from .models import Administration, ComplexeSportif, Hall, EpreuveSportive, CustomUser, Tarif, Ticket, Achat


class TicketAdmin(admin.ModelAdmin):
    list_display = ('epreuve_sportive', 'start_time_epreuve', 'remaining_places', 'total_sales', 'sales_by_offer_display')

    def sales_by_offer_display(self, obj):
        sales_by_offer = obj.sales_by_offer()
        return ', '.join([f"{offer.name_tarif}: {sales}" for offer, sales in sales_by_offer.items()])

    sales_by_offer_display.short_description = 'Sales by Offer'



admin.site.register(Administration)
admin.site.register(ComplexeSportif)
admin.site.register(Hall)
admin.site.register(EpreuveSportive)
admin.site.register(CustomUser)
admin.site.register(Tarif)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Achat)