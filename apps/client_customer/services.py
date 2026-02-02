from django.db import transaction
from .models import ClientCustomer, ClientCustomerAddress, ClientCustomerDependent
from apps.master_management.models import MasterProductSubCategory, MasterRelationship

class ClientCustomerService:
    @staticmethod
    @transaction.atomic
    def upsert_customer(user, data, instance=None):
        #Creates or updates a ClientCustomer along with nested addresses and dependents.
        addresses_data = data.pop('addresses', None)
        dependents_data = data.pop('dependents', None)
        services_data = data.pop('services', None)
        packages_data = data.pop('packages', [])

        fk_fields = ['client', 'branch', 'product', 'gender', 'state', 'city']
        processed_data = {}
        for k, v in data.items():
            if k in fk_fields and isinstance(v, int):
                processed_data[f"{k}_id"] = v
            else:
                processed_data[k] = v

        # Create or update instance
        is_new = instance is None
        if is_new:
            instance = ClientCustomer.objects.create(created_by=user, updated_by=user, **processed_data)
        else:
            for attr, value in processed_data.items():
                setattr(instance, attr, value)
            instance.updated_by = user
            instance.save()

        # Handle Many-to-Many services
        if services_data is not None:
            instance.services.set(services_data)
        
        # Handle Many-to-Many packages
        if packages_data:
            instance.packages.set(packages_data)
        
        # Handle nested Addresses - Always run on creation to ensure "Self" record
        if addresses_data is not None or is_new:
            if addresses_data is None:
                addresses_data = []
            default_self_address = ClientCustomerService._sync_addresses(instance, addresses_data)
            
            # Sync "Self" default address back to main customer fields
            if default_self_address:
                instance.state = default_self_address.state
                instance.city = default_self_address.city
                instance.area_locality = default_self_address.area_locality
                instance.landmark = default_self_address.landmark
                instance.pincode = default_self_address.pincode
                instance.save()

        # Handle nested Dependents
        if dependents_data is not None:
            ClientCustomerService._sync_dependents(instance, dependents_data)

        return instance

    @staticmethod
    def _sync_addresses(customer, addresses_data):
        existing_ids = []
        default_self_address = None

        self_rel, _ = MasterRelationship.objects.get_or_create(name='Self')

        has_self_in_payload = any(
            addr.get('relation_type') == self_rel.id 
            for addr in addresses_data
        )

        if not has_self_in_payload:
            existing_self = customer.addresses.filter(relation_type=self_rel).first()
            
            self_entry = {
                "address_type": "Home",
                "state": customer.state_id,
                "city": customer.city_id,
                "area_locality": customer.area_locality,
                "landmark": customer.landmark,
                "pincode": customer.pincode,
                "relation_type": self_rel.id,
                "is_default": True
            }
            if existing_self:
                self_entry["id"] = existing_self.id
            
            if any([self_entry["state"], self_entry["city"], self_entry["pincode"]]):
                addresses_data.append(self_entry)

        for addr_data in addresses_data:
            addr_id = addr_data.get('id')
            addr_instance = None
            if addr_id:
                # Update existing address
                addr_instance = ClientCustomerAddress.objects.get(id=addr_id, customer=customer)
                for attr, value in addr_data.items():
                    if attr == 'id': continue
                    if attr in ['state', 'city', 'relation_type'] and isinstance(value, int):
                        setattr(addr_instance, f"{attr}_id", value)
                    else:
                        setattr(addr_instance, attr, value)
                addr_instance.save()
                existing_ids.append(addr_id)
            else:
                # Create new address
                processed_data = {}
                for k, v in addr_data.items():
                    if k in ['state', 'city', 'relation_type'] and isinstance(v, int):
                        processed_data[f"{k}_id"] = v
                    else:
                        processed_data[k] = v
                addr_instance = ClientCustomerAddress.objects.create(customer=customer, **processed_data)
                existing_ids.append(addr_instance.id)
            
            # Track default self address for syncing back to parent
            if addr_instance and addr_instance.is_default and addr_instance.relation_type and addr_instance.relation_type.name.upper() == 'SELF':
                default_self_address = addr_instance
        
        # Delete addresses not in the provided data
        customer.addresses.exclude(id__in=existing_ids).delete()
        
        return default_self_address

    @staticmethod
    def _sync_dependents(customer, dependents_data):
        existing_ids = []
        for dep_data in dependents_data:
            dep_id = dep_data.get('id')
            if dep_id:
                # Update existing dependent
                dep_instance = ClientCustomerDependent.objects.get(id=dep_id, customer=customer)
                for attr, value in dep_data.items():
                    if attr == 'id': continue
                    if attr in ['relationship', 'gender'] and isinstance(value, int):
                        setattr(dep_instance, f"{attr}_id", value)
                    else:
                        setattr(dep_instance, attr, value)
                dep_instance.save()
                existing_ids.append(dep_id)
            else:
                # Create new dependent
                processed_data = {}
                for k, v in dep_data.items():
                    if k in ['relationship', 'gender'] and isinstance(v, int):
                        processed_data[f"{k}_id"] = v
                    else:
                        processed_data[k] = v
                dep_instance = ClientCustomerDependent.objects.create(customer=customer, **processed_data)
                existing_ids.append(dep_instance.id)

        # Delete dependents not in the provided data
        customer.dependents.exclude(id__in=existing_ids).delete()
