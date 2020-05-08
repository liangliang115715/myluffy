<template>
  <div class="wrap">
    <div class="web-course-banner">
      <div class="container">
        <div class="title">
          <a :href="video_brief_link"><img src="../../../static/images/play.png" height="67" width="67" alt=""></a>
          <h1 class="course-title">{{ course_name }}</h1>
        </div>
        <span class="course-text">{{ course_brief }}</span>
        <div class="course-list">
          <ul>
            <li class="detail-item">
              难度：{{level}}
            </li>
            <li class="sep"></li>
            <li class=detail-item>时长：{{ hours }}</li>
            <li class="sep"></li>
            <li class=detail-item>学习人数：632人</li>
            <li class="sep"></li>
            <li class=detail-item>评分 10.0</li>
          </ul>
        </div>
      </div>
    </div>
    <div class="course-review">
      <ul class="review-head-wrap">
        <li class="head-item">课程概述</li>
        <li class="head-item">课程章节</li>
        <li class="head-item">用户评价(10)</li>
        <li class="head-item">常见问题</li>

      </ul>
    </div>
    <!-- 课程详情 -->
    <div class="course-detail">
      <div class="container">
        <div class="course-detail-text">
          <h3>课程概述</h3>
          <p>
            Django是Python语言中最流行、最强大的WEB框架，可快速构建稳定强大的WEB项目，大大提高开发效率，很多知名项目都是基于Django开发，如Disqus、Pinterest、Instagram、Bitbucket等，
            Django官方Slogan是The framework for perfectionist with deadline!
            一个为完美主义者且又开发工期很紧的人设计的框架，事实确实如此，Django自身集成了丰富的WEB开发通用组件，如用户认证、分页、中间件、缓存、session等，可以避免浪费大量时间重复造轮子。人生苦短，join
            the course now and start to build your first web program based on Django.
          </p>
        </div>
        <div class="course-img">
          <img :src="course_img" alt="">
        </div>
      </div>
    </div>
    <div class="course-price">
      <div class="container">
        <span>可以根据不同的学习情况购买不一样的学习套餐哦！</span>
        <ul class="course-price-item">
          <li @click='priceHandler(index)' :class='{active:index == currentIndex}' v-for='(price,index) in prices'
              :key='price.id'>
            <p class="price" :class='{active:index === currentIndex}'>¥{{ price.price }}</p>
            <p class="time" :class='{active:index === currentIndex}'>有效期{{price.valid_period_text}}</p>
          </li>

        </ul>
        <div class="course-action">
          <button class="left" @click="directBuy">购买</button>
          <button class="right" @click='addShopCart'>加入购物车</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
  export default {

    name: 'CourseDetail',
    data() {
      return {
        prices: [], //价格套餐
        currentIndex: null,
        level: '',
        hours: '',
        video_brief_link: '',
        course_img: '',
        course_name: '',
        course_brief: '',
        course_id:null,
      }
    },
    methods: {
      addShopCart() {
        //1.如果用户没有选中价格套餐，提示用户 “您没有选择要加入的套餐哦”
        //2.如果用户选中套餐，点击购物车按钮，（判断当前用户有登录  vue-cookie）
        // 2.1 如果用户未登录（未产生token）
        //编程式导航 跳转登录页面

        if (this.currentIndex != null) {
          //用户选中套餐
          //判断登录状态
          if (localStorage.getItem('token')) {
            //已登录
            let params = {
              courseId: this.$route.params.courseId,
              validPeriodId: this.prices[this.currentIndex].id,
            };
            this.$http.add_shop_car(params)
              .then(res => {
                  if (res.code === 1000) {
                    this.$message('购物车添加成功')
                  }
                  else {
                    this.$message(res.msg)
                  }
                }
              )
              .catch(err => {
                console.log(err)
              })


          } else {
            //未登录，跳转登陆界面
            this.$router.push({
              name: 'Login',

            })


          }


        } else {
          //用户未选中套餐
          this.$message({
            message: '您没有选择要加入的套餐哦',
            type: 'warning',
            duration: 1000
          });
        }


      },
      //价格套餐点击事件
      priceHandler(index) {

        if (this.currentIndex === index) {
          //又点了当前的套餐
          this.currentIndex = null;
        } else {
          this.currentIndex = index;
        }

      },
      //获取课程详情  包含 价格套餐
      getCourseDetail() {
        let course_id = this.$route.params.courseId;
        this.$http.courseDetail(course_id)
          .then(res => {
            this.course_id=res.id;
            this.prices = res.prices;
            this.hours = res.hours;
            this.level = res.level;
            this.video_brief_link = res.video_brief_link;
            this.course_img = res.course_img;
            this.course_name = res.name;
            this.course_brief = res.brief;

          })
          .catch(err => {
            console.log(err);
          })
      },
      //直接购买
      directBuy() {
        console.log('直接购买！！！');
        if (this.currentIndex != null) {
          let arr = [{
            "course_id": this.course_id,
            "price_policy_id": this.prices[this.currentIndex]["id"]
          }];
          this.$http.account(arr).then(res =>{
            this.$router.push({
              name: 'account'
            })
          }).catch(err => {
          })
        } else {
          this.$message({
            message: '请选择价格策略！',
            center: true
          });
        }
      },

    },
    created() {
      this.getCourseDetail()
    }
  };
