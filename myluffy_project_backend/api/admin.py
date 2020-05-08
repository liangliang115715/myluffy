from django.contrib import admin
from api.models import *
# Register your models here.

admin.site.register(UserInfo)
admin.site.register(Course)
admin.site.register(CourseDetail)
admin.site.register(Teacher)
admin.site.register(PricePolicy)
admin.site.register(Coupon)
admin.site.register(CouponRecord)
admin.site.register(CourseCategory)