import axios from "@/axios";
const state = {
  ActionLoader: false,
  authentication: {
    config_name: '',
    value: '',
    options: {
      
    },
  },
}

const getters = {
  ActionLoader: state => state.ActionLoader,
  authentication: state => state.authentication,
}
const actions = {
  SETUP_API_APPBASIC_GET({ commit }, payload) {
    commit('ActonLoader', true)
    return new Promise((resolve, reject) => {
      axios.get('pm/api/appbasic' + payload.endpoint, )
        .then(data => {
          resolve(data)
          commit('ActonLoader', false)
          commit('mutation__authentication', data.data.results[0])
          
        })
        .catch(err => {
          reject(err)
          commit('ActonLoader', false)
          
        })
    })

  },

  SETUP_API_APPBASIC_POST({ commit }, payload) {
    commit('ActonLoader', true)
    return new Promise((resolve, reject) => {
      axios.post('pm/api/appbasic' + payload.endpoint, {
        config_name : payload.data.config_name,
        value : payload.data.value,
        options : JSON.stringify(payload.data.options),
      })
        .then(data => {
          resolve(data)
          commit('ActonLoader', false)
          
        })
        .catch(err => {
          reject(err)

          commit('ActonLoader', false)
         
        })
    })
  },

  SETUP_API_FORMMODEL_GET({commit}, query=''){
    commit('ActonLoader', true)
    return new Promise((resolve, reject) => {
      axios.get('setup/forms/'+query)
      .then(data => {
        resolve(data)
      })
      .catch(err => {
        reject(err)
      })
    })
  },
  SETUP_API_FORMMODEL_POST({commit}, payload){
    commit('ActonLoader', true)
    return new Promise((resolve, reject) => {
      axios.patch('setup/forms/'+payload.query_param+'/', payload.data)
      .then(data => {
        resolve(data)
      })
      .catch(err => {
        reject(err)
      })
    })
  },
}

const mutations = {
  ActonLoader(state, value) {
    // state.NonInvoData[value.key] = value.value
    state.ActionLoader = value
  },
  mutation__authentication(state, value) {
    // state.NonInvoData[value.key] = value.value
    if (!value.options){
      value.options = {
        app_id: '',
        app_secret: '',
        authority: '',
        redirect: '',
        scopes: '',
      }
    }
    state.authentication = Object.assign(state.authentication, value)

    // Json
    state.authentication.options = JSON.parse(value.options)
  },
}

export const SetupStore = {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
}
