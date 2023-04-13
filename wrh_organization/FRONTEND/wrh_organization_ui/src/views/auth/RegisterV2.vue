<template>
  <v-card class="auth-card">


    <v-card-text>
      <v-row>
        <v-col col="12" sm="12">
         
        </v-col>
        <v-col cols="12" sm="4">
          <v-card-text >
            <p class="text-2xl font-weight-semibold text--primary mb-2">
              {{ $store.state.sitePrefs.site_ui__signup_page_title || 'Adventure starts here' }}
            </p>
            <p class="mb-2">
              {{ $store.state.sitePrefs.site_ui__signup_page_caption || 'Make your bicycling races easy and fun!' }}
            </p>
          </v-card-text>
        </v-col>
        <v-col cols="12" sm="8">
          <!-- title -->


          <!-- register form -->
          <v-card-text>
            <v-form @submit.prevent="register()" v-model="formValid">
              <v-row>
                <v-col cols="12" sm="6" class="ma-0 pa-0">
                  <v-text-field v-model="registerForm.email" outlined :append-icon="icons.mdiEmailOutline"
                    label="E-mail (Username)" placeholder="E-mail (Username)" class="mb-3" persistent-hint
                    hint="The E-mail will be used as your username on the login"
                    :rules="[rules.required, rules.emailValidator]" dense></v-text-field>
                </v-col>
                <v-col cols="12" sm="6" class="ma-0 pa-0 pl-2">
                  <v-text-field v-model="registerForm.confirm_email" outlined :append-icon="icons.mdiEmailOutline"
                    label="Confirm E-mail" placeholder="Enter E-mail again" class="mb-3"
                    :rules="[rules.required, rules.emailValidator, rules.confirmedValidator(registerForm.confirm_email, registerForm.email, 'The Confirm E-mail field confirmation does not match')]"
                    dense></v-text-field>
                </v-col>
                <v-col cols="12" sm="6" class="ma-0 pa-0">
                  <v-text-field v-model="registerForm.first_name" outlined label="First Name" placeholder="First Name"
                    hide-details class="mb-3" :rules="[rules.required]" dense></v-text-field>
                </v-col>
                <v-col cols="12" sm="6" class="ma-0 pa-0 pl-2">
                  <v-text-field v-model="registerForm.last_name" outlined label="Last Name" placeholder="Last Name"
                    hide-details class="mb-3" :rules="[rules.required]" dense></v-text-field>
                </v-col>
                <v-col cols="12" sm="6" class="ma-0 pa-0">
                  <v-text-field v-model="registerForm.password" outlined :type="isPasswordVisible ? 'text' : 'password'"
                    label="Password" placeholder="Password"
                    :append-icon="isPasswordVisible ? icons.mdiEyeOffOutline : icons.mdiEyeOutline" class=""
                    hint="Password should contains at least 1 digit with min 8 chars" persistent-hint
                    :rules="[rules.required]" dense @click:append="isPasswordVisible = !isPasswordVisible"></v-text-field>
                </v-col>

                <v-col cols="12" sm="6" class="ma-0 pa-0 pl-2">
                  <v-text-field v-model="registerForm.confirm_password" outlined
                    :type="isPasswordVisible ? 'text' : 'password'" label="Confirm Password"
                    placeholder="Confirm Password" class=""
                    :append-icon="isPasswordVisible ? icons.mdiEyeOffOutline : icons.mdiEyeOutline"
                    :rules="[rules.required, rules.confirmedValidator(registerForm.confirm_password, registerForm.password)]"
                    dense @click:append="isPasswordVisible = !isPasswordVisible"></v-text-field>
                </v-col>
                <v-col cols="12" sm="6" class="ma-0 pa-0">
                  <v-select outlined v-model="registerForm.gender" :items="$const.GENDER_OPTIONS" item-text="title"
                item-value="value" label="Gender" dense hide-details class="mb-3" :rules="[rules.required]"></v-select>

                </v-col>
                <v-col cols="12" sm="6" class="ma-0 pa-0 pl-2">
                  <v-menu ref="birthDateMenuRef" v-model="showBirthDateMenu" :close-on-content-click="false"
                transition="scale-transition" offset-y min-width="auto">
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field v-model="registerForm.birth_date" label="Birth Date" :append-icon="icons.mdiCalendar"
                    readonly v-bind="attrs" v-on="on" :rules="[rules.required]" outlined class="mb-3" hide-details
                    dense></v-text-field>
                </template>

                <v-date-picker ref="birthDatePickerRef" v-model="registerForm.birth_date"
                  :active-picker.sync="birthDateActivePicker" :max="new Date().toISOString().slice(0, 10)"
                  min="1940-01-01" color="primary" @change="(d) => { $refs.birthDateMenuRef.save(d) }"></v-date-picker>
              </v-menu>
                </v-col>
                <v-col cols="12" sm="6" class="ma-0 pa-0">
                  <v-menu ref="birthDateMenuRef" v-model="showBirthDateMenu" :close-on-content-click="false"
                transition="scale-transition" offset-y min-width="auto">
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field v-model="registerForm.birth_date" label="Birth Date" :append-icon="icons.mdiCalendar"
                    readonly v-bind="attrs" v-on="on" :rules="[rules.required]" outlined class="mb-3" hide-details
                    dense></v-text-field>
                </template>

                <v-date-picker ref="birthDatePickerRef" v-model="registerForm.birth_date"
                  :active-picker.sync="birthDateActivePicker" :max="new Date().toISOString().slice(0, 10)"
                  min="1940-01-01" color="primary" @change="(d) => { $refs.birthDateMenuRef.save(d) }"></v-date-picker>
              </v-menu>
                </v-col>
                <v-col cols="12" sm="6" class="ma-0 pa-0 pl-2">
                  <v-text-field v-model="registerForm.member.usac_license_number" outlined label="USAC License# (optional)"
                placeholder="USAC License# (optional)" hide-details class="mb-3" :rules="[]" dense></v-text-field>
                </v-col>
                <v-col cols="12" sm="6" class="ma-0 pa-0"></v-col>
                <v-col cols="12" sm="6" class="ma-0 pa-0"></v-col>
              </v-row>



              
              

              <!--        <v-text-field-->
              <!--            v-model="registerForm.member.phone"-->
              <!--            v-mask="$utils.internationalPhoneMask"-->
              <!--            :append-icon="icons.mdiPhoneOutline"-->
              <!--            outlined-->
              <!--            dense-->
              <!--            label="Phone"-->
              <!--        >-->
              <!--        </v-text-field>-->

              <!--        <v-autocomplete-->
              <!--            v-model="registerForm.member.country"-->
              <!--            outlined-->
              <!--            dense-->
              <!--            label="Country"-->
              <!--            :items="$const.COUNTRY_OPTIONS"-->
              <!--            item-text="name"-->
              <!--            item-value="code"-->
              <!--        ></v-autocomplete>-->

              <v-checkbox hide-details class="mt-1 agree-terms" v-model="registerForm.agree_terms">
                <template #label>
                  <span class="">I agree to</span>
                </template>
                <template #append>
                  <v-btn text color="primary" link small @click.capture="$refs.termsOfServiceDialogRef.show()"
                    class="pl-0 pr-1 pb-1">
                    privacy policy &amp; terms
                  </v-btn>
                </template>
              </v-checkbox>
              <user-agrement-legal-waver-dialog ref="uglw"></user-agrement-legal-waver-dialog>
              <turnstile-component v-if="turnstileSiteKey" ref="turnstileCmpRef" id="signup-turnstile-widget"
                :sitekey="turnstileSiteKey" @verify="onVerifyTurnstile" @expire="$refs.turnstileCmpRef.reset()"
                @fail="onFailTurnstile" @timeout="onFailTurnstile"></turnstile-component>

              <v-btn block type="submit" color="primary" class="mt-6" :loading="registering"
                :disabled="!registerForm.agree_terms || !$refs.uglw.agreementAccept || !registerForm.turnstile_token || !turnstileSiteKey || !formValid">
                Sign Up
              </v-btn>
            </v-form>
          </v-card-text>
        </v-col>
      </v-row>
    </v-card-text>


    <!-- divider -->
    <!-- <v-card-text class="d-flex align-center mt-2">
      <v-divider></v-divider>
      <span class="mx-5">or</span>
      <v-divider></v-divider>
    </v-card-text> -->

    <!-- social link -->
    <!-- <v-card-actions class="d-flex justify-center">
      <v-btn v-for="link in socialLink" :key="link.icon" icon class="ms-1">
        <v-icon :color="$vuetify.theme.dark ? link.colorInDark : link.color">
          {{ link.icon }}
        </v-icon>
      </v-btn>
    </v-card-actions> -->
    <terms-of-service-dialog ref="termsOfServiceDialogRef"></terms-of-service-dialog>
  </v-card>
