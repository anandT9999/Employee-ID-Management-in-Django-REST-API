# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Employee
from django.db import IntegrityError
from django.core.exceptions import ValidationError


# Helper function to check if a key is missing in the request JSON
def check_missing_keys(data, required_keys):
    missing_keys = [key for key in required_keys if key not in data]
    return missing_keys


# Helper function to validate data types
def validate_data_types(data):
    required_data_types = {
        'name': str,
        'email': str,
        'age': int,
        'gender': str,
        'phoneNo': str,
        'addressDetails': dict,
        'workExperience': list,
        'qualifications': list,
        'projects': list,
        'photo': str
    }

    for key, value_type in required_data_types.items():
        if key not in data:
            continue
        if not isinstance(data[key], value_type):
            return False
    return True


# Helper function to create employee
def create_employee(data):
    try:
        employee = Employee.objects.create(**data)
        return JsonResponse({
            'message': 'Employee created successfully',
            'regid': employee.regid,
            'success': True
        })
    except IntegrityError:
        return JsonResponse({
            'message': 'Employee already exists',
            'success': False
        })
    except Exception as e:
        return JsonResponse({
            'message': 'Employee creation failed',
            'success': False
        }, status=500)


@csrf_exempt
def create_employee_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            required_keys = ['name', 'email', 'age', 'gender', 'addressDetails', 'workExperience', 'qualifications', 'projects', 'photo']
            missing_keys = check_missing_keys(data, required_keys)
            if missing_keys:
                return JsonResponse({
                    'message': 'Invalid body request, missing keys: {}'.format(missing_keys),
                    'success': False
                }, status=400)

            if not validate_data_types(data):
                return JsonResponse({
                    'message': 'Invalid body request, data types mismatch',
                    'success': False
                }, status=400)

            return create_employee(data)
        except Exception as e:
            return JsonResponse({
                'message': 'Employee creation failed',
                'success': False
            }, status=500)


@csrf_exempt
def update_employee_view(request):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            if 'regid' not in data:
                return JsonResponse({
                    'message': 'Invalid body request, regid missing',
                    'success': False
                }, status=400)

            regid = data.pop('regid')
            try:
                employee = Employee.objects.get(regid=regid)
            except Employee.DoesNotExist:
                return JsonResponse({
                    'message': 'No employee found with this regid',
                    'success': False
                })

            for key, value in data.items():
                setattr(employee, key, value)

            employee.save()

            return JsonResponse({
                'message': 'Employee details updated successfully',
                'success': True
            })
        except Exception as e:
            return JsonResponse({
                'message': 'Employee updation failed',
                'success': False
            }, status=500)


@csrf_exempt
def delete_employee_view(request):
    if request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            if 'regid' not in data:
                return JsonResponse({
                    'message': 'Invalid body request, regid missing',
                    'success': False
                }, status=400)

            regid = data['regid']
            try:
                employee = Employee.objects.get(regid=regid)
                employee.delete()
                return JsonResponse({
                    'message': 'Employee deleted successfully',
                    'success': True
                })
            except Employee.DoesNotExist:
                return JsonResponse({
                    'message': 'No employee found with this regid',
                    'success': False
                })

        except Exception as e:
            return JsonResponse({
                'message': 'Employee deletion failed',
                'success': False
            }, status=500)


def get_employee_view(request):
    regid = request.GET.get('regid')

    if regid:
        try:
            employee = Employee.objects.get(regid=regid)
            employees = [employee.serialize()]
        except Employee.DoesNotExist:
            return JsonResponse({
                'message': 'Employee details not found',
                'success': False,
                'employees': []
            })

    else:
        employees = [employee.serialize() for employee in Employee.objects.all()]

    return JsonResponse({
        'message': 'Employee details found' if employees else 'Employee details not found',
        'success': bool(employees),
        'employees': employees
    })

