from rest_framework import serializers
from django.db import transaction
from apps.accounts.models import User
from .models import ClientLogin, MasterSubPermission
from apps.client.models import Client
from apps.client_branch.models import ClientBranch
from apps.client_customer.models import ClientCustomer

class ClientLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    client_name = serializers.CharField(source='client.corporate_name', read_only=True)
    branch_name = serializers.CharField(source='branch.branch_name', read_only=True)
    employee_name = serializers.CharField(source='employee.customer_name', read_only=True)
    created_by = serializers.CharField(source='created_by.name', read_only=True, allow_null=True)
    updated_by = serializers.CharField(source='updated_by.name', read_only=True, allow_null=True)
    current_permissions = serializers.SerializerMethodField()

    class Meta:
        model = ClientLogin
        fields = [
            'id', 'client', 'branch', 'employee', 
            'username', 'email', 'password', 'is_active', 'permissions',
            'client_name', 'branch_name', 'employee_name', 
            'created_by', 'updated_by', 'created_at', 'updated_at',
            'current_permissions'
        ]
        read_only_fields = ['user']

    def get_current_permissions(self, obj):
        return obj.permissions.values_list('id', flat=True)

    def validate_username(self, value):
        if ClientLogin.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def validate_email(self, value):
        if value and User.objects.filter(email=value).exists():
             raise serializers.ValidationError("User with this email already exists.")
        return value

    def create(self, validated_data):
        username = validated_data.pop('username')
        email = validated_data.pop('email', None) 
        password = validated_data.pop('password')
        permissions = validated_data.pop('permissions', [])
        
        employee = validated_data.get('employee')
        mobile_number = employee.mobile_no
        
        if not email:
            email = employee.email_id
            
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": f"User with email {email} already exists."})
            
        if User.objects.filter(mobile_number=mobile_number).exists():
             raise serializers.ValidationError({"employee": "User with this employee's mobile number already exists."})

        with transaction.atomic():
            # Create User
            user = User.objects.create_user(
                email=email,
                password=password,
                mobile_number=mobile_number,
                name=employee.customer_name
            )
            
            # Create Client Login with the custom username
            client_login = ClientLogin.objects.create(
                user=user, 
                username=username,
                **validated_data
            )
            
            # Set Permissions
            if permissions:
                client_login.permissions.set(permissions)
                
        return client_login

    def update(self, instance, validated_data):
        permissions = validated_data.pop('permissions', None)
        password = validated_data.pop('password', None)
        
        # Update User password if provided
        if password:
            instance.user.set_password(password)
            instance.user.save()

        # Update ClientLogin fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update Permissions
        if permissions is not None:
            instance.permissions.set(permissions)

        return instance

class ClientUserContextSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.corporate_name')
    branch_name = serializers.CharField(source='branch.branch_name')
    employee_name = serializers.CharField(source='employee.customer_name')
    # employee_id = serializers.CharField(source='employee.id')
    permissions_list = serializers.SerializerMethodField()

    class Meta:
        model = ClientLogin
        fields = ['id', 'client', 'client_name', 'branch', 'branch_name', 'employee', 'employee_name', 'permissions_list']

    def get_permissions_list(self, obj):
        return list(obj.permissions.values('id', 'name', 'permission__name'))
