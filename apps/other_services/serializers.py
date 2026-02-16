from http import client
from rest_framework import serializers
from .models import OHC, CareProgram , EyeDentalTreatment , MedicalCamp , CampCase , CHP, TypeOfOHC , EyeTreatmentCase , DentalTreatmentCase
from apps.test_individual.models import IndividualTest as Test
from apps.master_management.models import City, ServiceMapping , State
from apps.client_customer.models import ClientCustomer, ClientCustomerDependent

class CareProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareProgram
        fields = [
            'id',
            'care_program_name',
            'normal_price',
            'care_program_details',
            'image',
            'is_active',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
            'deleted_at'
        ]


# EYE & DENTAL TREATMENTS SERIALIZER-----

class EyeDentalTreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EyeDentalTreatment
        fields = [
            "id",
            "treatment_type",
            "treatment_name",
            "image",
            "is_active",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
            "deleted_at",
        ]


# MEDICAL CAMP SERIALIZER-----


class MedicalCampSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source="main_client.corporate_name", read_only=True)
    sub_client_name = serializers.CharField(source="sub_client.name", read_only=True)
    package_name = serializers.CharField(source="package.package_name", read_only=True)
    test_name = serializers.CharField(source="tests.test_name", read_only=True)
    network_provider_name = serializers.CharField(source="network_provider.center_name", read_only=True)


    class Meta:
        model = MedicalCamp
        fields = "__all__"
        read_only_fields = ("case_id", "created_at")

    def validate(self, attrs):
        request_from = attrs.get("camp_request_from")
        main_client = attrs.get("main_client")
        sub_client = attrs.get("sub_client")
        package = attrs.get("package")
        test=attrs.get("tests")
        camp_status = attrs.get("camp_status")
        completed_count = attrs.get("completed_medical_count")

        if request_from == "Sub Client":
            if not sub_client:
                raise serializers.ValidationError(
                    "Sub client is required when request is from Sub Client."
                )
            if sub_client.client_id != main_client.id:
                raise serializers.ValidationError(
                    "Selected sub client does not belong to the selected main client."
                )
            
        
        if not main_client:
            raise serializers.ValidationError("Main client is required.")
        
        if not request_from:
            raise serializers.ValidationError("Camp request from is required.")
            
        if not package:
            raise serializers.ValidationError("Package is required.")
            
         # Package must belong to client
        if package and package.client_id != main_client.id:
            raise serializers.ValidationError("Selected package does not belong to the selected client.")

        # ✅ Test must belong to the selected package
        # Since Package has test_ids (M2M or reverse FK)
        if not package.tests_included.filter(id=test.id).exists():
            raise serializers.ValidationError("Selected test does not belong to the selected package.")
        

        if camp_status == "Completed":
            if completed_count is None:
                raise serializers.ValidationError(
                    "completed_medical_count is required when case_status is Completed."
                )
            if completed_count <= 0:
                raise serializers.ValidationError(
                    "completed_medical_count must be greater than 0 when case_status is Completed."
                )

        return attrs


# ADD CASE SERIALIZERS-----


class CampCaseSerializer(serializers.ModelSerializer):
    # Existing auto fields
    case__id = serializers.CharField(source="case_id", read_only=True)
    customer__id = serializers.CharField(source="customer_id", read_only=True)
    updated_by_name=serializers.CharField(source="updated_by.name", read_only=True)

    # ✅ Fields from MedicalCamp
    camp_id = serializers.CharField(source="camp.camp_id", read_only=True)
    client_name = serializers.CharField(source="camp.main_client.corporate_name", read_only=True)
    sub_client_name = serializers.CharField(source="camp.sub_client.name", read_only=True)
    camp_location = serializers.CharField(source="camp.camp_location", read_only=True)
    city_name = serializers.CharField(source="camp.camp_city.name", read_only=True)


    # Optional: names for FK fields in Case
    status_name = serializers.CharField(source="case_status.name", read_only=True)

    class Meta:
        model = CampCase
        fields = "__all__"
        read_only_fields = ("case_id", "customer_id", "created_at")


# COMPREHENSIVE HEALTH PLANS SERIALIZER-----

class CHPSerializer(serializers.ModelSerializer):
    package_name = serializers.CharField(source="package.package_name", read_only=True)
    product_name = serializers.CharField(source="product.name", read_only=True)
    service_name = serializers.CharField(source="service.name", read_only=True)

    class Meta:
        model = CHP
        fields = "__all__"

    def validate(self, attrs):
        product = attrs.get("product")
        service = attrs.get("service")

        # ✅ Check mapping: product must have this service in sub_products
        mapping = ServiceMapping.objects.filter(product=product).first()

        if not mapping:
            raise serializers.ValidationError("No service mapping found for this product.")

        if not mapping.sub_products.filter(id=service.id).exists():
            raise serializers.ValidationError(
                "Selected service does not belong to the selected product."
            )

        return attrs
    

