
from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from api.utils.auth import ExpiringTokenAuthentication
from api.utils.response import BaseResponse
from api.utils.exceptions import CommonException
from api.utils.ali.api import ali_api
from api.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import datetime,random,redis
cache = redis.Redis(decode_responses=True)
class PaymentView(APIView):
    authentication_classes = [ExpiringTokenAuthentication,]

    def get_pay_url(self, request, order_number, final_price):
        # 4 调用支付宝支付接口(二维码页面)

        if request.META["HTTP_USER_AGENT"]:


            pay_api = ali_api.pay.pc

        elif request == "APP":
            pay_api = ali_api.pay.app

        else:
            pay_api = ali_api.pay.wap

        pay_url = pay_api.direct(
            subject="我的路飞学城",  # 商品简单描述
            out_trade_no=order_number,  # 商户订单号
            total_amount=final_price,  # 交易金额(单位: 元 保留俩位小数)
        )

        return pay_url


    def get_order_num(self):
        now=datetime.datetime.now()
        orderType="1"
        dateStr4yyyyMMddHHmmss="{0}{1}{2}".format(now.year,now.month,now.day)
        rand=str(random.randint(1000,9999))

        s=orderType+dateStr4yyyyMMddHHmmss+rand

        return s


    def cal_coupon_price(self, price, coupon_record_obj):
        coupon_type = coupon_record_obj.coupon.coupon_type
        money_equivalent_value = coupon_record_obj.coupon.money_equivalent_value
        off_percent = coupon_record_obj.coupon.off_percent
        minimum_consume = coupon_record_obj.coupon.minimum_consume
        rebate_price = 0
        if coupon_type == 0:  # 立减券
            rebate_price = price - money_equivalent_value
            if rebate_price <= 0:
                rebate_price = 0
        elif coupon_type == 1:  # 满减券
            if minimum_consume > price:
                raise CommonException(1007, "优惠券未达到最低消费")
            else:
                rebate_price = price - money_equivalent_value
        elif coupon_type == 2:
            rebate_price = price * off_percent / 100

        return rebate_price

    def post(self,request):
    # 1.获取数据
        is_beli = request.data.get('is_beli')
        course_list =request.data.get('course_list')
        global_coupon_id = request.data.get('global_coupon_id')
        pay_money = request.data.get('pay_money')
        user_id = request.user.pk
        # 2.校验
        res = BaseResponse()
        price_list = []
        try:
            now = datetime.datetime.now()
            # 2.1 每个课程
            for course_dict in course_list:
                course_id = course_dict.get("course_id")
                default_price_policy_id = course_dict.get('default_price_policy_id')
                # coupon_record_id = course_dict.get('coupon_record_id','')
                course_obj = Course.objects.get(pk=course_id)

                if default_price_policy_id not in [ obj.pk for obj in course_obj.price_policy.all()]:
                    raise CommonException(1002,'价格策略不存在')
                content_obj = ContentType.objects.get(
                    app_label='api',
                    model='course',
                )

                price_policy_obj = PricePolicy.objects.get(pk=course_dict.get("default_price_policy_id"))
                course_dict["original_price"] = price_policy_obj.price
                course_dict["valid_period_display"] = price_policy_obj.get_valid_period_display()
                course_dict["valid_period"] = price_policy_obj.valid_period
                coupon_record_id = course_dict.get("coupon_record_id")
                # 检验课程优惠券，并计算出折后的总价格（不带通用优惠券和贝利）
                if not coupon_record_id:
                    price_list.append(price_policy_obj.price)
                else:
                    coupon_record_list = CouponRecord.objects.filter(
                        account = request.user,
                        coupon__content_type=content_obj,
                        coupon__object_id=course_id,
                        status=0,
                        coupon__valid_begin_date__lte=now,
                        coupon__valid_end_date__gte=now,
                    )
                    if coupon_record_id and coupon_record_id not in [obj.pk for obj in coupon_record_list]:
                        raise CommonException("课程优惠券异常！", 1006)
                    coupon_record_obj = CouponRecord.objects.get(pk=coupon_record_id)
                    rebate_money = self.cal_coupon_price(price_policy_obj.price,coupon_record_obj)
                    price_list.append(rebate_money)
            # 2.2 通用优惠券
            global_coupon_record_list = CouponRecord.objects.filter(account=request.user,
                                                                    status=0,
                                                                    coupon__valid_begin_date__lt=now,
                                                                    coupon__valid_end_date__gt=now,
                                                                    coupon__content_type_id=14,
                                                                    coupon__object_id=None
                                                                    )
            if not global_coupon_record_list:global_coupon_record_list = []
            if global_coupon_id and global_coupon_id not in [obj.pk for obj in global_coupon_record_list]:
                raise CommonException("通用优惠券异常", 1006)
            if global_coupon_id:
                global_coupon_record_obj = CouponRecord.objects.get(pk=global_coupon_id)
                final_price = self.cal_coupon_price(sum(price_list), global_coupon_record_obj)
            else:final_price=sum(price_list)
            # 2.3 贝利
            cost_beli_num = 0
            if is_beli:
                final_price = final_price - request.user.beli / 10
                cost_beli_num = request.user.beli
                if final_price < 0:
                    final_price = 0
                    cost_beli_num = final_price * 10
            if final_price != float(pay_money):
                raise CommonException(1008, "支付总价格异常！")

            # 生成订单
            order_number = self.get_order_num()
            order_obj = Order.objects.create(
                payment_type=1,
                order_number=order_number,
                account=request.user,
                status=1,
                order_type=1,
                actual_amount=pay_money,
            )

            for course_item in course_list:
                OrderDetail.objects.create(
                    order=order_obj,
                    content_type_id=14,
                    object_id=course_item.get("course_id"),
                    original_price=course_item.get("original_price"),
                    price=course_item.get("rebate_price") or course_item.get("original_price"),
                    valid_period=course_item.get("valid_period"),
                    valid_period_display=course_item.get("valid_period_display"),
                )

            request.user.beli = request.user.beli - cost_beli_num
            request.user.save()

            cache.set(order_number + "|" + str(cost_beli_num), "", 20)
            account_key = settings.ACCOUNT_REDIS_KEY % (user_id, "*")

            cache.delete(*cache.keys(account_key))
            res.data = self.get_pay_url(request, order_number, final_price)

        except ObjectDoesNotExist as e:
            res.code = 1001
            res.msg = '课程不存在！'
        except CommonException as e :
            res.code = e.code
            res.msg = e.msg
        return Response(res.dict)
        # 3.生成订单
        # 4.返回阿里支付页面



def get_pay_url(request):
    print('--->',request.GET.get("order_number"))
    pay_url = ali_api.pay.pc.direct(
        subject="python全栈课程",  # 商品简单描述
        out_trade_no=request.GET.get("order_number"),  # 商户订单号
        total_amount=request.GET.get("final_price"),  # 交易金额(单位: 元 保留俩位小数)
    )

    return JsonResponse({"pay_url":pay_url})


