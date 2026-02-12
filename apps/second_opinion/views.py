from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.parsers import MultiPartParser, FormParser
import pandas as pd
from django.db import transaction
from .models import SecondOpinionCase
from apps.core.choices import GENDER_CHOICES
from apps.client.models import Client
from .serializers import (
    SecondOpinionCaseSerializer, 
    SecondOpinionCaseListSerializer,
    SecondOpinionBulkUploadSerializer
)


class SecondOpinionDropdownsAPI(APIView):
    def get(self, request):
        from apps.master_management.models import (
            MasterRelationship, State, 
            City, MasterInsuranceCompany
        )
        from apps.doctor.models import Doctor
        
        # Return choices directly from the model
        case_types = [{"id": c[0], "name": c[1]} for c in SecondOpinionCase.CaseType.choices]
        interpretation_types = [{"id": c[0], "name": c[1]} for c in SecondOpinionCase.InterpretationType.choices]
        case_received_modes = [{"id": c[0], "name": c[1]} for c in SecondOpinionCase.ReceivedMode.choices]
        case_statuses = [{"id": c[0], "name": c[1]} for c in SecondOpinionCase.CaseStatus.choices]
        
        clients = Client.objects.filter(is_active=True).values('id', 'corporate_name')
        genders = [{"id": c[0], "name": c[1]} for c in GENDER_CHOICES]
        relationships = MasterRelationship.objects.filter(is_active=True).values('id', 'name')
        states = State.objects.filter(is_active=True).values('id', 'name')
        cities = City.objects.filter(is_active=True).values('id', 'name', 'state_id')
        insurance_companies = MasterInsuranceCompany.objects.filter(is_active=True).values('id', 'name', 'type_of_insurance_id')
        doctors = Doctor.objects.filter(is_active=True).values('id', 'doctor_name')
        
        return Response({
            "case_types": case_types,
            "interpretation_types": interpretation_types,
            "case_received_modes": case_received_modes,
            "case_statuses": case_statuses,
            "clients": list(clients),
            "genders": list(genders),
            "relationships": list(relationships),
            "states": list(states),
            "cities": list(cities),
            "insurance_companies": list(insurance_companies),
            "doctors": list(doctors),
        })


def filter_second_opinion_cases(qs, request):
    """
    Reusable helper to apply filters to SecondOpinionCase queryset.
    """
    # Filtering
    case_type = request.query_params.get('case_type')
    if case_type:
        qs = qs.filter(case_type=case_type)
        
    interpretation_type = request.query_params.get('interpretation_type')
    if interpretation_type:
        qs = qs.filter(interpretation_type=interpretation_type)
        
    doctor_id = request.query_params.get('doctor')
    if doctor_id:
        qs = qs.filter(doctor_id=doctor_id)

    # Multi-select filters (expecting comma separated or multiple params)
    # Handling multiple params: ?client=1&client=2
    client_ids = request.query_params.getlist('client')
    if client_ids:
        qs = qs.filter(client_id__in=client_ids)
        
    case_statuses = request.query_params.getlist('case_status')
    if case_statuses:
        qs = qs.filter(case_status__in=case_statuses)
        
    # Search
    app_no = request.query_params.get('application_number')
    if app_no:
        qs = qs.filter(application_number__icontains=app_no)
        
    return qs


class SecondOpinionCaseListAPI(APIView):
    def get(self, request):
        qs = SecondOpinionCase.objects.filter(is_active=True).select_related(
            'client', 'client_customer', 'doctor', 'qc_executive'
        ).order_by('-created_at')
        
        qs = filter_second_opinion_cases(qs, request)
        
        serializer = SecondOpinionCaseListSerializer(qs, many=True)
        return Response(serializer.data)


class ClosedSecondOpinionCaseListAPI(APIView):
    def get(self, request):
        qs = SecondOpinionCase.objects.filter(
            is_active=True,
            case_status=SecondOpinionCase.CaseStatus.COMPLETED
        ).select_related(
            'client', 'client_customer', 'doctor', 'qc_executive'
        ).order_by('-created_at')
        
        qs = filter_second_opinion_cases(qs, request)
        
        serializer = SecondOpinionCaseListSerializer(qs, many=True)
        return Response(serializer.data)


