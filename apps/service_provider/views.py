from django.shortcuts import render

# Create your views here.


from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from .models import *
from .serializers import ServiceProviderSerializer , ProviderDocumentSerializer , ProviderRegistrationLinkSerializer , DiscountListSerializer, VoucherListSerializer
from apps.master_management.models import MasterTypeOfProvider
import uuid
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser
from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client

from apps.service_provider.models import ServiceProvider, ProviderRegistrationLink



from rest_framework.generics import ListAPIView
from django.db.models import Q

from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from django.http import HttpResponse
import csv
from openpyxl import Workbook


 




class ServiceProviderViewSet(ModelViewSet):
    queryset = ServiceProvider.objects.all()
    serializer_class = ServiceProviderSerializer
    permission_classes = [IsAdminUser]

    # ---------------- CREATE ----------------
    def create(self, request, *args, **kwargs):
        data = request.data

       

        with transaction.atomic():
            provider = ServiceProvider.objects.create(
                provider_type_id=data["provider_type"],
                partnership_type_id=data["partnership_type"],
                specialty_type_id=data["specialty_type"],
                ownership_type_id=data["ownership_type"],
                corporate_group=data["corporate_group"],
                center_name=data["center_name"],
                email=data["email"],
                mobile=data["mobile"],
                landline=data.get("landline"),
                std_code=data.get("std_code"),
                fax=data.get("fax"),
                plot_no=data.get("plot_no"),
                address=data["address"],
                area=data["area"],
                city_id=data["city"],
                state_id=data["state"],
                pin_code=data["pin_code"],
                service_pin_code=data["service_pin_code"],
                website=data.get("website"),
                visit_type_id=data["visit_type"],
                vendor_registration_name=data.get("vendor_registration_name"),
                dc_unique_name_id=data["dc_unique_name"],
                # payment_term_id=data.get("payment_term"),
                mou_signed=data["mou_signed"],
                mou_received_date=data.get("mou_received_date"),
                remarks=data.get("remarks"),
                created_by=request.user,
                updated_by=request.user,
               
            )

            provider.corporate_companies.set(data.get("corporate_companies", []))
            provider.client_company.set(data.get("client_company", []))
            provider.medical_specialties.set(data.get("medical_specialties", []))

             # ---- BUSINESS RULE ----
            if "corporate_group"=="Yes" and not data.get("corporate_companies"):
                return Response(
                {"corporate_companies": "Required when corporate_group is Yes"},
                status=400
            )
            

            for s in data.get("spocs", []):
                SPOC.objects.create(provider=provider, created_by=request.user,updated_by=request.user, **s)

            for d in data.get("department_contacts", []):
                DepartmentContact.objects.create(
                provider=provider,
                department_id=d["department"],
                title=d.get("title"),
                contact_person_name=d.get("contact_person_name"),
                designation=d.get("designation"),
                email=d.get("email"),
                cell_no=d.get("cell_no"),
                created_by=request.user,
                updated_by=request.user,
            )


            if "recognition" in data:
                rec = ProviderRecognition.objects.create(provider=provider,created_by=request.user,
                updated_by=request.user)
                rec.recognitions.set(data["recognition"].get("recognitions", []))
                rec.accreditations.set(data["recognition"].get("accreditations", []))
                

            if "manpower" in data:
                ProviderManpower.objects.create(provider=provider, created_by=request.user, updated_by=request.user, **data["manpower"])

            if "service" in data:
                categories = data["service"].pop("service_categories", [])
                svc = ProviderService.objects.create(provider=provider, created_by=request.user, updated_by=request.user, **data["service"])
                svc.service_categories.set(categories)

            for r in data.get("radiologies", []):
                 RadiologyItem.objects.create(
                provider=provider,
                radiology_type_id=r["radiology_type"],
                status=r.get("status", False),
                service_mode=r.get("service_mode", "NA"),
                price=r.get("price"),
                discount=r.get("discount", 0),
                time_from=r.get("time_from"),
                time_to=r.get("time_to"),
                created_by=request.user,
                updated_by=request.user,
            )

            if "bank" in data:
                BankDetails.objects.create(provider=provider, created_by=request.user, updated_by=request.user, **data["bank"])

            for d in data.get("discounts", []):
                discount_service_id = d.pop("discount_service_id")

                discount_service = DiscountService.objects.get(id=discount_service_id)

                ProviderDiscount.objects.create(
                provider=provider,
                discount_service_id=discount_service_id,
                discount_type=discount_service.name,   # ✅ AUTO-FILL
                created_by=request.user,
                updated_by=request.user,
                 **d
            )

            
            for v in data.get("vouchers", []):
                v.pop("remarks", None)
                voucher_discount_id = (
                v.pop("voucher_discount", None)
                or v.pop("voucher_discount_id", None)
         )

                if not voucher_discount_id:
                    raise ValidationError("voucher_discount is required")

                voucher_discount = VoucherDiscountType.objects.get(
                id=voucher_discount_id
            )

                ProviderVoucher.objects.create(
                    provider=provider,
                    voucher_discount_id=voucher_discount_id,
                    voucher_discount_type=voucher_discount.name,   # ✅ AUTO-FILL
                    created_by=request.user,
                    updated_by=request.user,
                    **v
            )

        return Response(
            ServiceProviderSerializer(provider).data,
            status=status.HTTP_201_CREATED
        )

    # ---------------- UPDATE ----------------
    

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = request.user

        if data.get("corporate_group") == "Yes" and not data.get("corporate_companies"):
            return Response(
                {"corporate_companies": "Required when corporate_group is Yes"},
                status=400
            )   

    # -----------------------------------
    # 1. SIMPLE FIELDS
    # -----------------------------------
        simple_fields = [
        "center_name", "email", "mobile", "landline", "std_code", "fax",
        "plot_no", "address", "area", "pin_code", "service_pin_code",
        "website", "vendor_registration_name",
        "mou_signed", "mou_received_date", "remarks",
        "corporate_group", "status", "is_active",
        "provider_type", "partnership_type",
        "specialty_type", "ownership_type",
        "visit_type", "city", "state", "dc_unique_name"
    ]

        for field in simple_fields:
            if field in data:
                setattr(instance, field, data[field])

        instance.updated_by = user
        instance.save()

    # -----------------------------------
    # 2. MANY TO MANY
    # -----------------------------------
        if "client_company" in data:
            instance.client_company.set(data["client_company"])

        if "medical_specialties" in data:
            instance.medical_specialties.set(data["medical_specialties"])

        if "corporate_companies" in data:
            if instance.corporate_group == "Yes":
                instance.corporate_companies.set(data["corporate_companies"])
        else:
            instance.corporate_companies.clear()

    # -----------------------------------
    # 3. ONE TO ONE TABLES
    # -----------------------------------
        if "manpower" in data:
            ProviderManpower.objects.update_or_create(
                provider=instance,
                defaults={**data["manpower"], "updated_by": user}
            )

        if "bank" in data:
            BankDetails.objects.update_or_create(
                provider=instance,
                defaults={**data["bank"], "updated_by": user}
        )

        if "recognition" in data:
            rec_data = data["recognition"]
            rec_obj, _ = ProviderRecognition.objects.get_or_create(
                provider=instance,
                defaults={"created_by": user}
            )
            rec_obj.recognitions.set(rec_data.get("recognitions", []))
            rec_obj.accreditations.set(rec_data.get("accreditations", []))
            rec_obj.updated_by = user
            rec_obj.save()

    # -----------------------------------
    # 4. SERVICE (ONE TO ONE + M2M)
    # -----------------------------------
        if "service" in data:
            service_data = data["service"]
            categories = service_data.pop("service_categories", [])

            svc, _ = ProviderService.objects.update_or_create(
                provider=instance,
                defaults={**service_data, "updated_by": user}
            )
            svc.service_categories.set(categories)
            svc.save()

    # -----------------------------------
    # 5. CHILD TABLE UPSERT LOGIC
    # -----------------------------------
        def sync_children(model, rows):
            existing = model.objects.filter(provider=instance)
            existing_map = {obj.id: obj for obj in existing}
            sent_ids = []

            for row in rows:
                row_id = row.pop("id", None)

                if row_id and row_id in existing_map:
                # UPDATE
                    obj = existing_map[row_id]
                    for field, value in row.items():
                        setattr(obj, field, value)
                    obj.updated_by = user
                    obj.save()
                    sent_ids.append(row_id)
                else:
                # CREATE
                    obj = model.objects.create(
                        provider=instance,
                        created_by=user,
                        updated_by=user,
                        **row
                    )
                    sent_ids.append(obj.id)

        # DELETE REMOVED
            model.objects.filter(provider=instance).exclude(id__in=sent_ids).delete()

        if "spocs" in data:
            sync_children(SPOC, data["spocs"])

        if "department_contacts" in data:
            sync_children(DepartmentContact, data["department_contacts"])

        if "radiologies" in data:
            sync_children(RadiologyItem, data["radiologies"])

        if "discounts" in data:
            sync_children(ProviderDiscount, data["discounts"])

        if "vouchers" in data:
            sync_children(ProviderVoucher, data["vouchers"])

    # -----------------------------------
    # 6. RESPONSE
    # -----------------------------------
        response_serializer = self.get_serializer(instance)
        return Response(response_serializer.data, status=status.HTTP_200_OK)




    # ---------------- DELETE ----------------
    def destroy(self, request, *args, **kwargs):
        provider = self.get_object()
        provider.delete()
        return Response(
            {"message": "Service Provider deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
# ---------------- LIST & RETRIEVE are handled by ModelViewSet ----------------


# UPLOAD DOCUMENTS VIEWSET-----


class ProviderDocumentViewSet(ModelViewSet):
    queryset = ProviderDocuments.objects.select_related("provider")
    serializer_class = ProviderDocumentSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        provider_id = request.data.get("provider")

        if not provider_id:
            raise ValidationError({"provider": "Provider ID is required"})

        try:
            provider = ServiceProvider.objects.get(id=provider_id)
        except ServiceProvider.DoesNotExist:
            raise ValidationError({"provider": "Invalid provider ID"})

        # Ensure ONE row per provider
        instance, created = ProviderDocuments.objects.get_or_create(
            provider=provider,
            defaults={
                "created_by": request.user,
                "updated_by": request.user
            }
        )

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)

        serializer.save(updated_by=request.user)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=request.user)

        return Response(serializer.data)
    