</template>

<script>
// eslint-disable-next-line object-curly-newline
import {
  mdiEmailOutline,
  mdiPhoneOutline,
  mdiCalendar,
  mdiFacebook,
  mdiTwitter,
  mdiGithub,
  mdiGoogle,
  mdiEyeOutline,
  mdiEyeOffOutline
} from '@mdi/js'
import { onBeforeUnmount, onMounted, ref, watch } from '@vue/composition-api'
import themeConfig from '@themeConfig'
import { required, emailValidator, passwordValidator, confirmedValidator } from '@core/utils/validation'
import axios from "@/axios";
import { notifyDefaultServerError, notifySuccess, notifyError, randomId } from "@/composables/utils";
import TermsOfServiceDialog from "@/views/public/TermsOfServiceDialog.vue";
import UserAgrementLegalWaverDialog from "@/views/public/UserAgrementLegalWaverDialog.vue";
import TurnstileComponent from "@/components/TurnstileComponent.vue";

export default {
  components: { TurnstileComponent, TermsOfServiceDialog, UserAgrementLegalWaverDialog },
  setup(props, context) {
    const birthDateActivePicker = ref(null);
    const isPasswordVisible = ref(false);
    const registering = ref(false);
    const formValid = ref(false);
    const showBirthDateMenu = ref(false);
    const birthDatePickerRef = ref(null);
    const registerForm = ref({ member: { country: "US" }, turnstile_token: null });

    const socialLink = [
      {
        icon: mdiFacebook,
        color: '#4267b2',
        colorInDark: '#4267b2',
      },
      {
        icon: mdiTwitter,
        color: '#1da1f2',
        colorInDark: '#1da1f2',
      },
      {
        icon: mdiGithub,
        color: '#272727',
        colorInDark: '#fff',
      },
      {
        icon: mdiGoogle,
        color: '#db4437',
        colorInDark: '#db4437',
      },
    ];

    const turnstileSiteKey = ref(null);

    onMounted(() => {
      loadTurnstileSiteKey();
    });

    watch(showBirthDateMenu, val => {
      val && setTimeout(() => (birthDateActivePicker.value = 'YEAR'))
    });

    const loadTurnstileSiteKey = () => {
      axios.get("cycling_org/global_conf/TURNSTILE_SITE_KEY").then(
        response => {
          turnstileSiteKey.value = response.data;
        },
        error => {
          notifyDefaultServerError(error, true);
        }
      );
    };

    const onVerifyTurnstile = (token) => {
      registerForm.value.turnstile_token = token;
    };

    const onFailTurnstile = () => {
      notifyError('Something is wrong. refresh the page and try again!')
    };

    const register = () => {
      registering.value = true;
      axios.post("cycling_org/users/registration", registerForm.value).then((response) => {
        registering.value = false;
        notifySuccess("You must activate your account using the link sent to your email, before logging in.", 0);
        context.emit("change-page", "Login");
      }, (error) => {
        registering.value = false;
        notifyDefaultServerError(error, true);
      });
    };


    return {
      birthDateActivePicker,
      isPasswordVisible,
      registerForm,
      socialLink,
      registering,
      formValid,
      showBirthDateMenu,
      birthDatePickerRef,
      register,
      turnstileSiteKey,
      onVerifyTurnstile,
      onFailTurnstile,
      rules: {
        required, emailValidator, confirmedValidator
      },

      // Icons
      icons: {
        mdiEyeOutline,
        mdiEyeOffOutline,
        mdiCalendar,
        mdiPhoneOutline,
        mdiEmailOutline,
      },

      // themeConfig
      appName: themeConfig.app.name,
      appLogo: themeConfig.app.logo,
    }
  },
}
</script>
<style>
.auth-card .agree-terms .v-input__control {
  width: auto;
  flex-grow: 0;
}
</style>

