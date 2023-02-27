<template>
  <div>
    <!-- Form Drawer -->
    <v-navigation-drawer
      v-model="$store.state.Drawer.DrawerModel"
      :width="$store.state.Drawer.DrawerSize"
      app
      right
      temporary
      absolute
      hide-overlay
      :permanent="$store.state.Drawer.DrawerModel"
    >
      <v-app-bar v-if="$store.state.Drawer.DrawerShowAppBar" dense elevation="0" flat rounded shaped>
        <v-menu rounded open-on-hover top dense offset-x style="max-width: 600px">
          <template v-slot:activator="{ on, attrs }">
            <v-icon color="primary" v-bind="attrs" v-on="on" @click="showBar = true">mdi-apps</v-icon>
          </template>

          <!-- <v-list dense>
            <v-list-item-group v-model="defaultApp">
              <v-list-item :value="item.name" v-for="(item, index) in $store.state.Apps" :key="index">
                <v-list-item-icon
                  ><v-icon color="primary">{{ item.icon }}</v-icon></v-list-item-icon
                >

                <v-list-item-title>{{ item.name }}</v-list-item-title>
              </v-list-item>
            </v-list-item-group>
          </v-list> -->
        </v-menu>

        {{
          $store.state.Drawer.DrawerFormTitle ? $store.state.Drawer.DrawerFormTitle : $store.state.Drawer.DrawerFormType
        }}
        <v-spacer></v-spacer>
        <BaseButton :icon="true" mdi_icon="mdi-close" click="CloseDrawer" :options="{}" tooltip="Close" />&nbsp;&nbsp;
      </v-app-bar>

      <v-overlay absolute :value="$store.state.Drawer.DrawerLoader">
        <v-progress-circular color="primary" indeterminate size="30"></v-progress-circular>
      </v-overlay>
      <!-- Forms Type -->
      <v-card elevation="0" :disabled="$store.state.Drawer.DrawerLoader">
        <v-card-text class="ma-0 pa-0">
          <!-- <UserInfo v-if="$store.state.Drawer.DrawerFormType == 'UserInfo'" />
          <NewProject
            v-else-if="
              $store.state.Drawer.DrawerFormType == 'NewProject' || $store.state.Drawer.DrawerFormType == 'EditProject'
            "
          />
          <ResourceRequest v-if="$store.state.Drawer.DrawerFormType == 'NewResourceRequest'" />
          <NewCR v-else-if="$store.state.Drawer.DrawerFormType == 'NewCR'" /> -->
          <FormGenerator drawer="Drawer" ref="Drawer_form" />
          <template v-if="['ResourceAdd'].includes($store.state.Drawer.DrawerFormType)">
            <component  :is="$store.state.Drawer.DrawerFormType"></component>
          </template>
        </v-card-text>
      </v-card>
      <template v-slot:append>
        <div  class="ma-2 d-flex justify-start">
          <v-btn small color="primary" @click="drawer_form_submit">{{
            $store.state.Drawer.DrawerFormSubmit.btn_name
          }}</v-btn>
          <v-divider class="ma-1" vertical></v-divider>
          <BaseButton color="error" title="Cancel" click="CloseDrawer" :options="{}" />
        </div>
      </template>
    </v-navigation-drawer>

    
  </div>
</template>

<script>
import FormGenerator from '@/components/Forms/FormGenerator.vue'
import BaseButton from '@/components/Button/BaseButton.vue'

export default {
  data() {
    return {
      showBar: false,
      defaultApp: 'Project',
    }
  },
  components: {
    BaseButton,
    FormGenerator
  },
  watch: {
    defaultApp(value) {
      console.log(value)
      if (value == 'Customer') {
        this.$store.dispatch('OpenDrawerOnClick', {
          ShowAppBarOnDrawer: true,
          DrawerSize: '35%',
          DrawerFormType: 'NewCustomer',
          DrawerFormAPICall: true,
          DrawerMutation: 'mutation__second_drawer',
        })
      }
    },
  },
  methods: {
    drawer_form_submit() {
      this.$refs.Drawer_form.form_validation()
    },
    second_drawer_form_submit() {
      this.$refs.SecondDrawer_form.form_validation()
    },
  },
}
</script>