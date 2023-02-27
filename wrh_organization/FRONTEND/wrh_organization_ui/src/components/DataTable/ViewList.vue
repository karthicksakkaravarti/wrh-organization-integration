<template>
  <v-data-table
    class="user-search me-3 mb-4 row-pointer"
    :headers="generate_headers"
    :loading="loader"
    :show-select="show_select"
    v-model="selected"
    @click:row="handleClick"
    :options.sync="table_pagination"
    :server-items-length="items.count"
    :items="items.results"
  >
    <template v-slot:header.data-table-select="{ on, props }">
      <TableColoumnConfig @header_list="set_header" :FieldList="headers"> </TableColoumnConfig>
    </template>
    <template v-slot:item.data-table-select="{ isSelected, select }">
      <v-simple-checkbox
        v-if="show_select_checkbox"
        color="primary"
        :value="isSelected"
        @input="select($event)"
      ></v-simple-checkbox>
    </template>
    <template v-slot:top>
      <v-toolbar flat color="white">
        <v-toolbar-title
          ><b>{{ title }}</b></v-toolbar-title
        >
        <div class="ml-2 mt-0">
          <BaseButton
            :outlined="true"
            :rounded="true"
            mdi_icon="mdi-filter"
            click="OpenDrawerOnClick"
            title="Filter"
            tooltip="Apply Filter"
            :options="{
              ShowAppBarOnDrawer: true,
              DrawerSize: '25%',
              DrawerFormType: options.filter_table,
              DrawerFormTitle: 'Filter',
              DrawerFormAPICall: true,
              DrawerFilterForm: true,
              DrawerMutation: 'mutation__drawer',
              DrawerActionType: 'new',
              DrawerFormSubmit: {
                btn_name: 'Apply',
                store_action_name: '',
                custom_action: '',
              },
            }"
          />
        </div>
        <v-spacer></v-spacer>

        <v-card-title small class="ma-0 pa-0">
          <v-text-field
            rounded
            filled
            dense
            class="mt-4"
            v-debounce:1000="search"
            :prepend-inner-icon="icons.mdiMagnify"
            label="Search"
            single-line
            clearable
            v-model="search_text"
          ></v-text-field>
        </v-card-title>
      </v-toolbar>
    </template>

    <template v-slot:item.status="{ item }">
      <slot name="item-status" :item="item"> </slot>
    </template>
    <template v-slot:item.name="{ item }">
      <slot name="item-name" :item="item"> </slot>
    </template>
    <template v-slot:item.state="{ item }">
      <slot name="item-state" :item="item"> </slot>
    </template>
    <template v-slot:item.actions="{ item }">
      <slot name="item-actions" :item="item"> </slot>
    </template>


    <template v-slot:item.notification_metrix="{ item }">
      <slot name="item-notification_metrix" :item="item"> </slot>
    </template>
  </v-data-table>
</template>

<script>
// Components
import TableColoumnConfig from '@/components/DataTable/TableColoumnConfig.vue'
import BaseButton from '@/components/Button/BaseButton.vue'

// Mixins
import { bus } from '@/main'
import {
  mdiMagnify
} from '@mdi/js'

export default {
  mixins: [],
  components: {
    TableColoumnConfig,
    BaseButton,
  },
  props: {
    options: {
      // store_action_name
    },
    handlerow: { default: true },
    show_select: { default: true },
    show_select_checkbox: { default: false },
    type: { default: null },
    title: { default: null },
    extra_param:{default: '&'},
    end_point: {default: null}
  },
  data() {
    return {
      table_pagination: {},
      headers: [],
      headers_list: [],
      items: [],
      selected: [],
      loader: false,
      temp_query: '',
      search_text: '',
      icons: {
        mdiMagnify
      }
    }
  },
  computed: {
    generate_headers() {
      return this.headers.filter(obj => {
        return obj.is_default
      })
    },
  },
  methods: {
    search() {
      console.log('Search text', this.search_text)
      this.get_list({ view: '&search=' + this.search_text })
    },
    handleClick(items) {
      if (this.handlerow) {
        this.generate_route(items, this.type)
      }
    },
    set_header(header) {
      this.$store.dispatch('Snackbar', {
        bar: true,
        text: 'Order Updated',
      })
      this.headers = header
    },
    get_list(value, temp_query = null) {
      if (temp_query) {
        this.temp_query = temp_query
      }
      this.loader = true
      var query = ''
      if (this.$route.params.pid) {
        query = this.$route.params.pid
      } else if (this.$route.params.pid) {
        query = this.$route.params.pid
      }
      var query_param = '?' + query
      try {
        // Views
        if (value && value.view) {
          query_param += value.view
        }
        console.log(this.temp_query)
        // Views
        if (this.temp_query) {
          query_param += this.temp_query
        }

        // Sort By Query Generation
        if (value && value.sortBy && value.sortBy.length >= 1) {
          for (var [i, v] of value.sortBy.entries()) {
            if (value.sortDesc[i]) {
              query_param += '&ordering=-' + v + '&'
            } else {
              query_param += '&ordering=' + v + '&'
            }
          }
        } else {
          query_param += '&ordering=-submitted_date&'
        }
      } catch (err) {
        console.error(err)
      }

      // Pagination
      try {
        query_param += '&page=' + (value.page ? value.page : 1)
      } catch (_) {}

      //  API Call
      this.$store
        .dispatch(this.options.store_action_name, this.end_point+query_param+this.extra_param)
        .then(data => {
          this.headers = data.data.columns
          this.items = data.data.results
          this.loader = false
        })
        .catch(err => {
          console.error(err)
          this.loader = false
        })
    },
    resourcerequestsuccess(click, response) {
      this.$store.dispatch('Snackbar', {
        bar: true,
        color: status_color(response.status),
        text: 'Resource Request #' + response.data.id + ' Updated ...',
      })
      this.$store.dispatch('CloseDrawer')
    },
  },
  watch: {
    table_pagination: {
      handler(value) {
        this.get_list(value)
      },
    },
    selected(values) {
      this.$emit('item-clicked', values)
    },
  },
}
</script>

<style lang="css" scoped>
.row-pointer >>> tbody tr :hover {
  cursor: pointer;
}
</style>
