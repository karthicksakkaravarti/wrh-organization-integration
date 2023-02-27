<template>
  <div>
    <v-text-field
      color="primary"
      :prefix="prefix"
      hide-details="auto"
      :error-messages="error_message"
      :hint="hint"
      :autofocus="autofocus"
      :type="type"
      :rules="rules"
      :disabled="disabled"
      :readonly="readonly"
      :prepend-icon="prependicon"
      :append-icon="appendicon"
      :prepend-inner-icon="prependinnericon"
      :append-outer-icon="appendoutericon"
      :outlined="outlined"
      v-model="field.value"
      dense
    >
      <template v-slot:label> {{ label }} <span style="color: red" v-if="field && field.required">*</span> </template>
    </v-text-field>
  </div>
</template>

<script>
import { Rules } from '@/mixins/Rules'

export default {
  mixins: [Rules],
  props: {
    label: { required: true, type: String },
    field: { default: {} },
    prependicon: { default: '' },
    appendicon: { default: '' },
    error_message: { default: null },
    prependinnericon: { default: '' },
    appendoutericon: { default: '' },
    disabled: { default: false },
    readonly: { default: false },
    type: { default: 'String' },
    prefix: { default: null },
    value: { default: '' },
    autofocus: { default: false },
    hint: { default: '' },
    outlined: { default: false },
  },

  methods: {},
}
</script>

<style>
</style>