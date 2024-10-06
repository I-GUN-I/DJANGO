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

    def clean(self):
        cleaned_data = super().clean()
        cat_name = cleaned_data['name']

        if self.instance.name != cat_name:
            if Category.objects.filter(name=cat_name).exists():
                raise ValidationError("This Category already exists.")

        return cleaned_data
