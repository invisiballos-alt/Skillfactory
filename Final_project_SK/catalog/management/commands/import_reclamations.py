import os
from datetime import datetime
from openpyxl import load_workbook
from django.core.management.base import BaseCommand
from catalog.models import Machine, Reclamation, FailureNode

class Command(BaseCommand):
    help = 'Импорт данных рекламаций из Excel data.xlsx (Вкладка Рекламации)'

    def handle(self, *args, **options):
        file_path = 'data.xlsx'
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"Файл {file_path} не найден в корень проекта!"))
            return

        wb = load_workbook(file_path, data_only=True)
        # Открываем третью вкладку рекламаций
        sheet = wb.worksheets[2] 

        self.stdout.write(self.style.WARNING("Начало импорта рекламаций..."))

        for row_idx in range(3, sheet.max_row + 1):
            serial_number_raw = sheet[f'C{row_idx}'].value # Предполагаем, что зав. № машины в колонке C
            if not serial_number_raw:
                continue

            try:
                # 1. Читаем ячейки по буквам колонок вашей третьей вкладки
                serial_number = str(serial_number_raw).strip()
                
                # Дата отказа (Колонка B)
                raw_refusal_date = sheet[f'B{row_idx}'].value
                if isinstance(raw_refusal_date, datetime):
                    refusal_date = raw_refusal_date.date()
                else:
                    refusal_date = datetime.strptime(str(raw_refusal_date).strip(), "%d.%m.%Y").date()

                operating_hours = int(sheet[f'D{row_idx}'].value)
                node_name = str(sheet[f'E{row_idx}'].value).strip()
                failure_description = str(sheet[f'F{row_idx}'].value).strip()
                recovery_method = str(sheet[f'G{row_idx}'].value).strip()
                spare_parts = str(sheet[f'H{row_idx}'].value).strip() if sheet[f'H{row_idx}'].value else ""
                
                # Дата восстановления (Колонка I)
                raw_recovery_date = sheet[f'I{row_idx}'].value
                if isinstance(raw_recovery_date, datetime):
                    recovery_date = raw_recovery_date.date()
                else:
                    recovery_date = datetime.strptime(str(raw_recovery_date).strip(), "%d.%m.%Y").date()

                # 2. Находим машину и узел поломки в базе Django
                machine = Machine.objects.filter(serial_number=serial_number).first()
                if not machine:
                    self.stdout.write(self.style.ERROR(f"Строка {row_idx}: Машина №{serial_number} не найдена в базе! Пропускаем рекламацию."))
                    continue

                failure_node = FailureNode.objects.filter(name__iexact=node_name).first()

                # 3. Сохраняем в базу данных
                Reclamation.objects.update_or_create(
                    machine=machine,
                    refusal_date=refusal_date,
                    failure_node=failure_node,
                    defaults={
                        'operating_hours': operating_hours,
                        'failure_description': failure_description,
                        'recovery_method': recovery_method,
                        'spare_parts': spare_parts,
                        'recovery_date': recovery_date,
                        # Поле downtime_days посчитается автоматически в методе save() вашей модели!
                    }
                )
                self.stdout.write(self.style.SUCCESS(f"Строка {row_idx}: Рекламация по машине №{serial_number} успешно добавлена."))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Ошибка в строке {row_idx}: {e}"))

        self.stdout.write(self.style.SUCCESS("Импорт рекламаций успешно завершен!"))
