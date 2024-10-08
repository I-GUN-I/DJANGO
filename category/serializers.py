from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class CategoryPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'description']

    def validate(self, data):
        cat_name = data['name']
        if self.instance.name != cat_name:
            if Category.objects.filter(name=cat_name).exists():
                raise serializers.ValidationError("This category already exists.")
        return data