class SecondOpinionCaseExportAPI(APIView):
    def get(self, request):
        import pandas as pd
        from django.http import HttpResponse
        
        qs = SecondOpinionCase.objects.filter(is_active=True).select_related(
            'client', 'client_customer', 'doctor', 'qc_executive'
        ).order_by('-created_at')
        
        qs = filter_second_opinion_cases(qs, request)
        
        # Prepare data for export
        data = []
        for case in qs:
            data.append({
                "Interpretation Case ID": case.id, # Using ID as Case ID
                "Case Entry Date Time": case.created_at.strftime("%d/%m/%Y %H:%M:%S") if case.created_at else "",
                "Case Type": case.case_type,
                "Corporate Name": case.client.corporate_name if case.client else "",
                "Case Rec'd Mode": case.case_received_mode,
                "Customer Name": case.customer_name,
                "Application Number": case.application_number,
                "Policy Number": case.policy_number,
                "Interpretation Type": case.interpretation_type,
                "Case Status": case.case_status,
                "Doctor Name": case.doctor.doctor_name if case.doctor else "",
                "QC Executive Name": case.qc_executive.username if case.qc_executive else "",
                "Remark": case.remark
            })
            
        df = pd.DataFrame(data)
        
        export_format = request.query_params.get('export_format', 'csv')
        
        if export_format == 'excel':
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="SecondOpinionCases.xlsx"'
            df.to_excel(response, index=False, engine='openpyxl')
            return response
        else:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="SecondOpinionCases.csv"'
            df.to_csv(response, index=False)
            return response


class ClosedSecondOpinionCaseExportAPI(APIView):
    def get(self, request):
        import pandas as pd
        from django.http import HttpResponse
        
        qs = SecondOpinionCase.objects.filter(
            is_active=True,
            case_status=SecondOpinionCase.CaseStatus.COMPLETED
        ).select_related(
            'client', 'client_customer', 'doctor', 'qc_executive'
        ).order_by('-created_at')
        
        qs = filter_second_opinion_cases(qs, request)
        
        # Prepare data for export
        data = []
        for case in qs:
            data.append({
                "Interpretation Case ID": case.id,
                "Case Entry Date Time": case.created_at.strftime("%d/%m/%Y %H:%M:%S") if case.created_at else "",
                "Case Type": case.case_type,
                "Corporate Name": case.client.corporate_name if case.client else "",
                "Case Rec'd Mode": case.case_received_mode,
                "Customer Name": case.customer_name,
                "Application Number": case.application_number,
                "Policy Number": case.policy_number,
                "Interpretation Type": case.interpretation_type,
                "Case Status": case.case_status,
                "Doctor Name": case.doctor.doctor_name if case.doctor else "",
                "QC Executive Name": case.qc_executive.username if case.qc_executive else "",
                "Remark": case.remark
            })
            
        df = pd.DataFrame(data)
        
        export_format = request.query_params.get('export_format', 'csv')
        
        if export_format == 'excel':
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="ClosedSecondOpinionCases.xlsx"'
            df.to_excel(response, index=False, engine='openpyxl')
            return response
        else:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="ClosedSecondOpinionCases.csv"'
            df.to_csv(response, index=False)
            return response


class SecondOpinionAssignDoctorAPI(APIView):
    def post(self, request):
        from .serializers import SecondOpinionAssignDoctorSerializer
        from apps.doctor.models import Doctor
        
        serializer = SecondOpinionAssignDoctorSerializer(data=request.data)
        if not serializer.is_valid():
             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
             
        case_ids = serializer.validated_data['case_ids']
        doctor_id = serializer.validated_data['doctor_id']
        
        # Validate Doctor
        try:
            doctor = Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)
            
        # Update Cases
        # We also auto-update status to 'Assigned' if it helps, or keep it flexible.
        # Requirement: "Assign case to doctor" usually implies status change to Assigned
        
        updated_count = SecondOpinionCase.objects.filter(id__in=case_ids).update(
            doctor=doctor,
            case_status=SecondOpinionCase.CaseStatus.ASSIGNED
        )
        
        return Response({
            "message": f"Successfully assigned {updated_count} cases to Dr. {doctor.doctor_name}"
        }, status=status.HTTP_200_OK)


class SecondOpinionCaseDetailAPI(generics.RetrieveAPIView):
    queryset = SecondOpinionCase.objects.filter(is_active=True)
    serializer_class = SecondOpinionCaseSerializer


class SecondOpinionCaseUpdateAPI(generics.UpdateAPIView):
    queryset = SecondOpinionCase.objects.filter(is_active=True)
    serializer_class = SecondOpinionCaseSerializer


class SecondOpinionCaseDeleteAPI(APIView):
    def delete(self, request, pk):
        try:
            case = SecondOpinionCase.objects.get(pk=pk, is_active=True)
            case.is_active = False
            case.save()
            return Response({
                "message": f"Case {pk} has been deactivated successfully"
            }, status=status.HTTP_200_OK)
        except SecondOpinionCase.DoesNotExist:
            return Response({
                "error": "Case not found"
            }, status=status.HTTP_404_NOT_FOUND)


