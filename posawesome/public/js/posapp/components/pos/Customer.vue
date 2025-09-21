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
      :no-data-text="__('Customer not found')"
      hide-details
      :filter="() => true"
      :disabled="readonly"
      :loading="loading"
      :search-input.sync="search"
      append-icon="mdi-plus"
      @click:append="new_customer"
      prepend-inner-icon="mdi-account-edit"
      @click:prepend-inner="edit_customer"
    >
      <!-- legacy Vue 2 slot syntax -->
      <template slot="item" slot-scope="data">
        <v-list-item v-bind="data.attrs" v-on="data.on">
          <v-list-item-content>
            <v-list-item-title
              class="primary--text subtitle-1"
              v-html="data.item.customer_name"
            />
            <v-list-item-subtitle
              v-if="data.item.customer_name !== data.item.name"
              v-html="`ID: ${data.item.name}`"
            />
            <v-list-item-subtitle
              v-if="data.item.tax_id"
              v-html="`TAX ID: ${data.item.tax_id}`"
            />
            <v-list-item-subtitle
              v-if="data.item.email_id"
              v-html="`Email: ${data.item.email_id}`"
            />
            <v-list-item-subtitle
              v-if="data.item.mobile_no"
              v-html="`Mobile No: ${data.item.mobile_no}`"
            />
            <v-list-item-subtitle
              v-if="data.item.primary_address"
              v-html="`Primary Address: ${data.item.primary_address}`"
            />
          </v-list-item-content>
        </v-list-item>
      </template>
    </v-autocomplete>
    <div class="mb-8">
      <UpdateCustomer />
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
  components: { UpdateCustomer },

  data: () => ({
    pos_profile: '',
    customers: [],
    customer: '',           // holds selected customer (name)
    readonly: false,
    customer_info: {},
    search: '',             // v-autocomplete search text
    loading: false,
    _debounceTimer: null,
    _lastQuery: '',         // to avoid duplicate calls for same query
  }),

  methods: {
    // === removed localStorage usage entirely ===

    async fetchCustomers(query) {
      // guard rails
      if (!this.pos_profile || !this.pos_profile.pos_profile) return;
      if (!query || query.trim().length < 2) { // type ≥2 chars to search
        this.customers = [];
        return;
      }
      if (query === this._lastQuery) return;

      this.loading = true;
      this._lastQuery = query;

      frappe.call({
        method: 'posawesome.posawesome.api.posapp.search_customers',
        args: {
          query,
          pos_profile: JSON.stringify(this.pos_profile),
        },
        callback: (r) => {
          this.loading = false;
          this.customers = Array.isArray(r.message) ? r.message : [];
        },
        error: () => {
          this.loading = false;
          this.customers = [];
        },
      });
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
      evntBus.$on('register_pos_profile', (pos_profile) => {
        this.pos_profile = pos_profile;
      });
      evntBus.$on('payments_register_pos_profile', (pos_profile) => {
        this.pos_profile = pos_profile;
      });
      evntBus.$on('set_customer', (customer) => {
        this.customer = customer;
      });
      evntBus.$on('add_customer_to_list', (customer) => {
        // optional: push freshly created customer so it appears immediately
        // when user just added it via dialog
        if (customer && customer.name) {
          const exists = this.customers.some(c => c.name === customer.name);
          if (!exists) this.customers.unshift(customer);
        }
      });
      evntBus.$on('set_customer_readonly', (value) => {
        this.readonly = value;
      });
      evntBus.$on('set_customer_info_to_edit', (data) => {
        this.customer_info = data || {};
      });
      evntBus.$on('fetch_customer_details', () => {
        // no longer preloads; if needed, trigger a search with current text
        this.fetchCustomers(this.search);
      });
    });
  },

  watch: {
    // debounce server search as the user types
    search(val) {
      clearTimeout(this._debounceTimer);
      this._debounceTimer = setTimeout(() => {
        this.fetchCustomers(val);
      }, 250); // tweak delay as desired
    },

    // when selection changes, emit + keep a copy of the selected row for editing
    customer(newVal) {
      const found = this.customers.find(c => c.name === newVal);
      this.customer_info = found || {};
      evntBus.$emit('update_customer', newVal);
    },
  },
};
</script>
