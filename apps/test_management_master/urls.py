from rest_framework.routers import DefaultRouter
from .views import *



router = DefaultRouter()

router.register("test-types", TestTypeViewSet)
router.register("health-concerns", HealthConcernTypeViewSet)
router.register("plan-category", PlanCategoryViewSet)
router.register("checkup-type", CheckUpTypeViewSet)
router.register("gender", GenderViewSet)

urlpatterns = router.urls