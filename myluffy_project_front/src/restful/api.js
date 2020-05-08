import Axios from 'axios'

// Axios.defaults.baseURL = 'https://www.luffycity.com/api/v1/';
Axios.defaults.baseURL = 'http://127.0.0.1:8000/';
// const categoryUrl = '/course_sub/category/list/?belong=0';
const categoryUrl = '/category/';
// const courseUrl = '/courses/?sub_category=';
const courseUrl = '/course/?category_id=';
// const courseDetailUrl='';
const courseDetailUrl='/course/detail/';
// const captchaCheckUrl = '/captcha_check/';
const captchaCheckUrl = '/captcha_verify/';
// const loginUrl='/account/login/';
const loginUrl='/login/';
// const user_shop_car_url = '';
// const shop_car_list_url = '';
// const shop_car_update_url = '';
const user_shop_car_url = '/shoppingcar/';

const account_url = '/account/';
const logout_url = '/logout/';


const go_pay_url = '/get_pay_url/';
const payment_url = '/payment/';
const myOrderList_url = '/myorder/';


//请求拦截
Axios.interceptors.request.use(function (config) {
    // 在发送请求之前做些什么
    if (localStorage.getItem('token')) {
    	// Axios.defaults.headers.common['Authorization'] = localStorage.getItem('access_token');
    	// console.log(config.headers);
    	config.headers.Authorization = localStorage.getItem('token')
    }
    // 更改加载的样式

    return config;
  }, function (error) {
    // 对请求错误做些什么
    return Promise.reject(error);
});



export function categoryList(){
  return Axios.get(categoryUrl).then(res=>res.data)
}
export function courseList(categoryId){
  return Axios.get(`${courseUrl}${categoryId}`).then(res=>res.data)
}
export function courseDetail(course_id) {
  return Axios.get(`${courseDetailUrl}${course_id}/`).then(res=>res.data)
}
export function geetest() {
  return Axios.get(`${captchaCheckUrl}`).then(res=>res.data)
}

export function userLogin(params) {
  return Axios.post(`${loginUrl}`,params).then(res=>res)
}

export function add_shop_car(params) {
  return Axios.post(`${user_shop_car_url}`,params).then(res=>res.data)
}
export function shoppingcar() {
  return Axios.get(`${user_shop_car_url}`).then(res=>res.data)
}

export function removeCourse(params){
	return Axios.delete(`${user_shop_car_url}`,{data:params}).then(res=>res);
}

export function account(params) {
  return Axios.post(`${account_url}`,params).then(res=>res.data)
}

export function account_list() {
  return Axios.get(`${account_url}`).then(res=>res.data)
}

export function total_price(params) {
  return Axios.put(`${account_url}`,params).then(res=>res.data)
}

export function logout(){
  return Axios.delete(`${logout_url}`).then(res=>res.data)
}

//支付
export const payment = (params)=>{

  return Axios.post(`${payment_url}`,params).then(res=>res.data);
};

//我的订单
export const myOrderList = ()=>{
   return Axios.get(`${myOrderList_url}`).then(res=>res.data);

};
//去支付
export const go_pay = (order_number,final_price)=>{
  return Axios.get(`${go_pay_url}?order_number=${order_number}&final_price=${final_price}`).then(res=>res.data);
};


