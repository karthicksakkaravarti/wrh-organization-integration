<template>
  <div :class="`auth-wrapper ${pageVersion}`">
    <div class="auth-inner">
      <v-slide-x-transition :hide-on-leave="true">
        <component :key="activePage" :is="activePage" @change-page="(p) => {activePage=p}"></component>
      </v-slide-x-transition>
    </div>
  </div>
</template>

<script>
// eslint-disable-next-line object-curly-newline
import {onMounted, ref} from '@vue/composition-api'
import Login from "@/views/auth/Login";
import Register from "@/views/auth/Register";
import RegisterV2 from "@/views/auth/RegisterV2";
import ForgotPassword from "@/views/auth/ForgotPassword";
import {useRouter} from "@core/utils";

export default {
  components: {Register, Login, ForgotPassword, RegisterV2},
  setup() {
    const pages = {'Login': 'Login', 'Register': 'Register', 'RegisterV2':'RegisterV2', 'ForgotPassword': 'ForgotPassword', 'ForgotPasswordV2':'ForgotPasswordV2'};
    const { route } = useRouter();
    const pageVersion = ref('auth-v1')
    const activePage = ref('Login');
    onMounted(() => {
       console.log(route.value.query.page)
      if (pages[route.value.params.page]) {
        activePage.value = pages[route.value.params.page] || 'Login' ;
      } else if (pages[route.value.query.page]) {
        activePage.value = pages[route.value.query.page] || 'Login' ;
        if (route.value.query.page == 'RegisterV2'){
          console.log(route.value.query.page)
          pageVersion.value = 'auth-v2'
        }
      }
    });
    return {
      activePage,
      pageVersion
    }

  },
}
</script>

<style lang="scss" scoped>
@import '@core/preset/preset/pages/auth.scss';
</style>
