import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home/Home'
import Course from '@/components/Course/Course'
import LightCourse from '@/components/LightCourse/LightCourse'
import Micro from '@/components/Micro/Micro'
import CourseDetail from '@/components/Course/CourseDetail'
import Login from '@/components/Login/Login'
import Cart from '@/components/Cart/Cart'
import Account from '@/components/Cart/Account'
import MyOrder from '@/components/Order/MyOrder'
import PaySuccess from '@/components/Order/PaySuccess'

Vue.use(Router);

export default new Router({
  mode: 'history',
  linkActiveClass:'is-active',
  routes: [
    {
      path: '/',
      redirect: {name: 'Home'},
    },
    {
      path: '/home',
      name: 'Home',
      component: Home
    },
    {
      path: '/course',
      name: 'Course',
      component: Course
    },
    {
      path: '/lightcourse',
      name: 'LightCourse',
      component: LightCourse
    },
    {
      path: '/micro',
      name: 'Micro',
      component: Micro
    },
    {
      path: '/course/detail/:courseId',
      name: 'course_detail',
      component: CourseDetail
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: "/purchase/shopping_cart/",
      name: 'purchase.shop',
      component: Cart,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/buy',
      name: 'account',
      component: Account,
      meta: {
        requiresAuth: true
      }
    },
        {
      path:'/my/order',
      name:'my_order',
      component:MyOrder,
      meta: {
        requiresAuth: true
      }
    },
    {
      path:'/order/pay_success',
      name:'pay_success',
      component:PaySuccess,
      meta: {
        requiresAuth: true
      }
    },


  ]
})
