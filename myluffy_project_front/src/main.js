// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import ElementUI from 'element-ui';
import VueCookies from 'vue-cookies'
Vue.use(VueCookies);
import 'element-ui/lib/theme-chalk/index.css';
Vue.use(ElementUI);
import App from './App'
import router from './router'
import '../static/global/myindex.css'
import LuffyHeader from '@/components/Common/LuffyHeader'
Vue.component(LuffyHeader.name,LuffyHeader);
// Vue.config.productionTip = false;
import * as api from './restful/api'
import '../static/global/gt'
import store from './store/index'


Vue.prototype.$http = api;
// Vue.prototype.$store = store;

/* eslint-disable no-new */

// 全局守卫
router.beforeEach((to, from, next) => {
if(to.meta.requiresAuth){ //表示用户访问该组件需要登录
  if(!localStorage.getItem('token')){
    next({
        name: 'Login'
      })
  }else{
    let user = {
        token:localStorage.getItem('token'),
        username:localStorage.getItem('username'),
        head_img:localStorage.getItem('avatar'),
      };
    store.dispatch('getUserInfo',user);
    next()
  }

}
else{
  //放行
  next()
}
});

let vm = new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>',

  created(){

    if (sessionStorage.getItem('store')) {
      this.$store.replaceState(Object.assign({}, this.$store.state, JSON.parse(sessionStorage.getItem('store'))))
    }
    // 在页面刷新时将store保存到sessionStorage里
    window.addEventListener('beforeunload', () => {
      sessionStorage.setItem('store', JSON.stringify(this.$store.state))
    })
  }


});
