"""
Serializer for recipe API.
"""
from rest_framework import serializers

from core.models import (
    Recipe,
    Tag,
    Ingredient,
)


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_filelds = ['id']
        
        
class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredient."""
    class Meta:
        model = Ingredient
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""
    tags = TagSerializer(many=True, required=False)
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'time_minutes', 'price', 'tags', 'ingredients'
            ]
        read_only_fields = ['id']

    def _get_or_create_tag(self, recipe, tags):
        """Handling getting or creating tag as needed."""
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                name=tag['name']
            )
            recipe.tags.add(tag_obj)

    def _get_or_create_ingredient(self, recipe, ingredients):
        """Handling getting or creatinh ingredient as needed."""
        auth_user = self.context['request'].user
        for ingredient in ingredients:
            ing_obj, created = Ingredient.objects.get_or_create(
                user=auth_user,
                name=ingredient['name']
            )
            recipe.ingredients.add(ing_obj)

    def create(self, validated_data):
        """Create and return recipe with tags."""
        tags = validated_data.pop('tags', [])
        ingredients = validated_data.pop('ingredients', [])
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tag(recipe, tags)
        self._get_or_create_ingredient(recipe, ingredients)

        return recipe

    def update(self, instance, validated_data):
        """Update recipe."""
        tags = validated_data.pop('tags', None)
        ingredients = validated_data.pop('ingredients', None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tag(instance, tags)
        if ingredients is not None:
            instance.ingredients.clear()
            self._get_or_create_ingredient(instance, ingredients)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view."""
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']


class ImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading image to the recipe."""
    class Meta:
        model = Recipe
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': True}}
