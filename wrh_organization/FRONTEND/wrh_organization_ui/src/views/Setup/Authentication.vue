<template>
  <v-card
    :loading='ActionLoader'
    flat
    class="pa-3"
  >
    <v-card-text>
      <v-form class="multi-col-validation">
        <v-row>
          <v-col
            cols="12"
            md="8"
            sm="6"
          >
            <v-row>
              <v-col cols="12">
                <span class="text-xs">Authentication Method</span>
                <v-radio-group
                  v-model="authentication.value"
                  row
                  hide-details
                  class="mt-2"
                >
                  <v-radio
                    value="basic-auth"
                    label="Basic Authentication"
                  ></v-radio>
                  <v-radio
                    value="ms-oauth"
                    label="Microsoft OAuth"
                    class="mt-3 mt-md-0"
                  ></v-radio>
                </v-radio-group>
              </v-col>

              <template v-if="authentication.value == 'ms-oauth'">
                <v-col cols="12">
                <v-text-field
                  label="app_id"
                  dense
                  v-model="authentication.options.app_id"
                  outlined
                ></v-text-field>
              </v-col>

              <v-col cols="12">
                <v-text-field
                  label="app_secret"
                  v-model="authentication.options.app_secret"
                  dense
                  outlined
                >
                </v-text-field>
              </v-col>

              <v-col
                cols="6"
                md="12"
              >
                <v-text-field
                  label="authority"
                  v-model="authentication.options.authority"
                  outlined
                  hint="https://login.microsoftonline.com/radisyscorp.onmicrosoft.com"
                  dense
                ></v-text-field>
              </v-col>

              <v-col
                cols="6"
                md="12"
              >
                <v-text-field
                  label="redirect"
                  v-model="authentication.options.redirect"
                  outlined
                  dense
                  hint="<Domain>/pm/microsoftOAuth/callback"
                ></v-text-field>
              </v-col>
              <v-col
                cols="6"
                md="12"
              >
                <v-textarea
                  label="scopes"
                  v-model="authentication.options.scopes"
                  outlined
                  dense
                  hint="Scopes separated by ','"
                ></v-textarea>
              </v-col>
              </template>
            </v-row>
          </v-col>

          

          <v-col cols="12">
            <v-btn
            :loading="ActionLoader"
            small
              @click="SETUP_API_APPBASIC_POST({'endpoint': '/authentication/', 'data': authentication })"
              color="primary"
              class="me-3 mt-3"
            >
              Save changes
            </v-btn>
            
          </v-col>
        </v-row>
      </v-form>
    </v-card-text>

    
  </v-card>
</template>

<script>
import { mdiAccountOutline, mdiCloudOutline, mdiHelpCircleOutline } from '@mdi/js'
import { ref } from '@vue/composition-api'
import { Setup } from "@/mixins/Setup";


export default {
  mixins: [Setup],
  mounted() {
    this.SETUP_API_APPBASIC_GET({'endpoint': '/?config_name=Auth'})
  },
  setup() {
    const selectedAuthMethod = ref('basic-auth')
    const currentPlan = ref(true)
    const isPlanUpgradeDialogVisible = ref(false)
    const selectedPlan = ref('standard')
   

    return {
      selectedAuthMethod,
      currentPlan,
      selectedPlan,
      isPlanUpgradeDialogVisible,
      icons: {
        mdiAccountOutline,
        mdiCloudOutline,
        mdiHelpCircleOutline,
      },
    }
  },
}
</script>
