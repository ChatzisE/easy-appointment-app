<template>
  <v-card min-width="600" class="mx-auto">
    <v-card-title class="headline" primary-title>{{customerDetail.NAME}}</v-card-title>
    <v-card-text style="padding-top:0px;">
      <v-container fluid>
        <v-autocomplete
          v-model="customerDetail.RECNO"
          :items="customerList"
          label="Select Customer"
          item-text="SHORT_NAME"
          item-value="RECNO"
          chips
          :multiple="false"
          @change="changeCustomer()"
        ></v-autocomplete>
        <v-text-field
          v-model="customerDetail.NAME"
          label="Customer Name (Optional)"
          :hide-details="true"
        ></v-text-field>
        <v-text-field v-model="customerDetail.IP" label="Server Ip" :hide-details="true"></v-text-field>
        <v-text-field
          v-model="customerDetail.SERVER_PATH"
          label="Server File Path"
          :hide-details="true"
        ></v-text-field>
        <v-text-field
          v-model="customerDetail.CUST_CODE"
          label="Customization Code"
          :hide-details="true"
        ></v-text-field>
        <v-textarea v-model="customerDetail.COMMENTS" label="Comments" :hide-details="true"></v-textarea>
        <!-- <v-select
          v-model="customerApplicationsNew"
          :items="applicationList"
          label="Select Customer Applications"
          multiple
          chips
          item-text="APPLICATION_NAME"
          item-value="APPLICATION_CODE"
          persistent-hint
        ></v-select> -->
      </v-container>
    </v-card-text>
    <v-card-actions>
      <div class="flex-grow-1"></div>
      <v-btn @click="$emit('close')">Close</v-btn>
      <v-btn v-if="customerDetail.ID" color="error" @click="deleteServer()">Delete</v-btn>
      <v-btn color="primary" @click="save()">Save</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import eventBus from "../services/eventBus";
import ajax from "../services/ajaxCall";
export default {
  props: [
    "applicationList",
    "customerDetail",
    "customerApplications",
    "customerList"
  ],
  data: () => ({
    customerApplicationsNew: [],
    customer: {}
  }),
  methods: {
    async save() {
      try {
        await ajax.post("/server", {
          customerServer: this.customerDetail,
          customerApplications: this.customerApplicationsNew
        });
        this.$emit("close");
      } catch (e) {
        eventBus.$emit("error", e.response.data);
      }
    },
    async deleteServer() {
      try {
        await ajax.delete("/server", {
          customerServer: this.customerDetail
        });
        this.$emit("delete");
      } catch (e) {
        eventBus.$emit("error", e.response.data);
      }
    },
    changeCustomer() {
      const customer = this.customerList.filter(customer => {
        return customer.RECNO === this.customerDetail.RECNO;
      });
      if (customer.length) {
        this.customerDetail.NAME = customer[0].SHORT_NAME;
      }
    }
  },
  created() {
    this.customerApplicationsNew = this.customerApplications.map(item => {
      return item.APPLICATION_CODE;
    }); // Object.assign(this.customerApplicationsNew,this.customerApplications)
  },
  async mounted() {
    // let applications = await this.getCustomerApplicationList(
    //   this.customerDetail.ID
    // );
  },
  computed: {}
};
</script>
