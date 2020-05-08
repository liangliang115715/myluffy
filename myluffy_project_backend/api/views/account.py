from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from api.utils.exceptions import CommonException
from api.utils.response import BaseResponse
from api.utils.auth import ExpiringTokenAuthentication
from api.models import *
import redis, json, datetime

cache = redis.Redis(decode_responses=True)


class AccountView(APIView):
    authentication_classes = [ExpiringTokenAuthentication, ]

    def get_coupon_list(self, request, course_id=None):
        now = datetime.datetime.now()
        content_type_obj = ContentType.objects.get(app_label='api', model='course')
        # 过滤出当前用户的都带当前课程的有效期内的未使用的优惠券
        coupon_record_list = CouponRecord.objects.filter(
            account=request.user.id,
            # content_type__pk=content_obj.id,
            # object_id=content_obj.id,
            coupon__content_type_id=content_type_obj.id,
            coupon__object_id=course_id,
            status=0,
            coupon__valid_begin_date__lte=now,
            coupon__valid_end_date__gte=now,
        )
        coupon_list = []
        for coupon_record in coupon_record_list:
            coupon_list.append({

                "pk": coupon_record.pk,
                "name": coupon_record.coupon.name,
                "coupon_type": coupon_record.coupon.get_coupon_type_display(),
                "money_equivalent_value": coupon_record.coupon.money_equivalent_value,
                "off_percent": coupon_record.coupon.off_percent,
                "minimum_consume": coupon_record.coupon.minimum_consume,
            })
        return coupon_list

    def cal_coupon_price(self, price, coupon_info):

        print("coupon_info", coupon_info)
        coupon_type = coupon_info["coupon_type"]
        money_equivalent_value = coupon_info.get("money_equivalent_value")
        off_percent = coupon_info.get("off_percent")
        minimum_consume = coupon_info.get("minimum_consume")
        rebate_price = 0
        if coupon_type == "立减券":  # 立减券
            rebate_price = price - money_equivalent_value
            if rebate_price <= 0:
                rebate_price = 0
        elif coupon_type == "满减券":  # 满减券
            if minimum_consume > price:
                raise CommonException(3000, "优惠券未达到最低消费")
            else:
                rebate_price = price - money_equivalent_value
        elif coupon_type == "折扣券":
            rebate_price = price * off_percent / 100

        return rebate_price

    def get(self, request):
        res = BaseResponse()
        try:
            # 1 取到user_id
            user_id = request.user.id
            # 2 拼接购物车的key
            account_key = settings.ACCOUNT_REDIS_KEY % (user_id, "*")
            # shopping_car_1_*
            # shopping_car_1_asdgnlaksdj
            # 3 去redis读取该用户的所有加入购物车的课程
            # 3.1 先去模糊匹配出所有符合要求的key
            all_keys = cache.scan_iter(account_key)

            # 3.2 循环所有的keys 得到每个可以
            account_course_list = []
            for key in all_keys:
                account_course = json.loads(cache.get(key))
                account_course_list.append(account_course)

            global_coupons = cache.get("global_coupon_%s" % request.user.pk)
            global_coupons = json.loads(global_coupons) if global_coupons else ''

            total_price = cache.get("total_price")

            res.data = {
                "account_course_list": account_course_list,
                "total": len(account_course_list),
                "global_coupons": global_coupons,
                "total_price": total_price
            }

        except Exception as e:
            res.code = 1033
            res.error = "获取购物车失败"

        return Response(res.dict)

    def post(self, request):
        '''
           request.data=>course_list=[{
                             "course_id":1,
                             "price_policy_id":2
                           },
        '''
        # self.dispatch()
        res = BaseResponse()
        # 1.取值
        course_list = request.data
        user_id = request.user.id
        # 2.校验数据
        try:
            del_list = cache.keys(settings.ACCOUNT_REDIS_KEY % (user_id, "*"))
            if del_list:
                cache.delete(*del_list)
            price_list = []
            for course_dict in course_list:

                course_id = course_dict.get("course_id")
                price_policy_id = course_dict.get("price_policy_id")
                # 校验课程是否存在
                course_obj = Course.objects.get(pk=course_id)
                # 查找课程关联的价格策略
                price_policy_list = course_obj.price_policy.all()
                price_policy_dict = {}
                for price_policy in price_policy_list:
                    price_policy_dict[price_policy.pk] = {
                        "prcie": price_policy.price,
                        "valid_period": price_policy.valid_period,
                        "valid_period_text": price_policy.get_valid_period_display(),
                        "default": price_policy.pk == price_policy_id
                    }

                if price_policy_id not in price_policy_dict:
                    raise CommonException(1001, "价格策略异常!")
                pp = PricePolicy.objects.get(pk=price_policy_id)
                # 将课程信息加入到每一个课程结算字典中
                account_dict = {
                    "id": course_id,
                    "name": course_obj.name,
                    "course_img": course_obj.course_img,
                    "relate_price_policy": price_policy_dict,
                    "default_price": pp.price,
                    "rebate_price": pp.price,
                    "default_price_period": pp.valid_period,
                    "default_price_policy_id": pp.pk
                }
                # 课程价格加入到价格列表
                price_list.append(float(pp.price))

                # 查询当前用户拥有未使用的，在有效期的且与当前课程相关的优惠券
                account_dict["coupon_list"] = self.get_coupon_list(request, course_id)

                # 存储结算信息
                account_key = settings.ACCOUNT_REDIS_KEY % (user_id, course_id)
                cache.set(account_key, json.dumps(account_dict))

            # 获取通用优惠券,加入redis中
            cache.set("global_coupon_%s" % user_id, json.dumps(self.get_coupon_list(request)))
            cache.set("total_price", sum(price_list))
        except ObjectDoesNotExist as e:
            res.code = 1001
            res.msg = '提交异常，课程对象不存在！'
        except CommonException as e:
            res.code = e.code
            res.msg = e.msg
        except Exception as e:
            print(e)
        return Response(res.dict)

    def put(self, request, *args, **kwargs):
        '''
        choose_coupons:
            {
            choose_coupons={"1":2,"2":3,"global_coupon_id":5}
            is_beli:true
            }
        '''
        res = BaseResponse()
        # try:

        # 1 获取数据
        choose_coupons = request.data.get("choose_coupons")
        is_beli = request.data.get("is_beli")
        user_pk = request.user.pk

        # 2 获取结算课程列表
        cal_price = {}
        data = self.get(request).data.get("data")
        account_course_list = data.get("account_course_list")

        account_courses_info = {}
        for account_course in account_course_list:
            temp = {
                "coupon": {},
                "default_price": account_course["default_price"]
            }
            account_courses_info[account_course["id"]] = temp

            for item in account_course["coupon_list"]:
                # print("choose_coupons", choose_coupons)  # {'4': 4}
                # print(str(account_course["id"]))
                coupon_id = choose_coupons.get(str(account_course["id"]))
                if coupon_id == item["pk"]:
                    temp["coupon"] = item
        print("account_course_info", account_courses_info)
        price_list = []
        for key, val in account_courses_info.items():
            if not val.get("coupon"):
                price_list.append(val["default_price"])
                cal_price[key] = val["default_price"]
            else:
                coupon_info = val.get("coupon")
                default_price = val["default_price"]
                rebate_price = self.cal_coupon_price(default_price, coupon_info)
                price_list.append(rebate_price)
                cal_price[key] = rebate_price

        print("课程优惠券后价格列表price_list", price_list)
        total_price = sum(price_list)
        # 3 计算通用优惠券的价格
        global_coupon_id = choose_coupons.get("global_coupon_id")
        if global_coupon_id:

            global_coupons = data.get("global_coupons")
            print("global_coupons", global_coupons)
            global_coupon_dict = {}
            for item in global_coupons:
                global_coupon_dict[item["pk"]] = item
            total_price = self.cal_coupon_price(total_price, global_coupon_dict[global_coupon_id])
            print("通用优惠券", global_coupon_dict[global_coupon_id]["coupon_type"])
            print("计算后total_price=", total_price)

        # 计算贝里
        if json.loads(is_beli):
            print("request.user.beli", request.user.beli)
            total_price = total_price - request.user.beli / 10
            if total_price < 0:
                total_price = 0
            print("贝里数计算后", total_price)

        cal_price["total_price"] = total_price
        res.data = cal_price

        # except Exception as e:
        #     res.code=500
        #     res.msg="结算错误!"+str(e)

        return Response(res.dict)
