from rest_framework import serializers
from .models import PersonInfo,Vocation
'''
该文件用于定义Django Rest Framework的序列化类,将使用DRF快速开发API
1.序列化类Serializer定义的字段必须与模型字段相互契合
2.模型序列化类ModelSerializer与模型完美结合，无须开发者定义序列化字段
'''
# 自定义序列化类Serializer
# values方法，数据以列表返回，列表元素以字典表示
nameList = PersonInfo.objects.values('name').all()
NAME_CHOICES = [item['name'] for item in nameList]
# 设置模型Vocation的字段name的下拉内容
class MySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    job = serializers.CharField(max_length=100)
    title = serializers.CharField(max_length=100)
    payment = serializers.CharField(max_length=100)
    # 模型Vocation的字段name是外键字段，它指向模型PersonInfo,因此可用PrimaryKeyRelatedField
    name = serializers.PrimaryKeyRelatedField(queryset=nameList)

    # 重写cerate函数，将API数据保存到数据表temp_app_vocation
    def create(self,validated_data):
        return Vocation.objects.create(**validated_data)
    # 重写update函数，将API数据更新到数据表temp_app_vocation
    def update(self,instance,validated_data):
        return instance.update(**validated_data)

# 模型序列化类ModelSerializer
class VocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vocation
        fields = '__all__'
        # fields=('id','job','title','payment','name')