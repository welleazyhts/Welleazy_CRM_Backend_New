from rest_framework import serializers
from .models import (
    ServiceProvider, SPOC, ProviderRecognition, ProviderManpower,
    ProviderService, RadiologyItem, BankDetails,
    ProviderDiscount, ProviderVoucher, DepartmentContact , 
ProviderDocuments   )

# ------------------------
# SIMPLE NESTED SERIALIZERS
# ------------------------

class SPOCSerializer(serializers.ModelSerializer):
    class Meta:
        model = SPOC
        exclude = ("provider",)


class DepartmentContactSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(
        source="department.name", read_only=True)
    class Meta:
        model = DepartmentContact
        exclude = ("provider",)


class ProviderRecognitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderRecognition
        exclude = ("provider",)


class ProviderManpowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderManpower
        exclude = ("provider",)


class ProviderServiceSerializer(serializers.ModelSerializer):
    service_categories_names = serializers.SerializerMethodField()

    class Meta:
        model = ProviderService
        exclude = ("provider",)

    def get_service_categories_names(self, obj):
        return list(obj.service_categories.values_list("name", flat=True))


class RadiologyItemSerializer(serializers.ModelSerializer):
    radiology_type_name = serializers.CharField(
        source="radiology_type.name", read_only=True
    )

    class Meta:
        model = RadiologyItem
        exclude = ("provider",)


class BankDetailsSerializer(serializers.ModelSerializer):
    preffered_payment_term_name = serializers.SerializerMethodField()

    def get_preffered_payment_term_name(self, obj):
        return obj.preffered_payment_term.name if obj.preffered_payment_term else None
    
    class Meta:
        model = BankDetails
        exclude = ("provider",)


class ProviderDiscountSerializer(serializers.ModelSerializer):
    discount_service_name = serializers.SerializerMethodField()
    discount_type = serializers.CharField(read_only=True)

    def get_discount_service_name(self, obj):
        return obj.discount_service.name if obj.discount_service else None

    class Meta:
        model = ProviderDiscount
        exclude = ("provider",)


class ProviderVoucherSerializer(serializers.ModelSerializer):
    voucher_discount_name = serializers.SerializerMethodField()
    voucher_discount_type = serializers.CharField(read_only=True)

    def get_voucher_discount_name(self, obj):
        return obj.voucher_discount.name if obj.voucher_discount else None

    class Meta:
        model = ProviderVoucher
        exclude = ("provider",)


# ------------------------
# MAIN SERVICE PROVIDER SERIALIZER (RESPONSE ONLY)
# ------------------------

class ServiceProviderSerializer(serializers.ModelSerializer):

    provider_type_name = serializers.CharField(source="provider_type.name", read_only=True)
    partnership_type_name = serializers.CharField(source="partnership_type.name", read_only=True)
    specialty_type_name = serializers.CharField(source="specialty_type.name", read_only=True)
    ownership_type_name = serializers.CharField(source="ownership_type.name", read_only=True)

    city_name = serializers.CharField(source="city.name", read_only=True)
    state_name = serializers.CharField(source="state.name", read_only=True)
    dc_unique_name = serializers.CharField(source="dc_unique_name.name", read_only=True)
    

    client_company_names = serializers.SerializerMethodField()
    medical_specialties_names = serializers.SerializerMethodField()
    recognition_names = serializers.SerializerMethodField()
    accreditation_names = serializers.SerializerMethodField()

    spocs = SPOCSerializer(many=True, required=False)
    department_contacts = DepartmentContactSerializer(many=True, required=False)
    recognition = ProviderRecognitionSerializer(required=False)
    manpower = ProviderManpowerSerializer(required=False)
    service = ProviderServiceSerializer(required=False)
    radiologies = RadiologyItemSerializer(many=True, required=False)
    bank = BankDetailsSerializer(required=False)
    discounts = ProviderDiscountSerializer(many=True, required=False)
    vouchers = ProviderVoucherSerializer(many=True, required=False)
    visit_type_name = serializers.SerializerMethodField()
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    

    class Meta:
        model = ServiceProvider
        fields = "__all__"

    def get_client_company_names(self, obj):
        return list(obj.client_company.values_list("corporate_name", flat=True))

    def get_medical_specialties_names(self, obj):
        return list(obj.medical_specialties.values_list("name", flat=True))
    
    def get_visit_type_name(self, obj):
        return obj.visit_type.name if obj.visit_type else None
    
    def get_recognition_names(self, obj):
        if hasattr(obj, "recognition"):
            return list(obj.recognition.recognitions.values_list("name", flat=True))
        return []

    def get_accreditation_names(self, obj):
        if hasattr(obj, "recognition"):
            return list(obj.recognition.accreditations.values_list("name", flat=True))
        return []


