from rest_framework import serializers

from apps.master_management.models import City, State
from .models import CareProgramCase
from apps.client_customer.models import ClientCustomer, ClientCustomerDependent

class CareProgramCaseSerializer(serializers.ModelSerializer):

    relationship_person_id = serializers.IntegerField(
        write_only=True,
        required=False
    )
    relationship_person_name = serializers.CharField(source='relationship_person.name', read_only=True)
    client_name = serializers.CharField(source='client.corporate_name', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    employee_name = serializers.CharField(source='employee.corporate_name', read_only=True)
    care_program_name = serializers.CharField(source='care_program.care_program_name', read_only=True)
    case_status_name = serializers.CharField(source='case_status.name', read_only=True)
    city_name = serializers.CharField(source='city.name', read_only=True)
    state_name = serializers.CharField(source='state.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)
    case_for_name = serializers.CharField(source='case_for.name', read_only=True)

    customer_name = serializers.CharField(required=False)
    mobile_number = serializers.CharField(required=False)
    email_id = serializers.EmailField(required=False)
    address = serializers.CharField(required=False, allow_blank=True)
    state = serializers.PrimaryKeyRelatedField(
        queryset=State.objects.all(),
        required=False
    )
    city = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(),
        required=False
    )

    class Meta:
        model = CareProgramCase
        fields = '__all__'
        read_only_fields = ['case_id','created_at']

    def validate(self, data):
        case_for = data['case_for']
        employee = data['employee']
        initial=self.initial_data

        # -------------------
        # SELF CASE
        # -------------------
        if case_for.name.lower() == 'self':
            data['relationship_person'] = None
            if 'customer_name' not in initial:
                data['customer_name'] = employee.customer_name

            # editable fields with fallback
                data['mobile_number'] = initial.get('mobile_number', employee.mobile_no)
                data['email_id'] = initial.get('email_id', employee.email_id)
                data['address'] = initial.get('address', employee.area_locality)
            if 'state' not in initial:
                data['state'] = employee.state
            else:
                data['state'] = State.objects.get(id=initial['state'])

            if 'city' not in initial:
                data['city'] = employee.city
            else:
                data['city'] = City.objects.get(id=initial['city'])

        # -------------------
        # RELATION CASE
        # -------------------
        else:
            relationship_person_id = initial.get('relationship_person_id')

            if not relationship_person_id:
                raise serializers.ValidationError({
                    "relationship_person_id": "Relationship person is required."
                })

            dependant = ClientCustomerDependent.objects.filter(
                id=relationship_person_id,
                customer=employee,
                relationship=case_for
            ).first()

            if not dependant:
                raise serializers.ValidationError(
                    "Invalid relationship person selected."
                )

            if 'customer_name' not in initial:
                data['customer_name'] = dependant.name

            required_fields=[
                'mobile_number',
                'email_id',
                'state',
                'city',
                'address'
            ]

            for field in required_fields:
                if field not in initial:
                    raise serializers.ValidationError({
                        field: "This field is required for dependant case."
                    })
                

            data['state'] = State.objects.get(id=initial['state'])
            data['city'] = City.objects.get(id=initial['city'])

        return data
