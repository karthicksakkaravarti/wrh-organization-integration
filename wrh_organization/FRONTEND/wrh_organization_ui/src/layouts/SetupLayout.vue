<template>
  <v-app>
    <v-app-bar elevation="0" dense app>
      <div class="d-flex align-center">
        <div><v-icon color="primary">{{icons.mdiHammerScrewdriver}}</v-icon> Setup</div>
      </div>

      <v-spacer></v-spacer>
      <v-btn icon @click="$router.push('/')">
        <v-icon color="primary">{{icons.mdiClose}}</v-icon>
      </v-btn>
    </v-app-bar>
    <v-navigation-drawer permanent absolute v-bind:width="250" app>
      <div class="pa-2">
        <v-text-field
          :prepend-inner-icon="icons.mdiMagnify"
          dense
          filled
          rounded
          v-model="search"
          hide-details
          placeholder="Search"
        ></v-text-field>

        <v-list dense>
          <v-list-group :key="key" v-for="(config, key) in filteredItems" :value="true">
            <template v-slot:activator>
              <v-list-item-title>{{ config.name }}</v-list-item-title>
            </template>

            <v-list-item color="primary" :key="key" :to="children.to" v-for="(children, key) in config.childern" link>
              <v-list-item-title class="pl-4">{{ children.name }}</v-list-item-title>

              <v-list-item-icon> </v-list-item-icon>
            </v-list-item>
          </v-list-group>
        </v-list>
      </div>
    </v-navigation-drawer>

    <v-main>
      <slot></slot>
    </v-main>
  </v-app>
</template>

<script>

import { Setup } from '@/mixins/Setup'
import {
  mdiHammerScrewdriver,
  mdiClose,
  mdiMagnify
} from '@mdi/js'
export default {
  mixins: [Setup],
  components: {
  },
  data() {
    return {
      search: '',
      Configs: [
       
      ],
    }
  },
  computed: {
    filteredItems() {
      return this.Configs.filter(item => {
        return item.name.toLowerCase().match(this.search)
      })
    },
  },
  setup(){
    return {
      icons: {
        mdiHammerScrewdriver,
        mdiClose,
        mdiMagnify
      }
    }
  },
  mounted(){
    // Loading Layout
    this.SETUP_API_FORMMODEL_GET('?fields=id,name')
    .then(data => {
      var layouts = []
      var layout_fields = {
          name: 'Forms',
          childern: [
          ],
        }
      for (var field of data.data){
        layouts.push({ "name": field.name , "to": {"name": 'Form Edit', "params": { "form": field.name, "id": field.id } }})
      }
      layout_fields['childern'] = layouts
      this.Configs.push(layout_fields)
    })
    .catch(err => {
      console.error(err)
    })
  }
}
</script>

<style>
</style>