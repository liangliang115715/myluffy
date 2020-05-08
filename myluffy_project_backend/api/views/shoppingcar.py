from rest_framework.views import APIView
from rest_framework.response import Response
from api.utils.auth import ExpiringTokenAuthentication
from api.utils.response import BaseResponse
from api.utils.exceptions import CommonException
from api.models import *
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
import redis, json

cache = redis.Redis(decode_responses=True)


class ShoppingCarView(APIView):
    authentication_classes = [ExpiringTokenAuthentication, ]
    def get(self, request):
        '''
        :param request:
        :return: ret_dict==.> ret_dict['data']为购物车列表信息
        '''
        res = BaseResponse()
        try:
            added_goods_list = []
            shopping_car_list = []
            user_id = request.user.id
            shoppingcar_key_pattern = settings.SHOPPINGCAR_REDIS_KEY %(user_id,'*')
            shoppingcar_key_list = cache.keys(shoppingcar_key_pattern)

            for shoppingcar_key in shoppingcar_key_list:
                goods_obj_info = json.loads(cache.get(shoppingcar_key))
                added_goods_list.append(goods_obj_info)
                '''
                    # 转换格式  将缓存中的数据格式转换成目标格式然后添加到shopping_car_list中
                    # shopping_car_item_dict = {}
                    # shopping_car_item_dict['id'] = shoppingcar_key
                    # shopping_car_item_dict['default_price_period'] = goods_obj_info['choosen_price_policy_id']
                    # shopping_car_item_dict['relate_price_policy'] = goods_obj_info['relate_price_policy']
                    # shopping_car_item_dict['name'] = goods_obj_info['title']
                    # shopping_car_item_dict['course_img'] = goods_obj_info['img']
                    # shopping_car_item_dict['default_price'] = goods_obj_info['choosen_price']
               
                '''
                shopping_car_list.append(goods_obj_info)
            # 存入data
            res.data={"shopping_car_list": shopping_car_list, "total": len(shopping_car_list)}
        except Exception as e:
            res.code = 1033
            res.msg = '获取购物车数据失败'
        return Response(res.dict)


    def post(self, request):

        res = BaseResponse()
        # 1.取值
        course_id = request.data.get('courseId')
        price_policy_id = request.data.get('validPeriodId')

        user_id = request.user.pk

        # 2.校验数据
        try:
            course_obj = Course.objects.get(pk=course_id)
            relate_price_police = course_obj.price_policy.all()
            if price_policy_id not in [obj.pk for obj in relate_price_police]:
                raise CommonException(1002, '价格策略非法')
            # 3.存到缓存
            # 3.1 构建redis的键
            shoppingcar_key = settings.SHOPPINGCAR_REDIS_KEY % (user_id, course_id)
            # 3.2 构建redis的值-shoppingcar_val
            relate_price_policy_dict = {}
            for price_policy in relate_price_police:
                relate_price_policy_dict[price_policy.pk] = {
                    'pk': price_policy.pk,
                    'valid_period': price_policy.valid_period,
                    'valid_period_text': price_policy.get_valid_period_display(),
                    'price': price_policy.price,
                    'default': False,
                }
            relate_price_policy_dict[price_policy_id]['default'] = True
            shoppingcar_val = {
                'id':course_obj.id,
                'title': course_obj.name,
                'img': course_obj.course_img,
                'relate_price_policy': relate_price_policy_dict,
                'choosen_price_policy_id': price_policy_id,
                'choosen_price': relate_price_policy_dict[price_policy_id]['price'],
                'choosen_valid_period': relate_price_policy_dict[price_policy_id]['valid_period'],
                'choosen_valid_period_text': relate_price_policy_dict[price_policy_id]['valid_period_text'],
            }
            cache.set(shoppingcar_key, json.dumps(shoppingcar_val))
            res.data = '加入购物车成功'
        except ObjectDoesNotExist as e:
            res.code = 1001
            res.msg = '提交异常，课程对象不存在！'
        except CommonException as e:
            res.code = e.code
            res.msg = e.msg
        return Response(res.dict)
    def put(self, request):
        res = BaseResponse()
        try:
            # 1 获取前端传过来的course_id 以及price_policy_id
            course_id = request.data.get("course_id", "")
            price_policy_id = request.data.get("price_policy_id", "")
            user_id = request.user.id
            # 2 校验数据的合法性
            # 2.1 校验course_id是否合法
            shopping_car_key = settings.SHOPPINGCAR_REDIS_KEY % (user_id, course_id)
            if not cache.exists(shopping_car_key):
                res.code = 1035
                res.error = "课程不存在"
                return Response(res.dict)
            # 2.2 判断价格策略是否合法
            course_info = cache.hgetall(shopping_car_key)
            price_policy_dict = json.loads(course_info["price_policy_dict"])
            if str(price_policy_id) not in price_policy_dict:
                res.code = 1036
                res.error = "所选的价格策略不存在"
                return Response(res.dict)
            # 3 修改redis中的default_policy_id
            course_info["default_policy_id"] = price_policy_id
            # 4 修改信息后写入redis
            cache.hmset(shopping_car_key, course_info)
            res.data = "更新成功"
        except Exception as e:
            res.code = 1034
            res.error = "更新价格策略失败"
        return Response(res.dict)

    def delete(self, request):
        res = BaseResponse()
        try:
            # 获取前端传过来的course_id
            course_id = request.data.get("course_id", "")
            user_id = request.user.id
            # 判断课程id是否合法
            shopping_car_key = settings.SHOPPINGCAR_REDIS_KEY % (user_id, course_id)
            if not cache.exists(shopping_car_key):
                res.code = 1039
                res.error = "删除的课程不存在"
                return Response(res.dict)
            # 删除redis中的数据
            cache.delete(shopping_car_key)
            res.data = "删除成功"
        except Exception as e:
            res.code = 1037
            res.error = "删除失败"
        return Response(res.dict)