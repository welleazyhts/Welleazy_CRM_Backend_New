from django.db import transaction
from .models import ClientCustomer, ClientCustomerAddress, ClientCustomerDependent
from apps.master_management.models import MasterProductSubCategory

class ClientCustomerService:
    @staticmethod
    @transaction.atomic
    def upsert_customer(user, data, instance=None):
        """
        Creates or updates a ClientCustomer along with nested addresses and dependents.
        """
        addresses_data = data.pop('addresses', [])
        dependents_data = data.pop('dependents', [])
        services_data = data.pop('services', [])

        fk_fields = ['client', 'branch', 'product', 'gender', 'state', 'city']
        processed_data = {}
        for k, v in data.items():
            if k in fk_fields and isinstance(v, int):
                processed_data[f"{k}_id"] = v
            else:
                processed_data[k] = v

        if instance:
            # Update existing instance
            for attr, value in processed_data.items():
                setattr(instance, attr, value)
            instance.updated_by = user
            instance.save()
        else:
            # Create new instance
            instance = ClientCustomer.objects.create(created_by=user, updated_by=user, **processed_data)

        # Handle Many-to-Many services
        if services_data:
            instance.services.set(services_data)

        # Handle nested Addresses
        ClientCustomerService._sync_addresses(instance, addresses_data)

        # Handle nested Dependents
        ClientCustomerService._sync_dependents(instance, dependents_data)

        return instance

    @staticmethod
    def _sync_addresses(customer, addresses_data):
        existing_ids = []
        for addr_data in addresses_data:
            addr_id = addr_data.get('id')
            if addr_id:
                # Update existing address
                addr_instance = ClientCustomerAddress.objects.get(id=addr_id, customer=customer)
                for attr, value in addr_data.items():
                    if attr == 'id': continue
                    if attr in ['state', 'city'] and isinstance(value, int):
                        setattr(addr_instance, f"{attr}_id", value)
                    else:
                        setattr(addr_instance, attr, value)
                addr_instance.save()
                existing_ids.append(addr_id)
            else:
                # Create new address
                # Handle FK IDs
                processed_data = {}
                for k, v in addr_data.items():
                    if k in ['state', 'city'] and isinstance(v, int):
                        processed_data[f"{k}_id"] = v
                    else:
                        processed_data[k] = v
                addr_instance = ClientCustomerAddress.objects.create(customer=customer, **processed_data)
                existing_ids.append(addr_instance.id)
        
        # Delete addresses not in the provided data
        customer.addresses.exclude(id__in=existing_ids).delete()

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