;


return {

  birthDateActivePicker,
  isPasswordVisible,
  reeistesF:rm,
  socialLink,
  registering,
  formValid,
  sho BirthDateMenu,
  birthDatePickerRef,
  register,
  turnstileSiteKey,
  onVerifyTurnstile,
  onFailTurnstile,
  rules: {
    required,
    emailValidator,
    confirmedValidator
  }

  ,

  // Icons
  icons{ {
    mdiEyeOutline,
    mdiEyeOffOutline,

   mdiCalendar,
    mdiPhoneOutline,
    mdiEmailOutline,
  }

  ,

  // themeConfig
  appName: themeConfig.app.name,  appLogo: themeConfig.app.logo,
}
}

,
 
     required, emailValidator, confirmedValidator
   crip ><st  },.auth-card .agree-terms .v-input__control {
  width: auto;
  flex-grow: 0;
}

      // Icons
      icons: {
        mdiEyeOutline,
        mdiEyeOffOutline,
        mdiCalendar,
        mdiPhoneOutline,
        mdiEmailOutline,
      },

      // themeConfig
      appName: themeConfig.app.name,
      appLogo: themeConfig.app.logo,
    }
  },
}
</script>
<style>
  .auth-card .agree-terms .v-input__control {
    width: auto;
    flex-grow: 0;
  }
  setup(props, context) {
    const birthDateActivePicker = ref(null);
    const isPasswordVisible = ef(false)
    const registering = ref(false);
    const formValid = ref(false);
    const showBirthDateMenu = ref(false);
    const birthDatePickerRef = ref(null);
    const registerForm = ref({ member: { country: "US" }, turnstile_token: null });

    const socialLink = [
      {
        icon: mdiFacebook,
        color: '#4267b2',
        colorInDark: '#4267b2',
      },
      {
        icon: mdiTwitter,
        color: '#1da1f2',
        colorInDark: '#1da1f2',
      },
      {
        icon: mdiGithub,
        color: '#272727',
        colorInDark: '#fff',
      },
      {
        icon: mdiGoogle,
        color: '#db4437',
        colorInDark: '#db4437',
      },
    ];

    const turnstileSiteKey = ref(null);

    onMounted(() => {
      loadTurnstileSiteKey();
    });

    watch(showBirthDateMenu, val => {
      val && setTimeout(() => (birthDateActivePicker.value = 'YEAR'))
    });

    const loadTurnstileSiteKey = () => {
      axios.get("cycling_org/global_conf/TURNSTILE_SITE_KEY").then(
        response => {
          turnstileSiteKey.value = response.data;
        },
        error => {
          notifyDefaultServerError(error, true);
        }
      );
    };

    const onVerifyTurnstile = (token) => {
      registerForm.value.turnstile_token = token;
    };

    const onFailTurnstile = () => {
      notifyError('Something is wrong. refresh the page and try again!')
    };

    const register = () => {
      registering.value = true;
      axios.post("cycling_org/users/registration", registerForm.value).then((response) => {
        registering.value = false;
        notifySuccess("You must activate your account using the link sent to your email, before logging in.", 0);
        context.emit("change-page", "Login");
      }, (error) => {
        registering.value = false;
        notifyDefaultServerError(error, true);
      });
    };


    return {
      birthDateActivePicker,
      isPasswordVisible,
      registerForm,
      socialLink,
      registering,
      formValid,
      showBirthDateMenu,
      birthDatePickerRef,
      register,
      turnstileSiteKey,
      onVerifyTurnstile,
      onFailTurnstile,
      rules: {
        required, emailValidator, confirmedValidator
      },

      // Icons
      icons: {
        mdiEyeOutline,
        mdiEyeOffOutline,
        mdiCalendar,
        mdiPhoneOutline,
        mdiEmailOutline,
      },

      // themeConfig
      appName: themeConfig.app.name,
      appLogo: themeConfig.app.logo,
      }
    },
  }
  </script>
<style>
.auth-card .agree-terms .v-input__control {
  width: auto;
  flex-grow: 0;
}
