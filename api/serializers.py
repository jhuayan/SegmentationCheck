from managerawdata.models import OPage
from rest_framework import serializers
from catalogue.models import Tripitaka, Volume
from segmentation.models import Page,Character

class OPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OPage
        fields = ('id', 'description', 'tripitaka','volume', 'page_no','page_type','height', 'width',
            'image','status')

class VolumeSerializer(serializers.ModelSerializer):
    o_pages = serializers.SerializerMethodField(read_only=True)
    bars_count = serializers.CharField(read_only=True, source="tripitaka.bars_count")
    o_pages_count = serializers.IntegerField(source='get_o_pages_count')

    def get_o_pages(self, volume):
        qs = OPage.objects.filter(status=0, volume=volume).order_by('-id')[:10]
        serializer = OPageSerializer(instance=qs, many=True, read_only=True)
        return serializer.data

    class Meta:
        model = Volume
        fields = ('id', 'number','start_page','end_page', 'o_pages', 'bars_count', 'o_pages_count')
        read_only_fields = ('o_pages_count')

class TripitakaSerializer(serializers.ModelSerializer):
    volumes = VolumeSerializer(many=True, read_only=True)
    class Meta:
        model = Tripitaka
        fields = ('id', 'name','code', 'volumes_count', 'bars_count', 'volumes')

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('id', 'text', 'is_correct','image','width','height','image_url')


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ('id','page', 'char','image', 'is_correct','image_url')

