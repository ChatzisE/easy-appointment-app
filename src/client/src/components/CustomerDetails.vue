<template>
  <v-card min-width="600" class="mx-auto">
    <v-toolbar color="blue" dark>
      <v-btn icon @click="$emit('close')" v-if="!progressIntervalId">
        <v-icon>mdi-arrow-left</v-icon>
      </v-btn>
      <v-avatar :color="'white'" :tile="false" :size="40" style="color:#2196F3;margin-right:10px;">
        <span>{{customerDetail.CUST_CODE}}</span>
      </v-avatar>
      <v-toolbar-title>{{customerDetail.NAME}}</v-toolbar-title>
      <div class="flex-grow-1"></div>
      <v-btn icon @click="dialogEdit=true">
        <v-icon>mdi-playlist-edit</v-icon>
      </v-btn>
    </v-toolbar>
    <v-card-text style="padding-top:0px;">
      <v-container fluid>
        <div style="position:relative;">
          <v-progress-linear
            style="position:absolute;top:0;"
            v-if="progressIntervalId"
            v-model="progreesBarPercentage"
            height="25"
            reactive
          >
            <strong style="color:white;">{{progreesBarPercentage}}%</strong>
          </v-progress-linear>
        </div>
        <div style="    text-align: right;margin-top:30px">
          <v-btn
            @click="zipbundle()"
            :disabled="!bundleBtnEnabled"
            :color="'primary'"
            :elevation="4"
          >
            <span>Download Bundle</span>
          </v-btn>
        </div>
        <v-checkbox v-model="allFlag" :label="'All'"></v-checkbox>
        <div v-if="!allFlag">
          <p class="font-weight-black">Select individual applications to bundle</p>
          <!-- <p>{{ selectedApplications }}</p> -->
          <v-checkbox
            v-model="selectedApplications"
            v-for="application in customerApplications"
            :key="application.APPLICATION_CODE"
            :label="displayApplicationName(application.APPLICATION_CODE)"
            :value="application.APPLICATION_CODE"
          ></v-checkbox>
        </div>
      </v-container>
    </v-card-text>
    <v-dialog v-model="dialog" width="500">
      <v-card>
        <v-card-title class="headline red" style="color:white;" primary-title>Error</v-card-title>
        <v-card-text v-if="progress.error">{{JSON.stringify(progress.error)}}}</v-card-text>
      </v-card>
    </v-dialog>
    <v-dialog v-model="dialogEdit" persistent max-width="800">
      <CustomerDetailsEdit
        v-if="dialogEdit"
        :applicationList="applicationList"
        :customerDetail="customerDetail"
        :customerApplications="customerApplications"
        :customerList="customerList"
        @close="closeEditDialog"
        @delete="deleteEditDialog"
      ></CustomerDetailsEdit>
    </v-dialog>
  </v-card>
</template>

<script>
import eventBus from "../services/eventBus";
import ajax from "../services/ajaxCall";
import CustomerDetailsEdit from "./CustomerDetailsEdit";
export default {
  props: ["applicationList", "customerDetail", "customerList"],
  data: () => ({
    frameworkApps: ["AM", "ADR", "VSL", "STY", "DBA"],
    customerApplications: [],
    selectedApplications: [],
    allFlag: false,
    progressIntervalId: "",
    zipbundleName: "",
    progress: {},
    pendingCall: false,
    dialog: false,
    dialogEdit: false
  }),
  methods: {
    async getCustomerApplicationList(custId) {
      try {
        return await ajax.get("/application/customer", {
          custId: custId
        });
      } catch (e) {
        eventBus.$emit("error", e.response.data);
      }
    },
    async zipbundle() {
      try {
        let args = {
          customizationCode: this.customerDetail.CUST_CODE,
          applications: this.selectedApplications,
          allFlag: this.allFlag,
          projectPath: this.customerDetail.SERVER_PATH
        };
        this.zipbundleName = await ajax.post("/zipbundle", args);
        await this.insertLog(this.selectedApplications);
        this.progress.processed = 0;
        this.progress.total = 100;
        this.progressIntervalId = setInterval(this.getProgress, 1000);
        return;
      } catch (e) {
        eventBus.$emit("error", e.response.data);
      }
    },
    async insertLog(applications) {
      try {
        let applicationsString = "";
        if (this.allFlag) {
          applicationsString = "All";
        } else {
          for (let app of applications) {
            applicationsString += app+',';
          }
          applicationsString=applicationsString.substring(0,applicationsString.length-2);
        }
        const log = {
          SERVER_ID: this.customerDetail.ID,
          APPLICATIONS: applicationsString
        };
        await ajax.post("/logs",{ log:log});
      } catch (e) {
        eventBus.$emit("error", e.response.data);
      }
    },
    downloadFilePromt(href, name) {
      let a = document.createElement("a");
      document.body.appendChild(a);
      a.download = name;
      a.href = href;
      a.click();
      a.parentNode.removeChild(a);
    },
    async getProgress() {
      try {
        if (this.pendingCall) return;
        let args = {
          filename: this.zipbundleName
        };
        this.pendingCall = true;
        this.progress = await ajax.get("/zipbundle/progress", args);
        this.pendingCall = false;
        if (this.progress.error) {
          this.dialog = true;
          clearInterval(this.progressIntervalId);
          return;
        }
        if (
          this.progress.processed === this.progress.total &&
          this.progress.finished
        ) {
          clearInterval(this.progressIntervalId);
          this.progressIntervalId = "";
          this.downloadFilePromt(
            "zipBundles/" + this.zipbundleName,
            this.zipbundleName
          );
        }
        return;
      } catch (e) {
        eventBus.$emit("error", e.response.data);
        clearInterval(this.progressIntervalId);
      }
    },
    displayApplicationName(applicationCode) {
      if (applicationCode) {
        const application = this.applicationList.filter(item => {
          return item.APPLICATION_CODE === applicationCode;
        });
        if (application.length) {
          return application[0].APPLICATION_NAME +' ( '+applicationCode+' )';
        }
      }
      return '( '+applicationCode+' )';
    },
    closeEditDialog() {
      this.dialogEdit = false;
      this.init();
    },
    deleteEditDialog() {
      this.dialogEdit = false;
      this.$emit("refresh-server-list");
    },
    async init() {
      try {
        let applications = await this.getCustomerApplicationList(
          this.customerDetail.RECNO
        );
        this.frameworkApps.forEach(element => {
          if (
            applications.filter(_item => {
              return _item.APPLICATION_CODE === element;
            }).length === 0
          )
            applications.push({
              APPLICATION_CODE: element
            });
        });
        applications = applications.sort(function(a, b) {
          return a.APPLICATION_CODE > b.APPLICATION_CODE ? 1 : -1;
        });
        this.customerApplications = applications;
      } catch (e) {
        eventBus.$emit("error", e.response.data);
      }
    }
  },
  async mounted() {
    this.init();
  },
  computed: {
    bundleBtnEnabled() {
      return this.allFlag === true || this.selectedApplications.length > 0;
    },
    progreesBarPercentage() {
      let progress = Math.floor(
        (this.progress.processed * 100) / this.progress.total,
        1
      );
      if (isNaN(progress)) {
        return 0;
      } else {
        return progress;
      }
    }
  },
  components: {
    CustomerDetailsEdit
  }
};
</script>
