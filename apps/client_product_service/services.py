from django.db import transaction
from .models import ClientProductService
from apps.master_management.models import MasterProduct, MasterProductSubCategory, ServiceMapping
from apps.client.models import Client
from apps.client_branch.models import ClientBranch

class ClientProductServiceService:
    @staticmethod
    def get_grouped_mappings(queryset):

        grouped_data = {}
        for item in queryset:
            key = (item.client_id, item.branch_id)
            if key not in grouped_data:
                grouped_data[key] = {
                    "client_id": item.client_id,
                    "client_name": item.client.corporate_name,
                    "branch_id": item.branch_id,
                    "branch_name": item.branch.branch_name if item.branch else "Corporate/All",
                    "login_type_id": item.login_type_id,
                    "login_type_name": item.login_type.name if item.login_type else None,
                    "is_active": item.is_active,
                    "updated_at": item.updated_at,
                    "products": []
                }
            
            grouped_data[key]["products"].append({
                "product_id": item.product_id,
                "product_name": item.product.name,
                "services": [
                    {"id": s.id, "name": s.name} for s in item.services.all()
                ]
            })
        return list(grouped_data.values())

    @staticmethod
    @transaction.atomic
    def synchronize_mappings(user, client_id, branch_ids, product_ids, service_ids, login_type_id, is_active):

        stats = {"added": 0, "updated": 0, "removed": 0, "unchanged": 0}
        created_instances = []
        
        service_map_dict = {}
        mappings = ServiceMapping.objects.filter(product_id__in=product_ids).prefetch_related('sub_products')
        for mapping in mappings:
            service_map_dict[mapping.product_id] = set(mapping.sub_products.values_list('id', flat=True))

        if not branch_ids:
            branch_ids = [None]

        for branch_id in branch_ids:
            to_delete = ClientProductService.objects.filter(
                client_id=client_id,
                branch_id=branch_id
            ).exclude(product_id__in=product_ids)
            stats["removed"] += to_delete.count()
            to_delete.delete()

            for product_id in product_ids:
                allowed_service_ids = service_map_dict.get(product_id, set())
                valid_service_ids = [s_id for s_id in service_ids if s_id in allowed_service_ids]

                existing_qs = ClientProductService.objects.filter(
                    client_id=client_id,
                    branch_id=branch_id,
                    product_id=product_id
                )
                
                if existing_qs.exists():
                    instance = existing_qs.first()
                    
                    current_service_ids = set(instance.services.values_list('id', flat=True))
                    new_service_ids = set(valid_service_ids)
                    
                    was_changed = (
                        current_service_ids != new_service_ids or 
                        instance.login_type_id != login_type_id or
                        instance.is_active != is_active
                    )

                    if was_changed:
                        instance.login_type_id = login_type_id
                        instance.is_active = is_active
                        instance.updated_by = user
                        instance.save()
                        instance.services.set(valid_service_ids)
                        stats["updated"] += 1
                    else:
                        stats["unchanged"] += 1
                    
                    # Cleanup duplicates
                    if existing_qs.count() > 1:
                        existing_qs.exclude(id=instance.id).delete()
                else:
                    instance = ClientProductService.objects.create(
                        client_id=client_id,
                        branch_id=branch_id,
                        product_id=product_id,
                        login_type_id=login_type_id,
                        is_active=is_active,
                        created_by=user,
                        updated_by=user
                    )
                    instance.services.set(valid_service_ids)
                    stats["added"] += 1
                
                created_instances.append(instance)

        return stats, created_instances

    @staticmethod
    def prepare_update_data(instance, data):

        product_id = data.get('product')
        if not product_id and data.get('product_ids'):
            product_id = data.get('product_ids')[0] if isinstance(data.get('product_ids'), list) else data.get('product_ids')
        
        branch_id = data.get('branch')
        if not branch_id and data.get('branch_ids'):
            branch_id = data.get('branch_ids')[0] if isinstance(data.get('branch_ids'), list) else data.get('branch_ids')

        service_ids = data.get('services')
        if service_ids is None and data.get('service_ids'):
            service_ids = data.get('service_ids')

        final_product_id = product_id if product_id else instance.product_id
        
        if service_ids is not None:
            mapping = ServiceMapping.objects.filter(product_id=final_product_id).first()
            if mapping:
                allowed_service_ids = set(mapping.sub_products.values_list('id', flat=True))
                valid_service_ids = [s_id for s_id in service_ids if s_id in allowed_service_ids]
                
                if service_ids and not valid_service_ids:
                     return None, f"None of the provided services are mapped to Product ID {final_product_id} in Master Management."
                
                data['services'] = valid_service_ids
            else:
                if service_ids:
                    return None, f"Product ID {final_product_id} has no services mapped in Master Management."

        if product_id:
            data['product'] = product_id
        if branch_id:
            data['branch'] = branch_id

        return data, None
