import json
from django.db import transaction
from rest_framework.exceptions import ValidationError


class DocumentService:
    @staticmethod
    def get_nested_data(data, key):

        if not isinstance(data, dict):
            return None

        val = data.get(key)
        if val is not None:
            if isinstance(val, list):
                return val
            if isinstance(val, dict):
                return [val]
            if isinstance(val, str):
                try:
                    parsed = json.loads(val)
                    if isinstance(parsed, list):
                        return parsed
                    if isinstance(parsed, dict):
                        return [parsed]
                except (ValueError, TypeError):
                    pass

        json_data_str = data.get('data')
        if json_data_str and isinstance(json_data_str, str):
            try:
                parsed = json.loads(json_data_str)
                if key in parsed:
                    nested = parsed.get(key)
                    if isinstance(nested, list):
                        return nested
                    if isinstance(nested, dict):
                        return [nested]
            except (ValueError, TypeError, AttributeError):
                pass

        return None

    @staticmethod
    @transaction.atomic
    def sync_documents(parent_instance, files, documents_json=None,
                      model=None, parent_field=None, file_field='file',
                      name_field=None, user=None, include_keys=None):

        if not parent_instance:
            raise ValidationError("parent_instance is required")

        if not model or not parent_field:
            raise ValidationError("model and parent_field are required")

        keep_ids = []

        if documents_json is not None:
            for doc in documents_json:
                doc_id = doc.get("id")
                if doc_id:
                    try:
                        keep_ids.append(int(doc_id))
                    except (ValueError, TypeError):
                        keep_ids.append(doc_id)
        else:
            keep_ids = list(
                model.objects.filter(
                    **{parent_field: parent_instance}
                ).values_list("id", flat=True)
            )

        created_docs = []

        for key in files:
            if include_keys and key not in include_keys:
                continue
            for uploaded_file in files.getlist(key):

                if not uploaded_file or uploaded_file.size == 0:
                    raise ValidationError("Uploaded file is empty")

                doc_kwargs = {
                    parent_field: parent_instance,
                    file_field: uploaded_file,
                }

                if name_field:
                    doc_kwargs[name_field] = uploaded_file.name

                if user:
                    doc_kwargs["created_by"] = user
                    doc_kwargs["updated_by"] = user

                doc = model(**doc_kwargs)
                doc.save()
                created_docs.append(doc)

        keep_ids.extend([doc.id for doc in created_docs])

        if documents_json is not None:
            model.objects.filter(
                **{parent_field: parent_instance}
            ).exclude(id__in=keep_ids).delete()

        return keep_ids

        return keep_ids
