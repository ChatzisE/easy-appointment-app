<template>
  <v-card min-width="900" class="mx-auto">
    <v-card-title class="headline" primary-title>Customer Server Logs</v-card-title>
    <v-card-text style="padding-top:0px;">
      <v-container fluid>
        <v-autocomplete
          v-model="selectedCustomerId"
          :items="serverList"
          label="Select Server"
          item-text="NAME"
          item-value="ID"
          chips
          :multiple="false"
          @change="getLogs()"
        ></v-autocomplete>
        <v-simple-table fixed-header height="600px">
          <thead>
            <tr>
              <th class="text-left" style="width:25%;">Date Created</th>
              <th class="text-left" style="width:30%;">User</th>
              <th class="text-left">Applications</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="log in logs" :key="log.ID">
              <td>{{prettyDate(log.DATE_CREATED) }}</td>
              <td>{{ log.FULL_NAME }}</td>
              <td>{{ log.APPLICATIONS }}</td>
            </tr>
          </tbody>
        </v-simple-table>
      </v-container>
    </v-card-text>
  </v-card>
</template>

<script>
import eventBus from "../services/eventBus";
import ajax from "../services/ajaxCall";
import moment from "moment";
export default {
  props: ["applicationList", "serverList"],
  data: () => ({
    customerApplicationsNew: [],
    customer: {},
    selectedCustomerId: "",
    logs: []
  }),
  methods: {
    async getLogs() {
      try {
        if (this.selectedCustomerId) {
          this.logs=[];
          this.logs = await ajax.get("/logs/server", {
            serverId: this.selectedCustomerId
          });
        }
      } catch (e) {
        eventBus.$emit("error", e.response.data);
      }
    },
    prettyDate(date) {
      if (!date) return "";
      return moment(date).format("lll");
    }
  },
  created() {},
  async mounted() {
    // let applications = await this.getCustomerApplicationList(
    //   this.customerDetail.ID
    // );
  },
  computed: {}
};
</script>
