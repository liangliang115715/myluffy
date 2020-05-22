<template>
  <el-container>
    <el-header height='80px'>
      <div class="header">
        <div class="nav-left">
          <img width="70" height="70" src="http://image.biaobaiju.com/uploads/20180918/15/1537256147-APZCeYtgDH.jpg"
               alt="">
        </div>
        <div class="nav-center">
          <ul>
            <li v-for='(nav,i) in navlinks' :key="nav.id">
              <router-link :to='{name:nav.name}'>
                {{ nav.title }}
              </router-link>
              <span v-if="i === 2">New</span>

            </li>
          </ul>
        </div>

        <div class="nav-right" v-if='userInfo.token' @mouseenter='enterHandler' @mouseleave='leaveHandler'>
          <span>学习中心</span>
          <el-dropdown>
            <el-dropdown-menu></el-dropdown-menu>
              <span class="user">{{ userInfo.username }}</span>
              <img :src="userInfo.head_img" alt="">
              <ul class="my_account" v-if="isShow">
                  <li>我的账户<i>></i></li>
                  <li @click='myorder'>
                    我的订单
                    <i>></i>
                  </li>
                  <li>
                    我的优惠券
                    <i>></i>
                  </li>
                  <li>
                    我的消息
                    <span class="msg">({{ userInfo.notice_num }})</span>
                    <i>></i>
                  </li>
                  <li @click='shopCartInfo'>
                    购物车
                    <span class="count">({{ userInfo.shop_cart_num}})</span>
                    <i>></i>
                  </li>
                  <li @click="logoutHandler">
                    退出
                    <i>></i>
                  </li>

                </ul>
          </el-dropdown>
        </div>
        <div class="nav-right" v-else>

          <span @click="goLoginHandler">登录</span>
          &nbsp;| &nbsp;
          <span>注册</span>

        </div>
      </div>
    </el-header>
  </el-container>


</template>

<script>
  export default {

    name: 'LuffyHeader',

    data() {
      return {
        isShow: false,
        navlinks: [
          {id: 1, title: '首页', name: "Home"},
          {id: 2, title: '全部课程', name: "Course"},
          {id: 3, title: '在线题库', name: "LightCourse"},
          {id: 4, title: '学位课程', name: "Micro"}

        ]
      }
    },
    methods: {
      shopCartInfo() {
        this.$router.push({
          name: 'purchase.shop'
        })
      },

      myorder() {
        this.$router.push({
          name: "my_order"
        })
      },

      enterHandler() {
        this.isShow = true;
      },
      leaveHandler() {
        this.isShow = false;
      },
      goLoginHandler() {
        this.$router.push({
          name: 'Login'
        });
        // this.$router.redirct('/login/')
      },

      logoutHandler() {
        this.$http.logout()
          .then(res => {
            localStorage.clear();
            // sessionStorage.removeItem('store');
            this.$store.dispatch('accountLogout');
            this.isShow = false;
            this.$router.push({
              name: 'Home'
            })
          })
          .catch(err => {
              console.log(err)
          })

      },

    },
    created() {
      // console.log('导航组件加载了')
      if (localStorage.getItem('token') != null) {
        let user = {
          token: localStorage.getItem('token'),
          username: localStorage.getItem('username'),
          head_img: localStorage.getItem('avatar'),
        };
        this.$store.dispatch('getUserInfo', user);
      }
    },
    computed: {
      userInfo() {
        //cookie的取法
        // let userInfo = {
        //   access_token: this.$cookies.get('access_token'),
        //   notice_num: this.$cookies.get('notice_num'),
        //   shop_cart_num: this.$cookies.get('shop_cart_num'),
        //   avatar: this.$cookies.get('avatar'),
        //   username: this.$cookies.get('username')
        // };
        //vuex的取法
        return this.$store.state.userinfo
      }
    }

  };
</script>

<style lang="css" scoped>
  .el-header {
    border-bottom: #c9c9c9;
    box-shadow: 0 0.5px 0.5px 0 #c9c9c9;
  }

  .header {
    width: 1200px;
    height: 80px;
    line-height: 80px;
    margin: 0 auto;
  }

  .nav-left {
    float: left;
    margin-top: 10px;
  }

  .nav-center {
    float: left;
    margin-left: 100px;
  }

  .nav-center ul {
    overflow: hidden;
  }

  .nav-center ul li {
    float: left;
    margin: 0 5px;
    /*width: 100px;*/
    padding: 0 20px;
    height: 80px;
    line-height: 80px;
    text-align: center;
    position: relative;
  }

  .nav-center ul li a {
    color: #4a4a4a;
    width: 100%;
    height: 60px;
    display: inline-block;

  }

  .nav-center ul li a:hover {
    color: #B3B3B3;
  }

  .nav-center ul li a.is-active {
    color: #4a4a4a;
    border-bottom: 4px solid #ffc210;
  }

  .nav-center ul li span {
    color: red;
    font-size: 12px;
    position: absolute;
    top: -12px;
    right: -3px;
  }

  .nav-right {
    float: right;
    position: relative;
    z-index: 100;

  }

  .nav-right span {
    cursor: pointer;
  }

  .nav-right .user {
    margin-left: 15px;
  }

  .nav-right img {
    width: 26px;
    height: 26px;
    border-radius: 50%;
    display: inline-block;
    vertical-align: middle;
    margin-left: 15px;
  }

  .nav-right ul {
    position: absolute;
    width: 221px;
    z-index: 100;
    font-size: 12px;
    top: 80px;
    background: #fff;
    border-top: 2px solid #d0d0d0;
    box-shadow: 0 2px 4px 0 #e8e8e8;
  }

  .nav-right ul li {
    height: 40px;
    color: #4a4a4a;
    padding-left: 30px;
    padding-right: 20px;
    font-size: 12px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    cursor: pointer;
    transition: all .2s linear;
  }

  .nav-right ul li span.msg {
    margin-left: -80px;
    color: red;
  }

  .nav-right ul li span.count {
    margin-left: -100px;
    color: red;
  }


</style>