# GENERATE THE LINK FOR PROVIDER REGISTRATION------



class ProviderLinkRequestViewSet(ModelViewSet):
    queryset = ProviderRegistrationLink.objects.all()
    serializer_class = ProviderRegistrationLinkSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        instance = serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user
        )

        # ---------------- EMAIL ----------------
        subject = "Provider Registration Link"
        message = (
            f"Dear {instance.concerned_person_name},\n\n"
            f"Please complete provider registration using the link below:\n\n"
            f"{instance.generated_link}\n\n"
            f"Regards,\nWelleazy Team"
        )

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=False,
        )

        # ---------------- SMS (TWILIO) ----------------
        try:
            client = Client(
                settings.TWILIO_ACCOUNT_SID,
                settings.TWILIO_AUTH_TOKEN
            )

            sms_body = (
                "Welleazy Provider Registration Link:\n"
                f"{instance.generated_link}"
            )

            phone = instance.contact_number.strip()
            if not phone.startswith("+"):
                phone = "+91" + phone

            client.messages.create(
                body=sms_body,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=phone
            )

        except Exception as e:
            # Log only — do not break API
            print("Twilio SMS Error:", e)



# SERVICE PROVIDER FILTER VIEWSET-----


class ProviderBaseFilterMixin:
    def apply_filters(self, qs, params):
        center_name = params.get("center_name")
        sp_code = params.get("sp_code")
        area = params.get("area")
        state = params.get("state")
        city = params.get("city")
        pincode = params.get("pincode")

        specialties = params.get("specialties")
        client_company = params.get("client_company")
        status = params.get("status")
        is_active = params.get("is_active")

        if center_name:
            qs = qs.filter(center_name__icontains=center_name)

        if sp_code:
            qs = qs.filter(sp_code__icontains=sp_code)

        if area:
            qs = qs.filter(area__icontains=area)

        if state:
            qs = qs.filter(state_id=state)

        if city:
            qs = qs.filter(city_id=city)

        if pincode:
            qs = qs.filter(pin_code__icontains=pincode)

        if specialties:
            ids = [int(i) for i in specialties.split(",") if i.isdigit()]
            qs = qs.filter(medical_specialties__id__in=ids)

        if client_company:
            ids = [int(i) for i in client_company.split(",") if i.isdigit()]
            qs = qs.filter(client_company__id__in=ids)

        if status:
            qs = qs.filter(status__in=status.split(","))

        if is_active is not None:
            qs = qs.filter(is_active=is_active.lower() == "true")

        return qs.distinct()
    



