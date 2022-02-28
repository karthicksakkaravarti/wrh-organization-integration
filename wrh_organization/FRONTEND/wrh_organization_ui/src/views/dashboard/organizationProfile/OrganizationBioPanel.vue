<template>
  <v-row class="member-profile-bio-panel">
    <!-- user profile -->
    <v-col cols="12">
      <v-card class="pt-10">
        <v-btn small text color="info" class="position-absolute back-org-btn" :to="{name: $rns.DASHBOARD_MEMBER_PROFILE, params: {tab: 1}}">
          <v-icon>{{icons.mdiKeyboardBackspace}}</v-icon>Organization List
        </v-btn>
        <v-card-title class="justify-center flex-column">
          <v-avatar
            :color="organization.logo ? '' : 'primary'"
            :class="organization.logo ? '' : 'v-avatar-light-bg primary--text'"
            size="120"
            rounded
            class="mb-4"
          >
            <v-img v-if="organization.logo" :src="organization.logo"></v-img>
            <span v-else class="font-weight-semibold text-5xl">{{ avatarText(organization.name) }}</span>
          </v-avatar>

          <span class="mb-2">{{ organization.name }}</span>

          <v-chip
            label
            small
            :color="($const.ORGANIZATION_TYPE_MAP[organization.type] || {}).css"
            :class="`v-chip-light-bg text-sm font-weight-semibold ${($const.ORGANIZATION_TYPE_MAP[organization.type] || {}).css}--text text-capitalize`"
          >
            {{($const.ORGANIZATION_TYPE_MAP[organization.type] || {}).title || organization.type}}
          </v-chip>
        </v-card-title>

        <v-card-text class="d-flex justify-center flex-wrap mt-2 pe-sm-0">
          <div class="d-flex align-center me-8 mb-4">
            <v-avatar
              size="40"
              rounded
              color="primary"
              class="v-avatar-light-bg primary--text me-3"
            >
              <v-icon
                color="primary"
                size="22"
              >
                {{ icons.mdiAccountMultipleOutline }}
              </v-icon>
            </v-avatar>

            <div>
              <h3 class="text-xl font-weight-medium mb-n1">
                {{ kFormatter(242) }}
              </h3>
              <span>Members</span>
            </div>
          </div>

          <div class="d-flex align-center mb-4 me-4">
            <v-avatar
              size="40"
              rounded
              color="primary"
              class="v-avatar-light-bg primary--text me-3"
            >
              <v-icon
                color="primary"
                size="22"
              >
                {{ icons.mdiCalendar }}
              </v-icon>
            </v-avatar>

            <div>
              <h3 class="text-xl font-weight-medium mb-n1">
                {{ kFormatter(12) }}
              </h3>
              <span>Events</span>
            </div>
          </div>
        </v-card-text>

        <v-card-text>
          <h2 class="text-xl font-weight-semibold mb-2">
            Details
          </h2>

          <v-divider></v-divider>

          <v-list>
            <v-list-item dense class="px-0 mb-n2">
              <span class="font-weight-medium me-2">About:</span>
              <span class="text--secondary">{{ organization.about || '-' }}</span>
            </v-list-item>

            <v-list-item dense class="px-0 mb-n2">
              <span class="font-weight-medium text-no-wrap me-2">Website:</span>
              <span class="text--secondary">{{ organization.website || '-' }}</span>
            </v-list-item>

            <v-list-item dense class="px-0 mb-n2">
              <span class="font-weight-medium me-2">E-mail:</span>
              <span class="text--secondary">{{ organization.email || '-' }}</span>
            </v-list-item>

            <v-list-item dense class="px-0 mb-n2">
              <span class="font-weight-medium me-2">Phone:</span>
              <span class="text--secondary">{{ organization.phone? $utils.formatPhone(organization.phone): '-' }}</span>
            </v-list-item>

            <v-list-item dense class="px-0 mb-n2">
              <span class="font-weight-medium text-no-wrap me-2">Instagram:</span>
              <span class="text--secondary">-</span>
            </v-list-item>

            <v-list-item dense class="px-0 mb-n2">
              <span class="font-weight-medium text-no-wrap me-2">Youtube:</span>
              <span class="text--secondary">-</span>
            </v-list-item>

            <v-list-item dense class="px-0 mb-n2">
              <span class="font-weight-medium me-2">Country:</span>
              <span class="text--secondary">{{($const.COUNTRY_MAP[organization.country] || {}).name || organization.country || '-'}}</span>
            </v-list-item>

            <v-list-item dense class="px-0 mb-n2">
              <span class="font-weight-medium me-2">State:</span>
              <span class="text--secondary">{{ organization.state || '-' }}</span>
            </v-list-item>

            <v-list-item dense class="px-0 mb-n2">
              <span class="font-weight-medium me-2">City:</span>
              <span class="text--secondary">{{ organization.city || '-' }}</span>
            </v-list-item>

            <v-list-item dense class="px-0 mb-n2">
              <span class="font-weight-medium me-2">Address:</span>
              <span class="text--secondary">{{ organization.address || '-' }}</span>
            </v-list-item>

          </v-list>
        </v-card-text>

        <v-card-actions class="justify-center">
          <v-btn color="warning" outlined class="me-3" @click="$emit('edit-click')">
            <v-icon dark left>
              {{ icons.mdiHomeEditOutline }}
            </v-icon>Edit
          </v-btn>
        </v-card-actions>
      </v-card>

    </v-col>
  </v-row>
</template>

<script>
import {
  mdiAccountMultipleOutline,
  mdiCalendar,
  mdiCheckboxBlankCircle,
  mdiHomeEditOutline,
  mdiKeyboardBackspace
} from '@mdi/js';
import { avatarText, kFormatter } from '@core/utils/filter';

export default {
  components: {
  },
  props: {
    organization: {
      type: Object,
      required: true
    }
  },
  setup() {
    return {
      avatarText,
      kFormatter,
      icons: {
        mdiAccountMultipleOutline,
        mdiCalendar,
        mdiCheckboxBlankCircle,
        mdiHomeEditOutline,
        mdiKeyboardBackspace,
      },
    }
  },
}
</script>
<style lang="scss">
.member-profile-bio-panel {
  .back-org-btn {
    top: 3px;
    left: 2px;
  }
}
</style>