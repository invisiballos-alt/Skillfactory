from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from .models import Machine, Maintenance, Reclamation, VehicleModel, EngineModel, TransmissionModel, SteerAxleModel, DriveAxleModel, FailureNode

class HomeView(View):
    def get(self, request):
        user = request.user
        context = {
            'is_authenticated': user.is_authenticated,
            # Передаем справочники для выпадающих списков фильтрации
            'vehicle_models': VehicleModel.objects.all(),
            'engine_models': EngineModel.objects.all(),
            'transmission_models': TransmissionModel.objects.all(),
            'steer_models': SteerAxleModel.objects.all(),
            'drive_models': DriveAxleModel.objects.all(),
        }

        # -----------------------------------------------------------------
        # ЛОГИКА ДЛЯ ГОСТЯ (НЕАВТОРИЗОВАННЫЙ ПОЛЬЗОВАТЕЛЬ)
        # -----------------------------------------------------------------
        if not user.is_authenticated:
            search_query = request.GET.get('search_serial', '').strip()
            context['search_query'] = search_query

            if search_query:
                # Ищем машину по точному заводскому номеру
                machine = Machine.objects.filter(serial_number=search_query).first()
                if machine:
                    context['machine_found'] = True
                    context['machine'] = machine
                else:
                    context['machine_found'] = False
                    context['error_message'] = f"Данных о машине с заводским номером «{search_query}» нет в системе."
            
            return render(request, 'catalog/index.html', context)

        # -----------------------------------------------------------------
        # ЛОГИКА ДЛЯ АВТОРИЗОВАННЫХ ПОЛЬЗОВАТЕЛЕЙ (ВКЛАДКИ И ПРАВА)
        # -----------------------------------------------------------------
        # Базовые наборы данных (QuerySets) с сортировкой по умолчанию из ТЗ
        machines_qs = Machine.objects.all().order_by('shipping_date')
        # Предполагаем, что у вас созданы модели Maintenance и Claim со своими датами
        maintenance_qs = Maintenance.objects.all().order_by('date') if 'Maintenance' in globals() else []
        
        claims_qs = Reclamation.objects.all().order_by('refusal_date') if 'Reclamation' in globals() else []

        # Фильтрация по ролям пользователей
        if user.groups.filter(name='Менеджеры').exists() or user.is_superuser:
            # Менеджер завода видит ВСЮ технику без ограничений
            pass
            
        elif user.groups.filter(name='Сервисные организации').exists():
            # Сервисная организация видит только те машины, которые она обслуживает
            machines_qs = machines_qs.filter(service_company__name__icontains=user.first_name)
            if maintenance_qs:
                maintenance_qs = maintenance_qs.filter(service_company__name__icontains=user.first_name)
            if claims_qs:
                claims_qs = Reclamation.filter(machine__service_company__name__icontains=user.first_name)

                
        elif user.groups.filter(name='Клиенты').exists():
            # Клиент видит только закрепленные за его аккаунтом машины
            machines_qs = machines_qs.filter(client=user)
            if maintenance_qs:
                maintenance_qs = maintenance_qs.filter(machine__client=user)
            if claims_qs:
                claims_qs = Reclamation.filter(machine__client=user)

        # -----------------------------------------------------------------
        # РЕАЛИЗАЦИЯ ФИЛЬТРОВ ИЗ ТЗ (ДЛЯ ТАБЛИЦЫ МАШИН)
        # -----------------------------------------------------------------
        if request.GET.get('f_vehicle'):
            machines_qs = machines_qs.filter(vehicle_model_id=request.GET.get('f_vehicle'))
        if request.GET.get('f_engine'):
            machines_qs = machines_qs.filter(engine_model_id=request.GET.get('f_engine'))
        if request.GET.get('f_trans'):
            machines_qs = machines_qs.filter(transmission_model_id=request.GET.get('f_trans'))
        if request.GET.get('f_steer'):
            machines_qs = machines_qs.filter(steer_axle_model_id=request.GET.get('f_steer'))
        if request.GET.get('f_drive'):
            machines_qs = machines_qs.filter(drive_axle_model_id=request.GET.get('f_drive'))

        context.update({
            'machines': machines_qs,
            'maintenances': maintenance_qs,
            'claims': claims_qs,
        })
        return render(request, 'catalog/index.html', context)
