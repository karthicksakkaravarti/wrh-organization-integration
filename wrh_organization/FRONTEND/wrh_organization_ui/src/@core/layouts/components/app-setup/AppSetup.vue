<template>
  <div class="app-setup">
    <v-btn icon to="/setup" small>
      <v-icon size="25">
        {{ icons.mdiHammerScrewdriver }}
      </v-icon>
    </v-btn>

  </div>
</template>

<script>

import { PerfectScrollbar } from 'vue2-perfect-scrollbar'
import { mdiCog, mdiClose, mdiHammerScrewdriver } from '@mdi/js'


// 3rd Party

export default {
  components: {
    PerfectScrollbar,
  },
  setup() {
    return {
      icons: {
        mdiHammerScrewdriver,
      },
    }
  }

}
</script>

