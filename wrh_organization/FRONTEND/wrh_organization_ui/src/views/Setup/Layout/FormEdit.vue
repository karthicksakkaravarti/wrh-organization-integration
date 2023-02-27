<template>
  <SetupForm :form="$route.params.form"> </SetupForm>
</template>

<script>

import SetupForm from '@/components/Forms/SetupForm.vue'
// import codemirror from '@/components/Codemirror/codemirror.vue'

export default {
  components: {
    SetupForm,
  }
}
</script>