class ProviderFilterListAPI(ProviderBaseFilterMixin, ListAPIView):
    serializer_class = ServiceProviderSerializer
    queryset = ServiceProvider.objects.all().order_by("-id")

    def get_queryset(self):
        qs = super().get_queryset()
        return self.apply_filters(qs, self.request.query_params)



#   CSV EXPORT OF THE PROVIDER LIST VIEWSET-----




class ProviderExportCSVAPI(ProviderBaseFilterMixin, APIView):

    def get(self, request):
        qs = ServiceProvider.objects.all()
        qs = self.apply_filters(qs, request.query_params)

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="service_providers.csv"'

        writer = csv.writer(response)
        writer.writerow([
            "SP Code", "Center Name", "Status", "Active",
            "City", "State",
            "Client Companies", "Specialties"
        ])

        for obj in qs:
            writer.writerow([
                obj.sp_code,
                obj.center_name,
                obj.status,
                obj.is_active,
                obj.city.name if obj.city else "",
                obj.state.name if obj.state else "",
                ", ".join(obj.client_company.values_list("name", flat=True)),
                ", ".join(obj.medical_specialties.values_list("name", flat=True)),
            ])

        return response




# EXCEL EXPORT OF PROVIDER LIST ------


from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from django.http import HttpResponse
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from .models import ServiceProvider


