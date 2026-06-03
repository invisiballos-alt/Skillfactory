from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

class Command(BaseCommand):
    help = 'Быстрое создание пользователей системы Силант'

    def handle(self, *args, **options):
        client_group, _ = Group.objects.get_or_create(name='Клиенты')
        service_group, _ = Group.objects.get_or_create(name='Сервисные организации')

        users_to_add = [
            ('promtech', 'ServicePass456!', 'ООО "Промышленная техника"', 'Сервисные организации'),
            ('silant_service', 'SilantPass789!', 'ООО "Силант"', 'Сервисные организации'),
            ('ooofns', 'OooFnsPass129', 'ООО "ФНС"', 'Сервисные организации'),
            ('Trudnikov', 'OooTRUDPass129', 'ИП Трудников С.В.', 'Клиенты'),
            ('ooofkp', 'OooFKPPass129', 'ООО "ФКП21"', 'Клиенты'),
            ('ooodet13', 'OooDET13Pass129', 'ООО "ДЭТ №13"', 'Клиенты'),
            ('mns77', 'SecurePass123!', 'ООО "МНС77"', 'Клиенты'),
            ('mosgorrest', 'SecureMSGR123!', 'ООО "Мосгоррест"', 'Клиенты'),
            ('frp_rus', 'SecureFRPR123!', 'ФРП России', 'Клиенты'),
            ('ran_lph', 'SecureMrunplR123!', 'ООО "Ранский ЛПХ"', 'Клиенты'),
            ('ooo_komplekt-postavka', 'SecureKipmolR123!', 'ООО "Комплект-Поставка"', 'Клиенты'),
            ('GP_SPB', 'SpbrulesR123!', 'ООО "ГП СПБ"', 'Клиенты'),
            ('rmk', 'RMKlesR123!', 'ООО "РМК"', 'Клиенты'),
            ('ao_zander', 'zanrdkfesR123!', 'АО "Зандер"', 'Клиенты'),
            ('t-minus', 'tmindsesR123!', 'АО "Т-Минус"', 'Клиенты'),
            ('GP_krasnodar', 'tmindsesR123!', 'ООО "ГП Краснодар"', 'Клиенты'),
        ]

        for username, password, company_name, group_name in users_to_add:
            if not User.objects.filter(username=username).exists():
                # Создаем пользователя с правильным хэшированием пароля
                user = User.objects.create_user(
                    username=username, 
                    password=password, 
                    first_name=company_name
                )
                
                if group_name in ['Сервисные организации']:
                    user.is_staff = True
                    user.save()

                if group_name == 'Клиенты':
                    user.groups.add(client_group)
                elif group_name == 'Сервисные организации':
                    user.groups.add(service_group)

                self.stdout.write(self.style.SUCCESS(f"Пользователь {username} ({company_name}) создан и добавлен в группу {group_name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Пользователь {username} уже существует, пропускаем."))