</script>

<style lang="css" scoped>
  .wrap {
    width: 100%;
  }

  .web-course-banner {
    width: 100%;
    height: 512px;
    background: url(https://www.luffycity.com/static/img/web-banner.1402933.png) no-repeat;
    background-size: 100% 100%;
    text-align: center;
    overflow: hidden;
  }

  .container {
    width: 1200px;
    margin: 182px auto 0;
    text-align: left;
  }

  .container img {
    vertical-align: middle;
  }

  .container h1 {
    display: inline-block;
    font-size: 48px;
    color: #4a4a4a;
    letter-spacing: .37px;
    margin-left: 40px;
    font-family: PingFangSC-Light;
    font-weight: 500;
    line-height: 1.1;
    position: relative;
    top: 10px;
  }

  .course-text {
    width: 464px;
    display: inline-block;
    font-size: 22px;
    color: #4a4a4a;
    letter-spacing: .17px;
    line-height: 36px;
    margin-top: 33px;
  }

  .course-list {
    width: 100%;
  }

  .course-list ul {
    margin-top: 63px;
    display: flex;
    align-items: center;
    justify-content: flex-start;
  }

  .course-list ul li.detail-item {
    font-size: 18px;
    color: #4a4a4a;
    letter-spacing: .74px;
    height: 26px;
    padding: 0 20px;
  }

  .course-list ul li.sep {
    width: 2px;
    height: 14px;
    border-left: 1px solid #979797;
  }

  .course-review {
    width: 100%;
    height: 80px;
    background: #fafbfc;
    border-top: 1px solid #e8e8e8;
    box-shadow: 0 1px 0 0 #e8e8e8;
  }

  .review-head-wrap {
    width: 590px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
  }

  .review-head-wrap .head-item {
    height: 80px;
    line-height: 80px;
    font-size: 16px;
    color: #555;
    cursor: pointer;
  }

  .course-detail {
    width: 100%;
    padding-top: 90px;

  }

  .course-detail .container {
    width: 1200px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
  }

  .course-detail-text {
    width: 500px;
    text-align: left;

  }

  .course-detail-text h3 {
    padding: 20px 0;
  }

  .course-detail-text p {
    width: 100%;
    height: 196px;
    font-size: 14px;
    color: #4A4A4A;
    letter-spacing: 1.83px;
    line-height: 30px;
    text-align: left;
  }

  .course-price {
    width: 100%;
    background: #FAFAFA;

  }

  .course-price .container {
    width: 1200px;
    margin: 0 auto;
    text-align: center;
  }

  .course-price span {
    font-size: 12px;
    color: #9b9b9b;
    letter-spacing: 1.57px;
    display: inline-block;
    margin-top: 102px
  }

  .course-price ul {
    /*width: 800px;*/
    margin: 50px auto;

    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
  }

  .course-price ul li {
    width: 200px;
    height: 112px;
    border: 1px solid #979797;
  }

  .course-price ul li.active {
    background: #00CD23;

  }

  .course-price ul li p:first-child {
    font-size: 24px;
    letter-spacing: 1.92px;
    color: #333;
    margin-top: 17px;
  }

  .course-price ul li p:nth-child(2) {

    color: #9b9b9b;
    font-size: 20px;
    letter-spacing: 1.6px;
    margin-top: 9px;
  }

  .course-price ul li p.active {
    color: #fff;
  }

  .course-action {
    width: 1000px;
    margin: 0 auto;
    padding-bottom: 80px;
    display: flex;
    justify-content: center;
  }

  .course-action button {
    border: none;
    outline: none;
    cursor: pointer;
    display: inline-block;
    width: 181px;
    height: 51px;
    font-size: 14px;
    color: #fff;
    letter-spacing: 1.12px;
    text-align: center;
    background: #f5a623;
    border-radius: 82px;
  }

  .course-action button.left {
    background: #7ed321;
    box-shadow: 0 2px 4px 0 #e8e8e8;
    color: #fff;
    margin-right: 48px;
    padding: 0 20px;
  }

  .course-action button.right {
    background: #f5a623 url() no-repeat 125px 15px !important;
  }


</style>