class ProviderExportExcelAPI(ProviderBaseFilterMixin, APIView):

    def get(self, request):
        qs = ServiceProvider.objects.all()
        qs = self.apply_filters(qs, request.query_params)

        wb = Workbook()
        ws = wb.active
        ws.title = "Service Providers"

        headers = [
            "SP Code", "Center Name", "Status", "Active",
            "City", "State",
            "Client Companies", "Specialties"
        ]
        ws.append(headers)

        for obj in qs:
            ws.append([
                obj.sp_code,
                obj.center_name,
                obj.status,
                obj.is_active,
                obj.city.name if obj.city else "",
                obj.state.name if obj.state else "",
                ", ".join(obj.client_company.values_list("name", flat=True)),
                ", ".join(obj.medical_specialties.values_list("name", flat=True)),
            ])

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename="service_providers.xlsx"'
        wb.save(response)
        return response



# SEND LINK TO PROVIDER FILTER----

from rest_framework.generics import ListAPIView
from apps.service_provider.models import ServiceProvider
from apps.service_provider.serializers import ServiceProviderSerializer

class ServiceProviderFilterAPI(ListAPIView):
    serializer_class = ServiceProviderSerializer
    queryset = ServiceProvider.objects.all().order_by("-id")

    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params

        center_name = params.get("center_name")
        sp_code = params.get("sp_code")
        status = params.get("status")

        if center_name:
            qs = qs.filter(center_name__icontains=center_name)

        if sp_code:
            qs = qs.filter(sp_code__icontains=sp_code)

        if status:
            status_list = [s.strip() for s in status.split(",")]
            qs = qs.filter(status__in=status_list)

        return qs