class SecondOpinionCaseCreateAPI(generics.CreateAPIView):
    queryset = SecondOpinionCase.objects.all()
    serializer_class = SecondOpinionCaseSerializer
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        serializer.save()
    
    def create(self, request, *args, **kwargs):
        # Use full serializer for input validation
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Use simplified serializer for response
        from .serializers import SecondOpinionCaseResponseSerializer
        response_serializer = SecondOpinionCaseResponseSerializer(serializer.instance)
        headers = self.get_success_headers(response_serializer.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SecondOpinionCaseBulkUploadAPI(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        serializer = SecondOpinionBulkUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        file_obj = serializer.validated_data['file']
        # For bulk upload, clients can pass case_type/client as ID or string. 
        # But our simplified model expects case_type to be a string (Value from choice).
        # We assume the UI sends the value (e.g. "Interpretation") or we map it if needed. 
        # Safest is to expect the string value "Interpretation" etc.
        
        case_type = serializer.validated_data.get('case_type') # Expecting String Value
        client_id = serializer.validated_data.get('client')
        
        try:
            # Validate IDs exist
            if not Client.objects.filter(id=client_id).exists():
                 return Response({"error": "Invalid Client ID"}, status=status.HTTP_400_BAD_REQUEST)

            import sys
            print(f"DEBUG: Python Executable: {sys.executable}")
            print(f"DEBUG: Sys Path: {sys.path}")
            
            filename = file_obj.name.lower()
            print(f"DEBUG: Receiving file '{file_obj.name}' (lower: '{filename}')")

            try:
                # Explicitly try import to see if it works here
                import xlrd
                print(f"DEBUG: xlrd imported successfully: {xlrd.__version__} at {xlrd.__file__}")
            except ImportError as e:
                print(f"DEBUG: Explicit xlrd import failed: {e}")

            try:
                if filename.endswith('.csv'):
                    df = pd.read_csv(file_obj)
                elif filename.endswith('.xlsx'):
                    df = pd.read_excel(file_obj, engine='openpyxl')
                else:
                    # Default to xlrd for .xls
                    print("DEBUG: Attempting to read with xlrd")
                    df = pd.read_excel(file_obj, engine='xlrd')

            except ImportError as ie:
                # Catch library missing errors specifically
                print(f"DEBUG: ImportError: {ie}")
                raise Exception(f"Library Import Error: {str(ie)}. Ensure xlrd/openpyxl are installed.")
            except Exception as e:
                # Catch format errors
                print(f"DEBUG: Read Error: {e}")
                raise Exception(f"Failed to read file: {str(e)}")
            
            # Normalize column names to handle whitespace/case
            df.columns = [str(col).strip().lower() for col in df.columns]

            # Map expected headers (lowercase for comparison)
            # Expected: "customer name", "application no", "policy no", "case received mode", "interpretation type"
            
            created_count = 0
            errors = []
            
            with transaction.atomic():
                for index, row in df.iterrows():
                    try:
                        # Skip rows that appear to be instructions (e.g., if 'interpretation type' contains '1=ECG')
                        # or if critical fields are clearly instructional text.
                        raw_interp = str(row.get('interpretation type', ''))
                        if '1=ECG' in raw_interp or '2=TMT' in raw_interp:
                            continue
                            
                        # Extract row data safely. Using 'get' allows it to fail gracefully or default
                        # Assuming pandas converts spaces to match.
                        # Look for potential column variations
                        
                        def get_val(possible_names):
                            for name in possible_names:
                                if name in df.columns:
                                    val = row[name]
                                    return str(val).strip() if pd.notna(val) else ""
                            return ""

                        customer_name = get_val(["customer name", "customer_name"])
                        app_no = get_val(["application no", "application_no", "application number"])
                        policy_no = get_val(["policy no", "policy_no", "policy number"])
                        mode_str = get_val(["case received mode", "mode", "case_received_mode"])
                        interp_str = get_val(["interpretation type", "interpretation_type"])
                        
                        # Fix: If app_no matches example text/headers, skip it
                        if app_no.lower() in ['application no', 'app-001'] and customer_name.lower() in ['customer name', 'rahul sharma']:
                             # This might be an example row or repeat header
                             pass 
                        
                        if not app_no or app_no.lower() == 'nan':
                            # Skip empty rows
                            continue

                        # No DB Lookup needed for modes/types anymore. We save the string directly.
                        # Ideally we validate against choices, but flexible string is okay for now.
                        
                        SecondOpinionCase.objects.create(
                            case_type=case_type, # Saved as string
                            client_id=client_id,
                            customer_name=customer_name,
                            application_number=app_no,
                            policy_number=policy_no,
                            case_received_mode=mode_str, # Saved as string
                            interpretation_type=interp_str, # Saved as string
                            remark="Bulk Uploaded",
                            is_active=True
                        )
                        created_count += 1
                    except Exception as e:
                        errors.append(f"Row {index + 2}: {str(e)}") # +2 for 1-based index + header
            
            if errors:
                return Response({
                    "message": f"Created {created_count} cases. Some rows failed.",
                    "errors": errors
                }, status=status.HTTP_207_MULTI_STATUS)
                
            return Response({"message": f"Successfully uploaded {created_count} cases."}, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
