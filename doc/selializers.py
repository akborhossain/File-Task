from rest_framework import serializers
import requests
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields='__all__'


class DocFileSerializer(serializers.ModelSerializer):
    class Meta:
        model= DocFile
        fields= '__all__'

class DocFileDetailsSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()
    class Meta:
        model= DocFile
        fields= '__all__'

    def to_representation(self, instance):
        try:
            created_by = User.objects.filter(username=instance.created_by).last()
            created_by={'id': created_by.id, 'username': created_by.username}

        except:
            created_by={}
        try:
            updated_by=User.objects.filter(username=instance.updated_by).last()
            updated_by={'id': updated_by.id, 'username': updated_by.username}

        except:
            updated_by={}
        file_info={
            "id":instance.id,
            "title":instance.title,
            "description":instance.description,
            "created_by":created_by,
            "created_at":instance.created_at,
            "updated_by":updated_by,
            "updated_at":instance.updated_at
        }
        if instance.uploaded_files:
            file_info["uploaded_files"] = instance.uploaded_files.url
        else:
            file_info["uploaded_files"] = None
        return file_info
