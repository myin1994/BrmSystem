import os

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoCRM.settings")
    import django
    django.setup()

    from app01 import models
    c_list = []
    for i in range(521):
        obj = models.Customer(
            qq= f'{i+1}{i+2}{i+3}',
            name= f'name{i}',
            course=['LinuxL',]
        )
        c_list.append(obj)
    models.Customer.objects.bulk_create(c_list)