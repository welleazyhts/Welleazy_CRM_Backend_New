from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProviderDocumentViewSet, ProviderFilterListAPI, ProviderLinkRequestViewSet, ServiceProviderViewSet , ProviderExportCSVAPI , ProviderExportExcelAPI , ServiceProviderFilterAPI , SendProviderLinkAPI,DiscountFilterListAPI , DiscountExportCSVAPI , VoucherFilterListAPI , VoucherExportCSV

router = DefaultRouter()
router.register("service-provider", ServiceProviderViewSet, basename="service-provider")
router.register("documents", ProviderDocumentViewSet, basename="provider-documents")
router.register("generate-link",ProviderLinkRequestViewSet,basename="provider-registration-link")


urlpatterns = [
    path("list/", ProviderFilterListAPI.as_view(), name="provider-filter-list"),
    path("export-csv/", ProviderExportCSVAPI.as_view(), name="export-service-provider-csv"),
    path("export-excel/", ProviderExportExcelAPI.as_view(), name="export-service-provider-excel"),
    path("provider/list/", ServiceProviderFilterAPI.as_view() , name="provider-filter-for-link"),
    path("provider/<int:provider_id>/send-link/",SendProviderLinkAPI.as_view(),name="send-provider-link"),
    path("discount/filter/", DiscountFilterListAPI.as_view() , name="discount-view"),
    path("discount/exportcsv/",DiscountExportCSVAPI.as_view() , name="discount-view-exportcsv"),
    path("voucher/filter/", VoucherFilterListAPI.as_view(), name="voucher-filter"),
    path("voucher/exportcsv/", VoucherExportCSV.as_view(), name="voucher-export-csv"),
]

urlpatterns += router.urls