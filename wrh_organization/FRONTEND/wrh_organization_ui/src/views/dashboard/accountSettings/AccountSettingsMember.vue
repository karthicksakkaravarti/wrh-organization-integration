<template>
  <v-card
    flat
    class="pa-3 mt-2" :class="{'no-member': !accountData.id}"
  >
    <v-card-text class="d-flex">
      <v-avatar
        rounded
        size="120"
        class="me-6"
      >
        <v-img :src="avatarChosenFileData || accountData.user.avatar || require('@/assets/images/misc/no-profile.png')"></v-img>
      </v-avatar>

      <!-- upload photo -->
      <div>
        <v-btn
          small
          color="primary"
          class="me-3 mt-5"
          @click="avatarImageRef.click()"
        >
          <v-icon class="d-sm-none">
            {{ icons.mdiCloudUploadOutline }}
          </v-icon>
          <span class="d-none d-sm-block">Choose new photo</span>
        </v-btn>

        <input
          ref="avatarImageRef"
          type="file"
          accept=".jpeg,.png,.jpg,GIF"
          :hidden="true"
          @change="onChangeAvatarFile"
        />

        <v-btn
          small
          color="warning"
          outlined
          class="mt-5 mr-2"
          @click="clearChosenAvatar()"
          :disabled="!avatarChosenFile"
        >
          Reset
        </v-btn>
        <v-btn
          small
          color="error"
          outlined
          class="mt-5 mr-2"
          @click="clearChosenAvatar(); accountData.user.avatar=null"
        >
          Delete
        </v-btn>

        <p class="text-sm mt-5">
          Allowed JPG, GIF or PNG. Max size of 10MB
        </p>
      </div>
    </v-card-text>

    <v-card-text>
      <v-form class="multi-col-validation mt-6">
        <v-row>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="accountData.user.username"
              label="Username"
              dense
              outlined
              disabled
            ></v-text-field>
          </v-col>

          <v-col cols="12" md="6">
            <v-text-field
              v-model="accountData.email"
              label="E-mail"
              dense
              outlined
              :disabled="accountDataOrig.email && accountDataOrig.email_verified"
              :suffix="accountDataOrig.email && accountDataOrig.email_verified? 'Verified': accountDataOrig.email? 'Not Verified!': ''"
            >
              <template #append v-if="accountDataOrig.email && !accountDataOrig.email_verified">
                <v-tooltip bottom color="info">
                  <template v-slot:activator="{ on, attrs }">
                    <v-icon size="20" v-bind="attrs" v-on="on" @click="$refs.verifyDialogRef.show('email', accountDataOrig.email)">{{icons.mdiEmailSend}}</v-icon>
                  </template>
                  <span>Click here to verify your E-mail</span>
                </v-tooltip>
              </template>
            </v-text-field>
          </v-col>

          <v-col md="6" cols="12">
            <v-text-field
              v-model="accountData.first_name"
              label="First Name"
              dense
              outlined
            ></v-text-field>
          </v-col>

          <v-col md="6" cols="12">
            <v-text-field
              v-model="accountData.last_name"
              label="Last Name"
              dense
              outlined
            ></v-text-field>
          </v-col>

          <v-col cols="12" md="6">
            <v-menu
              ref="birthDateMenuRef"
              v-model="showBirthDateMenu"
              :close-on-content-click="false"
              transition="scale-transition"
              offset-y
              min-width="auto"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  v-model="accountData.birth_date"
                  label="Birth Date"
                  :append-icon="icons.mdiCalendar"
                  readonly
                  v-bind="attrs"
                  v-on="on"
                  outlined
                  dense
                ></v-text-field>
              </template>

              <v-date-picker
                ref="birthDatePickerRef"
                v-model="accountData.birth_date"
                :active-picker.sync="birthDateActivePicker"
                :max="new Date().toISOString().slice(0, 10)"
                min="1940-01-01"
                color="primary"
                @change="(d) => {$refs.birthDateMenuRef.save(d)}"
              ></v-date-picker>
            </v-menu>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
               :disabled="accountData.usac_license_number_verified"
               :color="accountData.usac_license_number_verified ? 'success' : 'warning'"
                :prepend-icon="accountData.usac_license_number_verified ? icons.mdiCheck : icons.mdiAlert"
                v-model="accountData.usac_license_number"
                outlined
                label="USAC License# (optional)"
                placeholder="USAC License# (optional)"
                hide-details
                class="mb-3"
                :rules="[]"
                dense
              ></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="accountData.phone"
              v-mask="phoneMask"
              outlined
              dense
              :disabled="accountDataOrig.phone && accountDataOrig.phone_verified"
              label="Phone"
              :suffix="accountDataOrig.phone && accountDataOrig.phone_verified? 'Verified': accountDataOrig.phone? 'Not Verified!': ''"
            >
              <template #append v-if="accountDataOrig.phone && !accountDataOrig.phone_verified">
                <v-tooltip bottom color="info">
                  <template v-slot:activator="{ on, attrs }">
                    <v-icon size="20" v-bind="attrs" v-on="on" @click="$refs.verifyDialogRef.show('phone', accountDataOrig.phone)">{{icons.mdiEmailSend}}</v-icon>
                  </template>
                  <span>Click here to verify your phone</span>
                </v-tooltip>
              </template>
            </v-text-field>
          </v-col>

          <v-col cols="12" md="6">
            <p class="text--primary mt-n3 mb-2">
              Gender
            </p>
            <v-radio-group
              v-model="accountData.gender"
              row
              class="mt-0"
              hide-details
            >
              <v-radio v-for="o in $const.GENDER_OPTIONS" :key="o.value"
                :value="o.value"
                :label="o.title"
              >
              </v-radio>
            </v-radio-group>
          </v-col>

          <v-col cols="12" sm="6" md="3">
            <v-text-field type="number" v-model="accountData.weight" outlined dense label="Weight (For E-Sports)" suffix="kg"></v-text-field>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <v-text-field type="number" v-model="accountData.height" outlined dense label="Height (For E-Sports)" suffix="m"></v-text-field>
          </v-col>

          <v-col
            cols="12"
            md="6"
          >
            <v-autocomplete
              v-model="accountData.country"
              outlined
              dense
              label="Country"
              :items="$const.COUNTRY_OPTIONS"
              item-text="name"
              item-value="code"
            ></v-autocomplete>
          </v-col>

          <v-col cols="12" md="6">
            <v-text-field
              v-model="accountData.state"
              outlined
              dense
              label="State"
            ></v-text-field>
          </v-col>

          <v-col cols="12" md="6">
            <v-text-field
              v-model="accountData.city"
              outlined
              dense
              label="City"
            ></v-text-field>
          </v-col>

          <v-col cols="12" md="6">
            <v-text-field
              v-model="accountData.zipcode"
              outlined
              dense
              label="Zipcode"
            ></v-text-field>
          </v-col>

          <v-col cols="12" md="6">
            <v-text-field
              v-model="accountData.address1"
              outlined
              dense
              label="Address 1"
            ></v-text-field>
          </v-col>

          <v-col cols="12" md="6">
            <v-text-field
              v-model="accountData.address2"
              outlined
              dense
              label="Address 2"
            ></v-text-field>
          </v-col>


          <v-col cols="12 d-flex">
            <v-btn color="primary" class="me-3 mt-4" @click.prevent="save()" type="submit">
              Save changes
            </v-btn>
            <v-btn color="warning" outlined class="mt-4" type="reset"
                   @click.prevent="loadAccountData(); clearChosenAvatar()">
              Reset
            </v-btn>
            <v-spacer></v-spacer>
            <v-btn link color="secondary" class="mt-4" :to="{name: $rns.DASHBOARD_MEMBER_PROFILE}">
              Cancel
            </v-btn>
          </v-col>
        </v-row>
      </v-form>
    </v-card-text>
    <v-overlay :value="saving || loading" :absolute="true" opacity="0.3">
      <v-progress-circular indeterminate></v-progress-circular>
    </v-overlay>
    <verify-dialog ref="verifyDialogRef" @verify-successed="verifyDialogSuccessed" @verify-failed="verifyDialogFailed">
    </verify-dialog>
  </v-card>