# DOCUMENT UPLOAD SERIALIZERS



ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/jpg"]
ALLOWED_DOC_TYPES = ALLOWED_IMAGE_TYPES + ["application/pdf"]

def validate_file(value, max_size_mb):
    if value:
        if value.size > max_size_mb * 1024 * 1024:
            raise serializers.ValidationError(f"File size exceeds {max_size_mb} MB limit")
        if value.content_type not in ALLOWED_DOC_TYPES:
            raise serializers.ValidationError("Only JPG, JPEG, PNG, PDF allowed")
    return value


class ProviderDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProviderDocuments
        fields = "__all__"
        read_only_fields = ["provider"]

    def validate_dc_logo(self, value):
        return validate_file(value, 1)  # 1 MB

    def validate_dc_photo(self, value):
        return validate_file(value, 15)  # 15 MB

    # PDF or image files - 1 MB
    def validate_registration_certificate(self, value):
        return validate_file(value, 1)

    def validate_gst_certificate(self, value):
        return validate_file(value, 1)

    def validate_agreement_legal_document(self, value):
        return validate_file(value, 1)

    def validate_lol_legal_document(self, value):
        return validate_file(value, 1)

    def validate_pan_card(self, value):
        return validate_file(value, 1)

    def validate_vendor_registration_form(self, value):
        return validate_file(value, 1)

    def validate_mou_signed_copy(self, value):
        return validate_file(value, 1)

    def validate_other_document(self, value):
        return validate_file(value, 1)
    

# GENERATE THE LINK FOR PROVIDER REGISTRATION SERIALIZER------


from rest_framework import serializers
from .models import ProviderRegistrationLink


class ProviderRegistrationLinkSerializer(serializers.ModelSerializer):
    provider_type_name = serializers.CharField(
        source="provider_type.name",
        read_only=True
    )

    class Meta:
        model = ProviderRegistrationLink
        fields = "__all__"
        read_only_fields = (
            "id",
            "token",
            "generated_link",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        )



# DISCOUNT VIEW SERIALIZER----



class DiscountListSerializer(serializers.ModelSerializer):
    discount_service_name = serializers.CharField(
        source="discount_service.name", read_only=True
    )

    dc_name = serializers.CharField(
        source="provider.center_name", read_only=True
    )

    address = serializers.CharField(
        source="provider.address", read_only=True
    )

    area = serializers.CharField(
        source="provider.area", read_only=True
    )

    city = serializers.CharField(
        source="provider.city.name", read_only=True
    )

    state = serializers.CharField(
        source="provider.state.name", read_only=True
    )

    provider_status = serializers.CharField(
        source="provider.status", read_only=True
    )

    # ✅ NEW FIELDS FROM ProviderDocuments
    dc_logo = serializers.SerializerMethodField()
    dc_photo = serializers.SerializerMethodField()

    def get_dc_logo(self, obj):
        docs = getattr(obj.provider, "documents", None)
        if docs and docs.dc_logo:
            request = self.context.get("request")
            return request.build_absolute_uri(docs.dc_logo.url)
        return None

    def get_dc_photo(self, obj):
        docs = getattr(obj.provider, "documents", None)
        if docs and docs.dc_photo:
            request = self.context.get("request")
            return request.build_absolute_uri(docs.dc_photo.url)
        return None

    class Meta:
        model = ProviderDiscount
        fields = [
            "id",
            "discount_service_name",
            "discount_percent",
            "dc_logo",
            "dc_photo",
            "dc_name",
            "address",
            "area",
            "city",
            "state",
            "provider_status",
        ]


# Voucher view serializer-----



class VoucherListSerializer(serializers.ModelSerializer):
    dc_name = serializers.CharField(source="provider.center_name", read_only=True)
    city_name = serializers.CharField(source="provider.city.name", read_only=True)
    voucher_discount_name = serializers.CharField(source="voucher_discount.name", read_only=True)

    class Meta:
        model = ProviderVoucher
        fields = [
            "id",
            "voucher_added_date",
            "voucher_id",
            "voucher_code",
            "voucher_discount_name",
            "discount_percent",
            "dc_name",
            "start_date",
            "expiry_date",
            "city_name",
            "voucher_FAQ",
            "Voucher_status",
        ]