# OHC MASTER SERIALIZERS-------

class TypeOfOHCSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeOfOHC
        fields = "__all__"

# OHC MAIN SERIALIZERS-------


class OHCSerializer(serializers.ModelSerializer):
    type_of_ohc_name = serializers.CharField(source="type_of_ohc.name", read_only=True)
    client_name = serializers.CharField(source="client.corporate_name", read_only=True)  
    doctor_name = serializers.CharField(source="doctor.doctor_name", read_only=True)  
    
    created_by_name = serializers.CharField(source="created_by.name", read_only=True)
    updated_by_name = serializers.CharField(source="updated_by.name", read_only=True)          

    class Meta:
        model = OHC
        fields = "__all__"
        read_only_fields = ("doctor_qualifications",)


# EYE PROCEDURE SERIALIZER-------


class EyeTreatmentCaseSerializer(serializers.ModelSerializer):

    relationship_person_id = serializers.IntegerField(
        write_only=True,
        required=False
    )
    relationship_person_name = serializers.CharField(source='relationship_person.name', read_only=True)
    client_name = serializers.CharField(source='client.corporate_name', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    employee_name = serializers.CharField(source='employee.corporate_name', read_only=True)
    eye_treatment_name = serializers.CharField(source='eye_treatment.name', read_only=True)
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
        model = EyeTreatmentCase
        fields = '__all__'
        read_only_fields = ['case_id','created_at']

    def validate_eye_treatment(self, value):
       
        if value.treatment_type != 'Eye':
            raise serializers.ValidationError(
                "Only Eye treatments are allowed in Eye Treatment Case."
            )
        return value

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

            dependent = ClientCustomerDependent.objects.filter(
                id=relationship_person_id,
                customer=employee,
                relationship=case_for
            ).first()

            if not dependent:
                raise serializers.ValidationError(
                    "Invalid relationship person selected."
                )

            if 'customer_name' not in initial:
                data['customer_name'] = dependent.name

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
                        field: "This field is required for dependent case."
                    })
                

            data['state'] = State.objects.get(id=initial['state'])
            data['city'] = City.objects.get(id=initial['city'])

        return data
    

# DENTAL PROCEDURE SERIALIZER-------


class DentalTreatmentCaseSerializer(serializers.ModelSerializer):
    relationship_person_id = serializers.IntegerField(write_only=True, required=False)
    relationship_person_name = serializers.CharField(source='relationship_person.name', read_only=True)
    client_name = serializers.CharField(source='client.corporate_name', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    employee_name = serializers.CharField(source='employee.corporate_name', read_only=True)
    dental_treatment_name = serializers.CharField(source='dental_treatment.name', read_only=True)
    case_status_name = serializers.CharField(source='case_status.name', read_only=True)
    city_name = serializers.CharField(source='city.name', read_only=True)
    state_name = serializers.CharField(source='state.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)

    customer_name = serializers.CharField(required=False)
    mobile_number = serializers.CharField(required=False)
    email_id = serializers.EmailField(required=False)
    address = serializers.CharField(required=False, allow_blank=True)
    state = serializers.PrimaryKeyRelatedField(queryset=State.objects.all(), required=False)
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), required=False)

    class Meta:
        model = DentalTreatmentCase
        fields = '__all__'
        read_only_fields = ['case_id', 'created_at']

    def validate_dental_treatment(self, value):
        if value.treatment_type != 'Dental':
            raise serializers.ValidationError("Only Dental treatments are allowed in Dental Treatment Case.")
        return value

    def validate(self, data):
        case_for = data['case_for']
        employee = data['employee']
        initial = self.initial_data

        # SELF
        if case_for.name.lower() == 'self':
            data['relationship_person'] = None

            if 'customer_name' not in initial:
                data['customer_name'] = employee.customer_name

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

        # dependent
        else:
            relationship_person_id = initial.get('relationship_person_id')
            if not relationship_person_id:
                raise serializers.ValidationError({"relationship_person_id": "Relationship person is required."})

            dependent = ClientCustomerDependent.objects.filter(
                id=relationship_person_id,
                customer=employee,
                relationship=case_for
            ).first()

            if not dependent:
                raise serializers.ValidationError("Invalid relationship person selected.")

            data['relationship_person'] = dependent

            if 'customer_name' not in initial:
                data['customer_name'] = dependent.name

            required_fields = ['mobile_number', 'email_id', 'state', 'city', 'address']
            for field in required_fields:
                if field not in initial:
                    raise serializers.ValidationError({field: "This field is required for dependent case."})

            data['state'] = State.objects.get(id=initial['state'])
            data['city'] = City.objects.get(id=initial['city'])

        return data