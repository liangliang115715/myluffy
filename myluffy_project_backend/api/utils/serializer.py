from rest_framework import serializers
from api.models import *
class CourseSerializers(serializers.ModelSerializer):
    level = serializers.CharField(source="get_level_display")
    coursedetail_id = serializers.CharField(source="coursedetail.pk")
    class Meta:
        model = Course
        fields = '__all__'

    def to_representation(self, instance):

        data = super(CourseSerializers, self).to_representation(instance)
        # 购买人数
        # data["people_buy"] = instance.order_details.all().count()
        # 价格套餐列表
        price_policies = instance.price_policy.all().order_by("price").only("price")

        price = getattr(price_policies.first(), "price", 0)

        if price_policies and price == 0:
            is_free = True
            price = "免费"
            origin_price = "原价￥{}".format(price_policies.last().price)
        else:
            is_free = False
            price = "￥{}".format(price)
            origin_price = None

        # 是否免费
        data["is_free"] = is_free
        # 展示价格
        data["price"] = price
        # 原价
        data["origin_price"] = origin_price

        return data

class CourseDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = CourseDetail
        fields = '__all__'
    name=serializers.CharField(source="course.name")
    prices = serializers.SerializerMethodField()
    brief = serializers.CharField(source='course.brief')
    study_all_time = serializers.StringRelatedField(source='hours')
    level = serializers.CharField(source='course.get_level_display')
    teachers = serializers.SerializerMethodField()
    is_online = serializers.CharField(source="course.get_status_display")
    recommend_coursesinfo = serializers.SerializerMethodField()
    course_img = serializers.CharField(source='course.course_img')
    def get_prices(self,instance):

        return [{"price":obj.price,
                 # "valid_period":obj.valid_period,
                 "id":obj.id,
                 "valid_period":obj.valid_period,
                 "valid_period_text":obj.get_valid_period_display()
                 } for obj in instance.course.price_policy.all()
                ]

    def get_teachers(self, instance):
        return [{"name": obj.name,
                 "image": obj.image} for obj in instance.teachers.all()]

    def get_recommend_coursesinfo(self, instance):
        return [{"name": obj.name,
                 "pk": obj.pk} for obj in instance.recommend_courses.all()]

class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id","name",)

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserInfo
        fields="__all__"