# SEND LINK FOR PERTICULAR PROVIDER----


class SendProviderLinkAPI(APIView):

    def post(self, request, provider_id):
        try:
            provider = ServiceProvider.objects.get(id=provider_id)
        except ServiceProvider.DoesNotExist:
            return Response(
                {"error": "Service Provider not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # --------------------
        # Generate unique link
        # --------------------
        token = uuid.uuid4()
        link = f"https://live.welleazy.com/provider-registration/{token}"

        ProviderRegistrationLink.objects.create(
            provider=provider,
            token=token,
            generated_link=link,
            created_by=request.user,
            updated_by=request.user
        )

        # --------------------
        # Send EMAIL
        # --------------------
        send_mail(
            subject="Complete Your Provider Registration",
            message=(
                f"Dear {provider.center_name},\n\n"
                f"Please complete your registration using the link below:\n\n"
                f"{link}\n\n"
                f"Regards,\nWelleazy Team"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[provider.email],
            fail_silently=True,
        )

        # --------------------
        # Send SMS (Twilio)
        # --------------------
        sms_status = "sent"
        try:
            client = Client(
                settings.TWILIO_ACCOUNT_SID,
                settings.TWILIO_AUTH_TOKEN
            )

            client.messages.create(
                body=f"Welleazy Registration Link: {link}",
                from_=settings.TWILIO_PHONE_NUMBER,
                to=f"+91{provider.mobile}"
            )
        except Exception as e:
            sms_status = f"failed: {str(e)}"

        return Response({
            "message": "Registration link generated",
            "provider_id": provider.id,
            "center_name": provider.center_name,
            "email": provider.email,
            "mobile": provider.mobile,
            "sms_status": sms_status,
            "link": link
        }, status=status.HTTP_200_OK)



# DISCOUNT VIEW-----


class DiscountFilterListAPI(ListAPIView):
    serializer_class = DiscountListSerializer

    def get_queryset(self):
        qs = ProviderDiscount.objects.select_related(
            "provider",
            "provider__city",
            "provider__state",
            "discount_service"
        ).prefetch_related(
            "provider__client_company"
        )

        client_ids = self.request.query_params.get("client_ids")
        provider_ids = self.request.query_params.get("provider_ids")
        discount_service_ids = self.request.query_params.get("discount_service_ids")
        city_ids = self.request.query_params.get("city_ids")
        discount_percent = self.request.query_params.get("discount_percent")

        if client_ids:
            qs = qs.filter(
                provider__client_company__id__in=client_ids.split(",")
            )

        if provider_ids:
            qs = qs.filter(
                provider_id__in=provider_ids.split(",")
            )

        if discount_service_ids:
            qs = qs.filter(
                discount_service_id__in=discount_service_ids.split(",")
            )

        if city_ids:
            qs = qs.filter(
                provider__city_id__in=city_ids.split(",")
            )

        if discount_percent:
            qs = qs.filter(
                discount_percent=discount_percent
            )

        return qs.distinct()



# DISCOUNT VIEW CSV EXPORT----



class DiscountExportCSVAPI(APIView):

    def get(self, request):
        qs = ProviderDiscount.objects.select_related(
            "provider",
            "provider__city",
            "provider__state",
            "discount_service"
        ).prefetch_related(
            "provider__client_company"
        )

        client_ids = request.query_params.get("client_ids")
        provider_ids = request.query_params.get("provider_ids")
        discount_service_ids = request.query_params.get("discount_service_ids")
        city_ids = request.query_params.get("city_ids")
        discount_percent = request.query_params.get("discount_percent")

        if client_ids:
            qs = qs.filter(provider__client_company__id__in=client_ids.split(","))

        if provider_ids:
            qs = qs.filter(provider_id__in=provider_ids.split(","))

        if discount_service_ids:
            qs = qs.filter(discount_service_id__in=discount_service_ids.split(","))

        if city_ids:
            qs = qs.filter(provider__city_id__in=city_ids.split(","))

        if discount_percent:
            qs = qs.filter(discount_percent=discount_percent)

        qs = qs.distinct()

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="discount_report.csv"'

        writer = csv.writer(response)
        writer.writerow([
            "Discount Service",
            "Discount %",
            "DC Logo",
            "DC Photo",
            "DC Name",
            "Address",
            "Area",
            "City",
            "State",
            "Provider Status"
        ])

        for obj in qs:
            provider = obj.provider
            docs = getattr(provider, "documents", None)

            writer.writerow([
                obj.discount_service.name,
                obj.discount_percent,
                docs.dc_logo.url if docs and docs.dc_logo else "",
                docs.dc_photo.url if docs and docs.dc_photo else "",
                provider.center_name,
                provider.address,
                provider.area,
                provider.city.name if provider.city else "",
                provider.state.name if provider.state else "",
                provider.status,
            ])

        return response
    

# VOUCHER VIEW FILTER----



class VoucherFilterListAPI(ListAPIView):
    serializer_class = VoucherListSerializer

    def get_queryset(self):
        qs = ProviderVoucher.objects.select_related(
            "provider", "provider__city", "voucher_discount"
        ).all()

        qp = self.request.query_params

        provider_ids = qp.get("provider_ids")
        voucher_discount_ids = qp.get("voucher_discount_ids")
        discount_percent = qp.get("discount_percent")
        city_ids = qp.get("city_ids")
        voucher_status = qp.get("voucher_status")

        if provider_ids:
            qs = qs.filter(provider_id__in=provider_ids.split(","))

        if voucher_discount_ids:
            qs = qs.filter(voucher_discount_id__in=voucher_discount_ids.split(","))

        if discount_percent:
            qs = qs.filter(discount_percent=discount_percent)

        if city_ids:
            qs = qs.filter(provider__city_id__in=city_ids.split(","))

        if voucher_status:
            qs = qs.filter(Voucher_status__in=voucher_status.split(","))

        return qs.order_by("-id")
    

# VOUCHER VIEW CSV EXPORT----


class VoucherExportCSV(APIView):

    def get(self, request):
        qs = ProviderVoucher.objects.select_related(
            "provider", "provider__city", "voucher_discount"
        ).all()

        qp = request.query_params

        if qp.get("provider_ids"):
            qs = qs.filter(provider_id__in=qp["provider_ids"].split(","))

        if qp.get("voucher_discount_ids"):
            qs = qs.filter(voucher_discount_id__in=qp["voucher_discount_ids"].split(","))

        if qp.get("discount_percent"):
            qs = qs.filter(discount_percent=qp["discount_percent"])

        if qp.get("city_ids"):
            qs = qs.filter(provider__city_id__in=qp["city_ids"].split(","))

        if qp.get("voucher_status"):
            qs = qs.filter(Voucher_status__in=qp["voucher_status"].split(","))

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="voucher_list.csv"'

        writer = csv.writer(response)
        writer.writerow([
            "Voucher Added Date",
            "Voucher ID",
            "Voucher Code",
            "Voucher Discount Type",
            "Discount %",
            "DC Name",
            "City",
            "Start Date",
            "Expiry Date",
            "Voucher Status",
        ])

        for v in qs:
            writer.writerow([
                v.voucher_added_date,
                v.voucher_id,
                v.voucher_code,
                v.voucher_discount.name if v.voucher_discount else "",
                v.discount_percent,
                v.provider.center_name,
                v.provider.city.name if v.provider.city else "",
                v.start_date,
                v.expiry_date,
                v.Voucher_status,
            ])

        return response
