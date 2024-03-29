<template>
  <div class="organization-events-tab">
    <v-card>
      <v-tabs v-model="tab" grow>
        <v-tab @change="tableWidgetRef && tableWidgetRef.loadRecords()"><v-icon>{{ icons.mdiTable }}</v-icon> Events Table</v-tab>
        <v-tab @change="calendarWidgetRef && calendarWidgetRef.refreshCalendar()"><v-icon>{{ icons.mdiCalendar }}</v-icon> Events Calendar</v-tab>
      </v-tabs>
      <v-tabs-items v-model="tab">
        <v-tab-item>
          <events-table-widget ref="tableWidgetRef" :event-list-url="`cycling_org/organization/${organization.id}/event/`" show-actions
                               :organization="organization"
                               @add-action-clicked="$refs.eventFormDialogRef.show()"
                               @shared-orgs-action-clicked="(item) => $refs.eventSharedOrgsDialogRef.show(item)"
                               @edit-action-clicked="(item) => $refs.eventFormDialogRef.show(item)">
          </events-table-widget>
        </v-tab-item>
        <v-tab-item>
          <events-calendar-widget ref="calendarWidgetRef" :event-list-url="`cycling_org/organization/${organization.id}/event/`" :edit-mode="true"
                                  @nav-link-day-clicked="(date) => $refs.eventFormDialogRef.show({start_date: $utils.formatDate(date, 'YYYY-MM-DD')})"
                                  @event-clicked="(item) => $refs.eventFormDialogRef.show(item)">

          </events-calendar-widget>
        </v-tab-item>
      </v-tabs-items>
    </v-card>
    <organization-event-form-dialog ref="eventFormDialogRef" :organization="organization"
                                    @delete-successed="refreshCurrentTab()"
                                    @save-successed="refreshCurrentTab()"></organization-event-form-dialog>
    <event-shared-orgs-dialog ref="eventSharedOrgsDialogRef" :organization="organization"
                              @save-successed="refreshCurrentTab()"></event-shared-orgs-dialog>
  </div>
</template>

<script>
import {
  mdiCalendar,
  mdiTable,
  mdiShareVariant,
} from '@mdi/js'
import EventsCalendarWidget from "@/views/public/EventsCalendarWidget";
import EventsTableWidget from "@/views/public/EventsTableWidget";
import {onMounted, ref} from "@vue/composition-api";
import {useRouter} from "@core/utils";
import OrganizationEventFormDialog from "@/views/dashboard/organizationProfile/OrganizationEventFormDialog";
import EventSharedOrgsDialog from "@/views/dashboard/organizationProfile/EventSharedOrgsDialog.vue";
export default {
  components: {EventSharedOrgsDialog, OrganizationEventFormDialog, EventsTableWidget, EventsCalendarWidget},
  props: {
    organization: {
      type: Object,
      required: true
    }
  },
  setup(props, context) {
    const { route } = useRouter();
    const tab = ref(null);
    const tableWidgetRef = ref(null);
    const calendarWidgetRef = ref(null);

    onMounted(() => {
      var tabNumber = route.value.params.tab;
      if (tabNumber === undefined) {
        tabNumber = route.value.query.tab || undefined;
      }
      tab.value = tabNumber !== undefined? tabNumber * 1: 0 ;
    });

    const refreshCurrentTab = () => {
      if (tab.value === 0 && tableWidgetRef.value) {
        tableWidgetRef.value.loadRecords();
      }
      else if (tab.value === 1 && calendarWidgetRef.value) {
        calendarWidgetRef.value.refreshCalendar();
      }
    };

    return {
      tab,
      tableWidgetRef,
      refreshCurrentTab,
      calendarWidgetRef,
      icons: {
        mdiCalendar,
        mdiTable,
        mdiShareVariant,
      }
    }
  }
}
</script>
