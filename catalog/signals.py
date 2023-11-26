from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Receipt, Item, Supplier, Fabric
import random


@receiver(post_save, sender=Receipt)
def auto_reorder(sender, instance, **kwargs):
    items = Item.objects.count()
    sold_item_count = Receipt.objects.count()
    unsold_item_count = items - sold_item_count
    if unsold_item_count < 10:
        supplier = random.choice(Supplier.objects.all())
        fabric = random.choice(Fabric.objects.all())
        type = random.choice(['Вечірня сукня', 'Куртка', 'Футболка', 'Класичні штани',
                              'Пальто', 'Міні-спідниця', 'Спортивний світшот', 'Блуза',
                              'Класичні джинси', 'Майка', 'Светр', 'Рубашка',
                              'Блузка', 'Коктейльна сукня', 'Бомбер', 'Джерсі',
                              'Повсякденні шорти', 'Пальчиковий жакет', 'Максі-спідниця', 'Фітнес-топ',
                              'Джоггери', 'Пуловер', 'Костюмна сорочка', 'Шорти-бермуди',
                              'Денім-спідниця', 'Теніска з коротким рукавом', 'Кардиган', 'Плащ',
                              'Літні штани', 'Пуховик', 'Комбінезон', 'Леггінси',
                              'Спортивні штани', 'Туніка', 'Брюки-кюлоти', 'Капрі'])

        brand = random.choice(['CasualComfort', 'ChiElegance', 'DenimDreams', 'ElegantStyle',
                               'Hicco', 'OfficeChi', 'OutdoorAdventures', 'SadGhT',
                               'SportyStyle', 'TrendyVibes', 'UrbanStyle', 'LuxeCraft',
                               'UrbanVogue', 'VenBlend', 'TrendFlow', 'NovaChic',
                               'ClothesHub', 'EchoElite', 'VelvetAura', 'VivaPulse',
                               'LuminaStyle', 'UrbaneCraft', 'SavvyGlow', 'HarmonyHaven',
                               'VelvetVista', 'OpulaNex', 'SereneStyle', 'InnoNook',
                               'EnchantElite', 'VenBlend', 'RefinedRise', 'SSphere',
                               ])
        size = random.choice([choice[0] for choice in Item.SIZE])
        gender = random.choice([choice[0] for choice in Item.GENDER])
        color = random.choice([choice[0] for choice in Item.COLOR])
        chemical_treatment = random.choice([choice[0] for choice in Item.TREATMENT])
        seasonality = random.choice([choice[0] for choice in Item.SEASONALITY])
        state = random.choice([choice[0] for choice in Item.STATE])
        price = random.uniform(1, 5000)
        Item.objects.create(
            supplier=supplier,
            fabric=fabric,
            type=type,
            brand=brand,
            size=size,
            gender=gender,
            color=color,
            chemical_treatment=chemical_treatment,
            seasonality=seasonality,
            state=state,
            price=price
        )

