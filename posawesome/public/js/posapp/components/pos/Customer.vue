<template>
  <div>
    <v-menu
      v-model="menu"
      :close-on-content-click="false"
      :nudge-width="0"
      offset-y
      :max-height="200"
      transition="scale-transition"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-text-field
          dense
          clearable
          outlined
          color="primary"
          v-model="searchQuery"
          label="Search Customer"
          v-bind="attrs"
          v-on="on"
          @keyup.enter="search_customers"
          hide-details
          prepend-inner-icon="mdi-account-edit"
          @click:prepend-inner="open_edit_customer"
          @focus="menu = true"
        >
          <template v-slot:append>
            <v-icon
              class="mr-2"
              @click="search_customers"
            >mdi-magnify</v-icon>
            <v-icon
              @click="new_customer"
            >mdi-plus</v-icon>
          </template>
        </v-text-field>
      </template>
      <v-list v-if="customers.length" dense>
        <v-list-item
          v-for="(customer, index) in customers"
          :key="index"
          @click="select_customer(customer)"
        >
          <v-list-item-content>
            <v-list-item-title
              class="primary--text subtitle-1"
              v-html="customer.customer_name"
            ></v-list-item-title>
            <v-list-item-subtitle
              v-if="customer.customer_name != customer.name"
              v-html="`ID: ${customer.name}`"
            ></v-list-item-subtitle>
            <v-list-item-subtitle v-if="customer.tax_id"
              v-html="`TAX ID: ${customer.tax_id}`"
            ></v-list-item-subtitle>
            <v-list-item-subtitle v-if="customer.email_id"
              v-html="`Email: ${customer.email_id}`"
            ></v-list-item-subtitle>
            <v-list-item-subtitle v-if="customer.mobile_no"
              v-html="`Mobile No: ${customer.mobile_no}`"
            ></v-list-item-subtitle>
            <v-list-item-subtitle v-if="customer.primary_address"
              v-html="`Primary Address: ${customer.primary_address}`"
            ></v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-menu>
    <div class="mb-8">
      <UpdateCustomer></UpdateCustomer>
    </div>
  </div>
</template>

<style scoped>
.v-menu__content {
  max-height: 500px !important;
  overflow-y: auto !important;
}
</style>

<script>
import { evntBus } from '../../bus';
import UpdateCustomer from './UpdateCustomer.vue';

export default {
  data: () => ({
    pos_profile: '',
    customers: [],
    customer: '',
    searchQuery: '',
    readonly: false,
    customer_info: {},
    menu: false,
  }),

  components: {
    UpdateCustomer,
  },

  methods: {
    search_customers(event) {
      event.stopPropagation();
      if (this.searchQuery.length < 3) {
        console.warn("Please enter at least 3 characters to search.");
        return;
      }
      console.log("Searching customers with query:", this.searchQuery);
      const vm = this;
      frappe.call({
        method: 'posawesome.posawesome.api.posapp.search_customers',
        args: {
          query: this.searchQuery,
          pos_profile: this.pos_profile.pos_profile,
        },
        callback: function (r) {
          if (r.message) {
            vm.customers = r.message;
            vm.menu = true; // Open the menu when search results are available
            console.log("Search results:", vm.customers);
          }
        },
      });
    },
    select_customer(customer) {
      this.customer = customer.name;
      this.searchQuery = customer.customer_name;
      this.customers = [];
      this.menu = false; // Close the menu on selection
      this.fetch_customer_details(customer.name);
    },
    fetch_customer_details(customer_id) {
      if (!customer_id) {
        console.error("Customer ID is undefined");
        return;
      }
      const vm = this;
      frappe.call({
        method: 'posawesome.posawesome.api.posapp.get_customer_details',
        args: {
          customer_id: customer_id,
        },
        callback: function (r) {
          if (r.message) {
            vm.customer_info = r.message;
          }
        },
      });
    },
    new_customer() {
      evntBus.$emit('open_update_customer', null);
    },
    handleEditIconClick(event) {
      event.stopPropagation();
      this.open_edit_customer();
    },
    open_edit_customer() {
      evntBus.$emit('open_update_customer', this.customer_info);
    },
  },

  created: function () {
    this.$nextTick(function () {
      evntBus.$on('register_pos_profile', (pos_profile) => {
        this.pos_profile = pos_profile;
        console.log("Registered POS profile:", pos_profile);
      });
      evntBus.$on('payments_register_pos_profile', (pos_profile) => {
        this.pos_profile = pos_profile;
      });
      evntBus.$on('set_customer', (customer) => {
        this.customer = customer;
      });
      evntBus.$on('add_customer_to_list', (customer) => {
        this.customers.push(customer);
      });
      evntBus.$on('set_customer_readonly', (value) => {
        this.readonly = value;
      });
      evntBus.$on('set_customer_info_to_edit', (data) => {
        this.customer_info = data;
      });
      evntBus.$on('fetch_customer_details', () => {
      });
    });
  },

  watch: {
    customer(newVal) {
      evntBus.$emit('update_customer', this.customer);
    },
  },
};
</script>
