<template>
  <v-tooltip bottom>
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        class="text-capitalize"
        small
        :color="color"
        :icon="icon"
        @click="clickAction"
        v-bind="attrs"
        v-on="on"
        :ripple="false"
        :text="text"
        :outlined="outlined"
        :rounded="rounded"
        :disabled="disabled"
        ><v-icon v-if="mdi_icon" >{{ mdi_icon }}</v-icon> {{ title }}
      </v-btn>
    </template>
    <span>{{ tooltip ? tooltip : title }}</span>
  </v-tooltip>
</template>

<script>
export default {
  props: {
    click: { required: true },
    icon: { default: false },
    title: {
      type: String,
    },
    tooltip: {
      type: String,
    },
    color: {
      type: String,
      default: 'primary',
    },
    mdi_icon: {
      type: String,
    },
    options: {
      type: Object,
    },
    text: {
      default: false,
    },
    disabled: {
      default: false,
    },
    outlined: {
      default: false,
    },
    rounded: {
      default: false,
    },
  },
  watch: {},
  methods: {
    clickAction() {
      // Reset Error Message
      this.$store.dispatch('ResetErrorMessage')
      if (
        this.options &&
        this.options.validate_form &&
        this.options.refs &&
        this.options.refs[this.options.validate_form_name] &&
        this.options.refs[this.options.validate_form_name].validate()
      ) {
        this.$store.dispatch('EnableDrawerLoader')
        this.$store
          .dispatch(this.click, this.options)
          .then(data => {
            this.$emit('success', this.click, data)
            // this.$store.dispatch('CloseDrawer')
            this.$store.dispatch('DisableDrawerLoader')
          })
          .catch(_ => {
            this.$store.dispatch('DisableDrawerLoader')
          })
      } else {
        if (this.options && !this.options.validate_form) {
          console.log('coming', this.click)
          this.$store
            .dispatch(this.click, this.options)
            .then(response => {
              this.$emit('success', this.click, this.options,  response)
              // this.$store.dispatch('CloseDrawer')
                this.$store.dispatch('DisableDrawerLoader')
            })
            .catch(err => {
              console.error(err);
              this.$store.dispatch('DisableDrawerLoader')
            })
        }
      }
    },
  },
}
</script>

<style>
</style>