<template>
  <v-card min-width="600" class="mx-auto">
    <v-toolbar color="blue" dark>
      <v-text-field
        v-model="filterText"
        label="Search Companies"
        clearable
        :hide-details="true"
        :append-icon="'mdi-magnify'"
      ></v-text-field>
    </v-toolbar>
    <v-list two-line dense>
      <v-list-item-group color="primary">
        <v-list-item 
          v-for="(item, index) in serverListFiltered"
          :key="item.ID"
          color="primary"
          :nav="true"
          @click="$emit('select-customer',item)"
        >
          <v-list-item-avatar>
            <v-avatar :color="'teal'" :tile="false" :size="40" style="color:white;">
              <span>{{item.CUST_CODE}}</span>
            </v-avatar>
          </v-list-item-avatar>
          <v-list-item-content>
            <v-list-item-title>
              <a style="font-size:17px;" target="#">{{item.NAME}}</a>
            </v-list-item-title>
            <v-list-item-subtitle style="white-space: pre;">{{item.COMMENTS}}</v-list-item-subtitle>
          </v-list-item-content>
          <v-btn icon  @click="openIpLink(item,$event)">
            <v-icon large color="default">mdi-link-variant</v-icon>
          </v-btn>
          <!-- <v-btn icon>
            <v-icon x-large dark color="primary">mdi-arrow-right-drop-circle</v-icon>
          </v-btn> -->
        </v-list-item>
      </v-list-item-group>
    </v-list>
    <v-dialog v-model="dialogEdit" persistent max-width="800">
      <CustomerDetailsEdit
        v-if="dialogEdit"
        :applicationList="applicationList"
        :customerDetail="customerDetail"
        :customerApplications="[]"
        :customerList="customerList"
        @close="closeEditDialog"
        @delete="refreshServerList"
      ></CustomerDetailsEdit>
    </v-dialog>
    <v-btn
      style="position:fixed;right:100px; bottom:20px"
      @click="addCustomer()"
      color="error"
      fab
      dark
    >
      <v-icon>mdi-plus</v-icon>
    </v-btn>
  </v-card>
</template>

<script>
import CustomerDetailsEdit from "./CustomerDetailsEdit";
export default {
  props: ["serverList", "applicationList", "customerList"],
  data: () => ({
    filterText: "",
    dialogEdit: false,
    customerDetail: {}
  }),
  methods: {
    openIpLink(item, event) {
      window.open(item.IP, "_blank");
      event.preventDefault();
      event.stopPropagation();
    },
    closeEditDialog() {
      this.dialogEdit = false;
      this.$emit("refresh-server-list");
    },
    async addCustomer() {
      this.customerDetail = JSON.parse(
        JSON.stringify({
          ID: null,
          RECNO: null,
          NAME: "",
          IP: "",
          SERVER_PATH: "",
          CUST_CODE: "ST",
          COMMENTS: ""
        })
      );
      this.dialogEdit = true;
    },
    refreshServerList() {
      this.dialogEdit = false;
      this.$emit("refresh-server-list");
    }
  },
  computed: {
    serverListFiltered() {
      if (!this.filterText) {
        return this.serverList;
      } else {
        const _filterText = this.filterText.toUpperCase();
        return this.serverList.filter(item => {
          return (
            (item.NAME && item.NAME.toUpperCase().indexOf(_filterText) > -1) ||
            (item.CUST_CODE &&
              item.CUST_CODE.toUpperCase().indexOf(_filterText) > -1)
          );
        });
      }
    }
  },
  components: {
    CustomerDetailsEdit
  }
};
</script>
