import appConfigStoreModule from '@core/@app-config/appConfigStoreModule'
import Vue from 'vue'
import Vuex from 'vuex'
import app from './app'
import { ThemeStore } from './Theme'
import EventBus from "@/EventBus";
import { SetupStore } from './Setup'
import axios from "@/axios";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    currentUser: {},
    currentMember: {},
    checkedAuthentication: false,
    sitePrefs: {},
    backendVersion: null,
    Drawer: {
      DrawerModel: false,
      DrawerShowAppBar: false,
      DrawerSize: '35%',
      DrawerFormType: '',
      DrawerForm: [],
      DrawerFormSubmit: {},
      DrawerLoader: true,
      DrawerFormAPICall: false,
      DrawerFormTitle: '',
      DrawerExtraParam: '',
    }, // Used to open drawer
    
  },
  mutations: {
    currentUser: function(state, user) {
      const oldState = state.currentUser;
      state.currentUser = user || {};
      if (state.currentUser.id) {
        EventBus.emit("user:login", state.currentUser);
      } else {
        EventBus.emit("user:logout", oldState);
      }
      EventBus.emit("user:change-state", {newUser: state.currentUser, oldUser: oldState});
    },
    mutation__drawer(state, value) {
      state.Drawer = Object.assign(state.Drawer, value)
    },
    mutation__reset_error_message(state) {
      try {
        for (var drawerField of state.Drawer.DrawerForm) {
          drawerField['error_message'] = null
        }
      } catch (_) {}
    },
    mutation__set_errors(state, value) {
      try {
        for (var [key, value] of Object.entries(value)) {
          for (var drawerField of state.Drawer.DrawerForm) {
            if (drawerField['dbfield'] == key) {
              drawerField['error_message'] = value[0]
            }
          }
        }
      } catch (err) {
        console.error(err)
      }
    }
  },
  actions: {
    API({ commit }, value) {
      return new Promise((resolve, reject) => {
        axios.get(value)
          .then(data => {
            resolve(data)
          })
          .catch(err => {
            reject(err)            
          })
      })
    },
    OpenDrawerOnClick({ commit }, value) {
      commit(value.DrawerMutation, {
        DrawerModel: true,
        DrawerShowAppBar: value.ShowAppBarOnDrawer,
        DrawerSize: value.DrawerSize,
        DrawerFormType: value.DrawerFormType,
        DrawerLoader: true,
        DrawerActionType: value.DrawerActionType,
        DrawerFormTitle: value.DrawerFormTitle,
        DrawerFormSubmit: value.DrawerFormSubmit,
        DrawerApiForm: value.DrawerApiForm,
        DrawerShowAction: value.DrawerShowAction,
      })
      var type = "form_name"
      if (value && value.DrawerFilterForm){type = "filter_name"}
      if (value && value.DrawerFormAPICall) {
        commit(value.DrawerMutation, { DrawerLoader: true })
        return new Promise((resolve, reject) => {
          axios.get(`pm/api/forms/get_form/?${type}=` + value.DrawerFormType+(value.DrawerExtraParam ? value.DrawerExtraParam : ''))
            .then(data => {
              commit(value.DrawerMutation, {
                DrawerForm: data.data,
                DrawerLoader: false
              })

              resolve(data)
            })
            .catch(err => {
              reject(err)
              commit(value.DrawerMutation, {
                DrawerForm: [],
                DrawerLoader: false
              })
            })
        })
      } else {
        commit(value.DrawerMutation, {
          DrawerModel: true,
          DrawerShowAppBar: value.ShowAppBarOnDrawer,
          DrawerSize: value.DrawerSize,
          DrawerFormType: value.DrawerFormType,
          DrawerLoader: false,
        })
      }
    },
    CloseDrawer({ commit }) {
      commit('mutation__drawer', { DrawerLoader: false ,DrawerModel: false , DrawerForm: []})
    },
  },
  getters: {
    isStaffUser: function (state) {
      return true === state.currentUser.is_staff;
    },
    isSuperUser: function (state) {
      return true === state.currentUser.is_superuser;
    },
    isStaffOrSuperUser: function (state) {
      return (
        true === (state.currentUser.is_staff || state.currentUser.is_superuser)
      );
    },
    isAuthenticated: function (state) {
      return !!state.currentUser.id;
    },
    userFullName: function (state) {
      var name = "";
      if (state.currentUser.id) {
        if (state.currentUser.first_name) {
          name = state.currentUser.first_name;
        }
        if (state.currentUser.last_name) {
          name += " " + state.currentUser.last_name;
        }
        name = name.trim();
        if (!name) {
          name = state.currentUser.username;
        }
      }
      return name;
    },
    userDisplayName: function (state) {
      if (state.currentUser.id) {
        var name = (state.currentUser.first_name || state.currentUser.username);
        return name.charAt(0).toUpperCase() + name.slice(1);
      }
      return "";
    },
    currentUserId: function (state) {
      return state.currentUser.id;
    },
    memberDisplayName: function (state) {
      if (state.currentMember.id) {
        var name = (state.currentMember.first_name || null);
        return name && (name.charAt(0).toUpperCase() + name.slice(1));
      }
      return "";
    },
    currentMemberId: function (state) {
      return state.currentMember.id;
    },
    defaultRegionalOrg: function (state) {
      return (state.currentUser.prefs || {}).default_regional_org || null;
    },
    Drawer: state => state.Drawer,
  },
  modules: {
    appConfig: appConfigStoreModule,
    app,
    ThemeStore,
    SetupStore
  },
})
