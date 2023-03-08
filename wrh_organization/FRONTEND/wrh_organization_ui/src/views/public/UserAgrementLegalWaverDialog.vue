<template>
  <v-dialog scrollable v-model="isVisible" max-width="800px">
    <template v-slot:activator="{ on, attrs }">
      <v-checkbox :rules="[rules.required]" v-model="agreementAccept">
        <template v-slot:label>
          <div>
            I accept the
            <v-tooltip bottom>
              <template v-slot:activator="{}">
                <v-btn
                  v-bind="attrs"
                  v-on="on"
                  text
                  @click="getAgreementText"
                  color="primary"
                  link
                  small
                  class="pl-0 pr-1 pb-1"
                >
                  Release Waiver
                </v-btn>
              </template>
              Agreement & Waiver
            </v-tooltip>
          </div>
        </template>
      </v-checkbox>
    </template>
    <v-card>
      <v-card-title class="text-h5 grey lighten-2">
        Agreement and Waiver
      </v-card-title>

      <v-card-text>
        <div v-html="userAgrement || ''"></div>
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="error" outlined @click="hide()">Close</v-btn>
      </v-card-actions>
    </v-card>
    <v-overlay :value="loading" :absolute="true" opacity="0.3">
      <v-progress-circular indeterminate></v-progress-circular>
    </v-overlay>
  </v-dialog>
</template>

<script>
import { ref, watch } from "@vue/composition-api";
import axios from "@/axios";
import { required } from "@core/utils/validation";
import {
  notifyDefaultServerError,
  notifySuccess,
  notifyWarn,
} from "@/composables/utils";

export default {
  props: {
    userAgreementPropsText: { default: null },
  },
  setup(props, context) {
    const userAgrement = ref(null);
    const isVisible = ref(false);
    const loading = ref(false);
    const agreementAccept = ref(false);

    const hide = () => {
      isVisible.value = false;
    };
    const getAgreementText = () => {
      if (props.userAgreementPropsText) {
        userAgrement.value = props.userAgreementPropsText;
      } else {
        loaduserAgrement();
      }
    };

    const loaduserAgrement = () => {
      loading.value = true;
      axios.get("cycling_org/global_pref/site_ui__user_agreement_waver").then(
        (response) => {
          loading.value = false;
          userAgrement.value = response.data;
        },
        (error) => {
          loading.value = true;
          notifyDefaultServerError(error, true);
        }
      );
    };

    return {
      isVisible,
      loading,
      userAgrement,
      loaduserAgrement,
      agreementAccept,
      hide,
      getAgreementText,
      rules: {
        required,
      },
    };
  },
};
</script>

<style scoped>
</style>
