<template>
  <v-card min-width="600" class="mx-auto">
    <v-card-title class="headline" primary-title>Login</v-card-title>
    <v-card-text style="padding-top:0px;">
      <v-container fluid>
        <v-text-field v-model="username" @keydown="keyDown" label="Username" :hide-details="true"></v-text-field>
        <v-text-field
          v-model="password"
          @keydown="keyDown"
          label="Password"
          :type="'password'"
          :hide-details="true"
        ></v-text-field>
      </v-container>
    </v-card-text>
    <v-card-actions>
      <div class="flex-grow-1"></div>
      <v-btn color="primary" primary @click="login()">Login</v-btn>
    </v-card-actions>
    <v-snackbar v-model="errorDialog" :color="'error'" :timeout="5000" :vertical="false">
      <span v-html="errorMessage"></span>
      <v-btn dark @click="errorDialog = false" style="float: right;">Close</v-btn>
    </v-snackbar>
  </v-card>
</template>

<script>
import ajax from "../services/ajaxCall";
export default {
  props: [
    "applicationList",
    "customerDetail",
    "customerApplications",
    "customerList"
  ],
  data: () => ({
    username: "",
    password: "",
    errorDialog: false,
    errorMessage: ""
  }),
  methods: {
    keyDown(event) {
      if (event.keyCode === 13) {
        this.login();
      }
    },
    async login() {
      try {
        this.customerList = await ajax.post("/login", {
          user: this.username,
          password: this.password
        });
        location.reload();
      } catch (e) {
        this.errorDialog = true;
        this.errorMessage = e.response.data;
      }
    }
  },
  created() {},
  async mounted() {},
  computed: {}
};
</script>