</template>

<script>
import { mdiAlertOutline, mdiCloudUploadOutline, mdiEmailSend, mdiCalendar , mdiCheck, mdiAlert} from '@mdi/js'
import {nextTick, onMounted, ref} from '@vue/composition-api'
import axios from "@/axios";
import store from "@/store";
import {
  notifyDefaultServerError,
  notifySuccess,
  notifyError,
  internationalPhoneMask
} from "@/composables/utils";
import EventBus from "@/EventBus";
import VerifyDialog from "@/views/dashboard/accountSettings/VerifyDialog";
import {watch} from "@vue/composition-api/dist/vue-composition-api";
import {routeNames} from "@/router";
import {useRouter} from "@core/utils";

export default {
  components: {VerifyDialog},
  props: {
  },
  setup(props) {
    const { router } = useRouter();
    const birthDateActivePicker = ref(null);
    const accountDataOrig = ref({user: {}});
    const accountData = ref({user: {}});
    const loading = ref(false);
    const saving = ref(false);
    const avatarChosenFile = ref(null);
    const avatarChosenFileData = ref(null);
    const avatarImageRef = ref(null);
    const phoneMask = ref(null);
    const showBirthDateMenu = ref(false);
    const birthDatePickerRef = ref(null);

    watch(showBirthDateMenu, val => {
      // eslint-disable-next-line no-return-assign
      val && setTimeout(() => (birthDateActivePicker.value = 'YEAR'));
    });

    const cloneData = () => {
        var data = Object.assign({}, accountDataOrig.value);
        data.user = Object.assign({}, data.user);
        return data;
    };

    const loadAccountData = () => {
      loading.value = true;
      phoneMask.value = null;
      axios.get("cycling_org/member/me", {params: {xfields: "social_media"}}).then((response) => {
        accountDataOrig.value = response.data;
        accountData.value = cloneData();
        nextTick(() => {
          phoneMask.value = internationalPhoneMask;
        });
        loading.value = false;
      }, (error) => {
        loading.value = false;
        notifyDefaultServerError(error, true)
      });
    };

    const clearChosenAvatar = () => {
      avatarChosenFile.value = null;
      avatarChosenFileData.value = null;
      if (avatarImageRef.value) {
        avatarImageRef.value.value = null;
      }
    };

    const onChangeAvatarFile = (event) => {
      if (event.target.files.length > 0) {
        avatarChosenFile.value = event.target.files[0];
        var f = avatarChosenFile.value,
          r = new FileReader();
        r.onloadend = (e) => {
          avatarChosenFileData.value = e.target.result;
        };
        r.readAsDataURL(f);
      }
    };

    const save = () => {
      saving.value = true;
      var data = Object.assign({}, accountData.value);
      data.user = Object.assign({}, data.user);
      if (avatarChosenFileData.value) {
        data.user.avatar = avatarChosenFileData.value;
      } else if (data.user.avatar !== null) {
        delete data.user.avatar;
      }
      if (!data.usac_license_number) {
        data.usac_license_number = null;
      }
      axios.patch("cycling_org/member/me", data).then((response) => {
        saving.value = false;
        accountDataOrig.value = response.data;
        accountData.value = cloneData();
        store.state.currentUser.avatar = accountData.value.user.avatar;
        clearChosenAvatar();
        EventBus.emit("user:session-refresh");
        notifySuccess("data saved successfully");
        router.push({name: routeNames.DASHBOARD_MEMBER_PROFILE});
      }, (error) => {
        saving.value = false;
        notifyDefaultServerError(error, true);
      });
    };

    const verifyDialogSuccessed = (type, to) => {
      notifySuccess(`${type} verified successfully.`);
      loadAccountData();
    };

    const verifyDialogFailed = (type, to) => {
      notifyError('Incorrect code!');
    };

    onMounted(() => {
      loadAccountData();
    });

    return {
      birthDateActivePicker,
      accountData,
      accountDataOrig,
      loading,
      saving,
      loadAccountData,
      clearChosenAvatar,
      avatarChosenFile,
      avatarChosenFileData,
      avatarImageRef,
      onChangeAvatarFile,
      verifyDialogSuccessed,
      verifyDialogFailed,
      save,
      phoneMask,
      showBirthDateMenu,
      birthDatePickerRef,
      icons: {
        mdiAlertOutline,
        mdiCloudUploadOutline,
        mdiEmailSend,
        mdiCalendar,
        mdiCheck,
        mdiAlert
      },
    }
  },
}
</script>

<style scoped>
  .no-member {
    opacity: 0.5;
    pointer-events: none;
  }
</style>
