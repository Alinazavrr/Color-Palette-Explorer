from rest_framework import serializers
from .models import Color, Palette
from users.models import CustomUser

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'name', 'red', 'green', 'blue', 'hue', 'saturation', 'lightness', 'creator', 'created_at']
        read_only_fields = ['creator', 'created_at']

    def create(self, validated_data):
        return Color.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.red = validated_data.get('red', instance.red)
        instance.green = validated_data.get('green', instance.green)
        instance.blue = validated_data.get('blue', instance.blue)
        instance.hue = validated_data.get('hue', instance.hue)
        instance.saturation = validated_data.get('saturation', instance.saturation)
        instance.lightness = validated_data.get('lightness', instance.lightness)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()

class PaletteSerializer(serializers.ModelSerializer):
    colors = ColorSerializer(many=True, read_only=True)
    users_with_access = serializers.PrimaryKeyRelatedField(many=True, queryset=CustomUser.objects.all(), required=False)

    class Meta:
        model = Palette
        fields = ['id', 'name', 'colors', 'creator', 'users_with_access', 'created_at']
        read_only_fields = ['creator', 'created_at']

    def create(self, validated_data):
        colors_data = validated_data.pop('colors', [])
        palette = Palette.objects.create(**validated_data)
        for color_data in colors_data:
            Color.objects.create(palette=palette, **color_data)
        return palette

    def update(self, instance, validated_data):
        # Update the 'name' field if provided
        instance.name = validated_data.get('name', instance.name)

        # Update the 'users_with_access' field if provided
        users_with_access_data = validated_data.get('users_with_access')
        if users_with_access_data:
            instance.users_with_access.set(users_with_access_data)

        # Update the 'colors' field if provided
        colors_data = validated_data.get('colors')
        if colors_data is not None:
            # List of color IDs to keep
            color_ids_to_keep = [color_data['id'] for color_data in colors_data if 'id' in color_data]

            # Delete colors that are not in the updated list
            instance.colors.exclude(id__in=color_ids_to_keep).delete()

            # Update or create colors from the updated list
            for color_data in colors_data:
                color_id = color_data.get('id')
                if color_id:
                    # If color ID is provided, update existing color
                    color_instance = instance.colors.get(id=color_id)
                    color_serializer = ColorSerializer(color_instance, data=color_data, partial=True)
                    if color_serializer.is_valid():
                        color_serializer.save()
                else:
                    # If no color ID provided, create a new color
                    Color.objects.create(palette=instance, **color_data)

        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()