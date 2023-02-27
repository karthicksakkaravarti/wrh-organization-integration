import { mapGetters, mapActions  } from 'vuex'

export const Setup = {
  computed: {
    ...mapGetters('SetupStore', ['ActionLoader', 'authentication']),
  },
  methods: {
    ...mapActions('SetupStore', ['SETUP_API_APPBASIC_POST', 'SETUP_API_APPBASIC_GET','SETUP_API_FORMMODEL_GET', 'SETUP_API_FORMMODEL_POST'])
  }
}
