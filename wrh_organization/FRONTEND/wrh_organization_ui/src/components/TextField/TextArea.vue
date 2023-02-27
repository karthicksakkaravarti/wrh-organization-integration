<template>
  <v-textarea
    color="primary"
    :label="`${label} ${field.required ? '*' : ''}`"
    :rules="rules"
    :rows="rows"
    auto-grow
    :row-height="rowheight"
    v-model="field.value"
    dense
    hide-details="auto"
    :prepend-icon="prependicon"
    :append-icon="appendicon"
    :prepend-inner-icon="prependinnericon"
    :append-outer-icon="appendoutericon"
    :outlined="outlined"
  >
    <template v-slot:label> {{ label }} <span style="color: red" v-if="field && field.required">*</span> </template>
  </v-textarea>
</template>

<script>
import { Rules } from '@/mixins/Rules'

export default {
  mixins: [Rules],
  props: {
    label: { required: true, type: String },
    field: { default: {} },
    rows: { default: 5 },
    rowheight: { default: 20 },
    prependicon: { default: '' },
    appendicon: { default: '' },
    prependinnericon: { default: '' },
    appendoutericon: { default: '' },
    outlined: { default: false },
  },
  methods: {},
}
</script>

<style>
</style>