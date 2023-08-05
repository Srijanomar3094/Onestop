from django.contrib.auth.models import User
def create_superuser():
    # Replace 'admin', 'password', and 'admin@example.com' with the desired values
    user = User.objects.create_user(username='srijan', password='srijanomar', email='srijanomar5840@example.com')
    user.is_superuser = True
    user.is_staff = True
    user.save()

if __name__ == '__main__':
    create_superuser()