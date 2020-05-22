import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

const store = new Vuex.Store({

  state:{
    userinfo:{},
  },
  mutations:{
    get_userinfo(state,data){
      state.userinfo = data;
    },
    account_logout(state){
      state.userinfo={};
      console.log('in mutations')
    }

  },
  actions:{
    getUserInfo(context,data){
      context.commit('get_userinfo',data);
    },
    accountLogout(context){
      context.commit('account_logout');
      console.log('in actions')
  }
  },


});

export default store;
