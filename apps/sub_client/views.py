from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import SubClient, SubClientSPOC
from .serializers import SubClientSerializer
from .filters import SubClientFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction

class SubClientViewSet(viewsets.ModelViewSet):
    queryset = SubClient.objects.select_related(
        'client', 'corporate_type', 'created_by', 'updated_by'
    ).prefetch_related('spocs').all().order_by("-created_at")
    serializer_class = SubClientSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = SubClientFilter
    search_fields = ['name', 'mobile_no', 'email_id', 'client__corporate_name']
    ordering_fields = ['created_at', 'name']

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = SubClientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data

        sub_client = SubClient(
            created_by=request.user if request.user.is_authenticated else None,
            updated_by=request.user if request.user.is_authenticated else None,
        )

        self._save_sub_client_fields(sub_client, validated)
        sub_client.save()

        self._save_spocs(sub_client, validated)
        
        sub_client = self.get_queryset().get(id=sub_client.id)

        return Response(
            {
                "message": "Sub Client created successfully",
                "data": SubClientSerializer(sub_client).data
            },
            status=status.HTTP_201_CREATED
        )

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        sub_client = self.get_object()
        serializer = SubClientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data

        sub_client.updated_by = request.user if request.user.is_authenticated else None
        self._save_sub_client_fields(sub_client, validated)
        sub_client.save()

        self._save_spocs(sub_client, validated)

        sub_client = self.get_queryset().get(id=sub_client.id)

        return Response(
            {
                "message": "Sub Client updated successfully",
                "data": SubClientSerializer(sub_client).data
            },
            status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Sub Client deleted successfully"},
            status=status.HTTP_200_OK
        )

    # HELPER METHODS

    def _save_sub_client_fields(self, sub_client, validated):
        simple_fields = [
            'name', 'mobile_no', 'landline_no', 'email_id',
            'head_office_address', 'branch_office_address',
            'source', 'lead_by', 'is_active'
        ]
        
        for field in simple_fields:
            if field in validated:
                setattr(sub_client, field, validated[field])
        
        fk_fields = ['client', 'corporate_type']
        for field in fk_fields:
            if field in validated:
                setattr(sub_client, field, validated[field])

    def _save_spocs(self, sub_client, validated):
        if "spocs" not in validated:
            return

        spocs_data = validated["spocs"]
        keep_ids = []

        for spoc_data in spocs_data:
            spoc_id = spoc_data.get("id")

            if spoc_id:
                spoc = SubClientSPOC.objects.filter(
                    id=spoc_id,
                    sub_client=sub_client
                ).first()

                if not spoc:
                    from rest_framework.exceptions import ValidationError
                    raise ValidationError({
                        "spocs": f"Invalid SPOC id {spoc_id} for this sub client"
                    })

                for field, value in spoc_data.items():
                    setattr(spoc, field, value)

                spoc.updated_by = sub_client.updated_by
                spoc.save()
                keep_ids.append(spoc.id)

            else:
                spoc = SubClientSPOC.objects.create(
                    sub_client=sub_client,
                    created_by=sub_client.created_by,
                    updated_by=sub_client.updated_by,
                    **spoc_data
                )
                keep_ids.append(spoc.id)

        SubClientSPOC.objects.filter(
            sub_client=sub_client
        ).exclude(id__in=keep_ids).delete()

    @action(detail=True, methods=["delete"], url_path="spocs/delete")
    def delete_spoc(self, request, pk=None):
        sub_client = self.get_object()
        
        spoc_id = request.data.get('spoc_id') or request.query_params.get('spoc_id')
        if not spoc_id:
            return Response({"spoc_id": "This field is required"}, status=400)
        
        try:
            spoc = sub_client.spocs.get(id=spoc_id)
            spoc.delete()
            return Response({"message": "SPOC deleted successfully"}, status=200)
        except SubClientSPOC.DoesNotExist:
            return Response({"error": "SPOC not found"}, status=404)
