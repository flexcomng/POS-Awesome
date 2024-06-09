<template>
  <div>
    <v-autocomplete
      dense
      clearable
      auto-select-first
      outlined
      color="primary"
      :label="frappe._('Customer')"
      v-model="customer"
      :items="customers"
      item-text="customer_name"
      item-value="name"
      background-color="white"
      :no-data-text="__('Please enter at least 3 characters')"
      hide-details
      :filter="() => true"
      :search-input.sync="searchQuery"
      :loading="loading"
      append-icon="mdi-plus"
      @click:append="new_customer"
      prepend-inner-icon="mdi-account-edit"
      @click:prepend-inner="edit_customer"
      @focus="loadLocalStorageCustomers"
    >
      <template v-slot:item="data">
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title
              class="primary--text subtitle-1"
              v-html="data.item.customer_name"
            ></v-list-item-title>
            <v-list-item-subtitle
              v-if="data.item.customer_name != data.item.name"
              v-html="`ID: ${data.item.name}`"
            ></v-list-item-subtitle>
            <v-list-item-subtitle
              v-if="data.item.tax_id"
              v-html="`TAX ID: ${data.item.tax_id}`"
            ></v-list-item-subtitle>
            <v-list-item-subtitle
              v-if="data.item.email_id"
              v-html="`Email: ${data.item.email_id}`"
            ></v-list-item-subtitle>
            <v-list-item-subtitle
              v-if="data.item.mobile_no"
              v-html="`Mobile No: ${data.item.mobile_no}`"
            ></v-list-item-subtitle>
            <v-list-item-subtitle
              v-if="data.item.primary_address"
              v-html="`Primary Address: ${data.item.primary_address}`"
            ></v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </template>
    </v-autocomplete>
    <div class="mb-8">
      <UpdateCustomer></UpdateCustomer>
    </div>
  </div>
</template>

<script>
import { evntBus } from '../../bus';
import UpdateCustomer from './UpdateCustomer.vue';

export default {
  data: () => ({
    pos_profile: '',
    customers: [],
    customer: '',
    readonly: false,
    customer_info: {},
    searchQuery: '',
    loading: false,
  }),

  components: {
    UpdateCustomer,
  },

  methods: {
    async get_customer_names(searchQuery = '', limit = 100) {
      if (!this.pos_profile || !this.pos_profile.pos_profile) {
        console.error("pos_profile is not set");
        return;
      }
      this.loading = true;

      try {
        const response = await frappe.call({
          method: 'posawesome.posawesome.api.posapp.get_customer_names',
          args: {
            pos_profile: JSON.stringify(this.pos_profile),
            limit,
            search: searchQuery,
          },
        });

        if (response.message) {
          if (searchQuery.length >= 3) {
            this.customers = response.message;
          }
        }
      } catch (error) {
        console.error("Error fetching customer names:", error);
      } finally {
        this.loading = false;
      }
    },

    loadLocalStorageCustomers() {
      this.customers = JSON.parse(localStorage.getItem('customer_storage')) || [];
    },

    searchCustomers(query) {
      this.searchQuery = query;
      const localCustomers = JSON.parse(localStorage.getItem('customer_storage')) || [];
      if (query.length < 3) {
        this.customers = localCustomers;
      } else {
        const filteredCustomers = localCustomers.filter(customer =>
          customer.customer_name.toLowerCase().includes(query.toLowerCase()) ||
          (customer.tax_id && customer.tax_id.toLowerCase().includes(query.toLowerCase())) ||
          (customer.email_id && customer.email_id.toLowerCase().includes(query.toLowerCase())) ||
          (customer.mobile_no && customer.mobile_no.toLowerCase().includes(query.toLowerCase()))
        );

        this.customers = filteredCustomers;
        this.get_customer_names(query);
      }
    },

    onFocus() {
      this.loadLocalStorageCustomers();
    },

    new_customer() {
      evntBus.$emit('open_update_customer', null);
    },

    edit_customer() {
      evntBus.$emit('open_update_customer', this.customer_info);
    },
  },

  created() {
    this.$nextTick(() => {
      this.get_customer_names();
    });

    this.$nextTick(function () {
      evntBus.$on('register_pos_profile', (pos_profile) => {
        this.pos_profile = pos_profile;
        this.get_customer_names();
      });
      evntBus.$on('payments_register_pos_profile', (pos_profile) => {
        this.pos_profile = pos_profile;
        this.get_customer_names();
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
        this.get_customer_names();
      });
    });
  },

  watch: {
    searchQuery(newQuery) {
      this.searchCustomers(newQuery);
    },
  },
};
</script>
