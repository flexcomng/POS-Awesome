<template>
  <nav>
    <v-app-bar app height="40" class="elevation-2">
      <v-app-bar-nav-icon
        @click.stop="drawer = !drawer"
        class="grey--text"
      ></v-app-bar-nav-icon>
      <v-img
        src="/assets/posawesome/js/posapp/components/pos/pos.png"
        alt="POS Awesome"
        max-width="32"
        class="mr-2"
        color="primary"
      ></v-img>
      <v-toolbar-title
        @click="go_desk"
        style="cursor: pointer"
        class="text-uppercase primary--text"
      >
        <span class="font-weight-light">pos</span>
        <span>awesome</span>
      </v-toolbar-title>

      <v-spacer></v-spacer>
      <v-btn style="cursor: unset" text color="primary">
        <span right>User: {{ user_full_name }}</span>
        </v-btn>
        <v-btn style="cursor: unset" text color="primary">
        <span right>POS Profile: {{ pos_profile.name }}</span>
      </v-btn>
      <div class="text-center">
        <v-menu offset-y>
          <template v-slot:activator="{ on, attrs }">
            <v-btn color="primary" dark text v-bind="attrs" v-on="on"
              >Menu</v-btn
            >
          </template>
          <v-card class="mx-auto" max-width="300" tile>
            <v-list dense>
              <v-list-item-group v-model="menu_item" color="primary">
                <v-list-item
                  @click="close_shift_dialog"
                  v-if="!pos_profile.posa_hide_closing_shift && item == 0"
                >
                  <v-list-item-icon>
                    <v-icon>mdi-content-save-move-outline</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title>{{
                      __('Close Shift')
                    }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item
                  @click="print_last_invoice"
                  v-if="
                    pos_profile.posa_allow_print_last_invoice &&
                    this.last_invoice
                  "
                >
                  <v-list-item-icon>
                    <v-icon>mdi-printer</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title>{{
                      __('Print Last Invoice')
                    }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-divider class="my-0"></v-divider>
                <v-list-item @click="logOut">
                  <v-list-item-icon>
                    <v-icon>mdi-logout</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title>{{ __('Logout') }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item @click="go_about">
                  <v-list-item-icon>
                    <v-icon>mdi-information-outline</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title>{{ __('About') }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list-item-group>
            </v-list>
          </v-card>
        </v-menu>
      </div>
    </v-app-bar>
    <v-navigation-drawer
      v-model="drawer"
      :mini-variant.sync="mini"
      app
      class="primary margen-top"
      width="190"
    >
      <v-list dark>
        <v-list-item class="px-2">
          <v-list-item-avatar>
            <v-img :src="company_img"></v-img>
          </v-list-item-avatar>

          <v-list-item-title>{{ company }}</v-list-item-title>

          <v-btn icon @click.stop="mini = !mini">
            <v-icon>mdi-chevron-left</v-icon>
          </v-btn>
        </v-list-item>
        <!-- <MyPopup/> -->
        <!-- POS and Update Price List Buttons -->
        <v-list-item-group v-model="item" color="white">
          <!-- Iterate through existing items (POS) -->
          <v-list-item
            v-for="item in items"
            :key="item.text"
            @click="changePage(item.text)"
          >
            <v-list-item-icon>
              <v-icon v-text="item.icon"></v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title v-text="item.text"></v-list-item-title>
            </v-list-item-content>
          </v-list-item>

          <!-- Iterate through positems (Update Price List) -->
          <v-list-item
            v-for="positem in positems"
            :key="positem.text"
            @click="startPriceUpdate"
          >
            <v-list-item-icon>
              <v-icon v-text="positem.icon"></v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title v-text="positem.text"></v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item
            v-for="positem in positem2"
            :key="positem.text"
            @click="startStockUpdate"
          >
            <v-list-item-icon>
              <v-icon v-text="positem.icon"></v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title v-text="positem.text"></v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item
            v-for="positem in positem3"
            :key="positem.text"
            @click="startSalesUpdate"
          >
            <v-list-item-icon>
              <v-icon v-text="positem.icon"></v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title v-text="positem.text"></v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>
    <v-snackbar v-model="snack" :timeout="5000" :color="snackColor" top right>
      {{ snackText }}
    </v-snackbar>
    <v-dialog v-model="freeze" persistent max-width="290">
      <v-card>
        <v-card-title class="text-h5">
          {{ freezeTitle }}
        </v-card-title>
        <v-card-text>{{ freezeMsg }}</v-card-text>
      </v-card>
    </v-dialog>
  </nav>
</template>


<script>
import { evntBus } from '../bus';

export default {
  // components: {MyPopup},
  data() {
    return {
      drawer: false,
      mini: true,
      item: 0,
      items: [{ text: 'POS', icon: 'mdi-network-pos' }],
      positems: [{ text: 'Price Update', icon: 'mdi-cash' }],
      positem2: [{ text: 'Stock Update', icon: 'mdi-database-arrow-up' }],
      positem3: [{ text: 'Sync Sales', icon: 'mdi-cloud-sync' }],
      page: '',
      fav: true,
      menu: false,
      message: false,
      hints: true,
      menu_item: 0,
      snack: false,
      snackColor: '',
      snackText: '',
      company: 'POS Awesome',
      company_img: '/assets/erpnext/images/erpnext-logo.svg',
      pos_profile: '',
      freeze: false,
      freezeTitle: '',
      freezeMsg: '',
      last_invoice: '',
      user_full_name: ''
    };
  },
  methods: {
    async fetchUserFullName() {
      try {
        const response = await frappe.call({
          method: 'posawesome.posawesome.api.posapp.get_user_full_name',
          args: {
            user: frappe.session.user
          }
        });
        if (response.message) {
          this.user_full_name = response.message;
        }
      } catch (error) {
        console.error('Error fetching user full name:', error);
      }
    },
    changePage(key) {
      this.$emit('changePage', key);
    },
    go_desk() {
      frappe.set_route('/');
      location.reload();
    },
    go_about() {
      const win = window.open(
        'https://github.com/yrestom/POS-Awesome',
        '_blank'
      );
      win.focus();
    },
    close_shift_dialog() {
      evntBus.$emit('open_closing_dialog');
    },
    show_mesage(data) {
      this.snack = true;
      this.snackColor = data.color;
      this.snackText = data.text;
    },
    logOut() {
        var me = this;
        me.logged_out = true;
        return frappe.call({
            method: 'logout',
            callback: function (r) {
                if (r.exc) {
                    return;
                }
                // Redirect to the login page after logout
                window.location.href = '/login';  // Redirects to base URL + /login
            },
        });
    },
    print_last_invoice() {
      if (!this.last_invoice) return;
      const print_format =
        this.pos_profile.print_format_for_online ||
        this.pos_profile.print_format;
      const letter_head = this.pos_profile.letter_head || 0;
      const url =
        frappe.urllib.get_base_url() +
        '/printview?doctype=Sales%20Invoice&name=' +
        this.last_invoice +
        '&trigger_print=1' +
        '&format=' +
        print_format +
        '&no_letterhead=' +
        letter_head;
      const printWindow = window.open(url, 'Print');
      printWindow.addEventListener(
        'load',
        function () {
          printWindow.print();
        },
        true
      );
    },
    // Start Price List Update
    async startPriceUpdate() {
      this.snack = true;
      this.snackColor = 'info';
      this.snackText = 'Price update in progress... this could take a few minutes.';
      
      try {
        // Call the backend function to update prices
        const response = await frappe.call({
          method: 'posawesome.posawesome.api.posapp.sync_item_price',
        });

        if (response.message.status === 'completed') {
          this.snackColor = 'success';
          this.snackText = 'Price update completed successfully!';
        } else if (response.message.status === 'volume_too_high') {
          this.snackColor = 'warning';
          this.snackText = 'Volume exceeds maximum for quick update. Please update price list from the Branch Control Center.';
        }
      } catch (error) {
        console.error('Error during price update:', error);
        this.snackColor = 'error';
        this.snackText = 'Error during price update.';
      }
    },
    // Start Price List Update
    async startStockUpdate() {
      this.snack = true;
      this.snackColor = 'info';
      this.snackText = 'Stock update in progress... this could take a few minutes.';
      
      try {
        // Call the backend function to update stock
        const response = await frappe.call({
          method: 'posawesome.posawesome.api.posapp.sync_stock',
        });

        // Handle the response status
        if (response.message.status === 'completed') {
          this.snackColor = 'success';
          this.snackText = 'Stock update completed successfully!';
        } else if (response.message.status === 'volume_too_high') {
          this.snackColor = 'warning';
          this.snackText = 'Volume exceeds maximum for quick update. Please update stock from the Branch Control Center.';
        } else {
          this.snackColor = 'error';
          this.snackText = 'Error updating stock!';
        }
      } catch (error) {
        console.error('Error during stock update:', error);
        this.snackColor = 'error';
        this.snackText = 'Error during stock update.';
      }
    },
    // Start Price List Update
    async startSalesUpdate() {
      this.snack = true;
      this.snackColor = 'info';
      this.snackText = 'Sales Invoice sync in progress... this could take a few minutes.';
      
      try {
        // Call the backend function to update stock
        const response = await frappe.call({
          method: 'posawesome.posawesome.api.posapp.sync_sales',
        });

        // Handle the response status
        if (response.message.status === 'completed') {
          this.snackColor = 'success';
          this.snackText = 'Sales Invoice sync completed successfully!';
        } else if (response.message.status === 'volume_too_high') {
          this.snackColor = 'warning';
          this.snackText = 'Volume exceeds maximum for quick update. Please update stock from the Branch Control Center.';
        } else {
          this.snackColor = 'error';
          this.snackText = 'Error updating sales invoices!';
        }
      } catch (error) {
        console.error('Error during sales invoice update:', error);
        this.snackColor = 'error';
        this.snackText = 'Error during sales invoice update.';
      }
    },
    showSnackbar(text, color) {
      this.snackText = text;
      this.snackColor = color;
      this.snack = true;
    },
  },
  created: function () {
    this.fetchUserFullName();
    this.$nextTick(function () {
      evntBus.$on('show_mesage', (data) => {
        this.show_mesage(data);
      });
      evntBus.$on('set_company', (data) => {
        this.company = data.name;
        this.company_img = data.company_logo
          ? data.company_logo
          : this.company_img;
      });
      evntBus.$on('register_pos_profile', (data) => {
        this.pos_profile = data.pos_profile;
        const payments = { text: 'Payments', icon: 'mdi-cash-register' };
        if (
          this.pos_profile.posa_use_pos_awesome_payments &&
          this.items.length !== 2
        ) {
          this.items.push(payments);
        }
      });
      evntBus.$on('set_last_invoice', (data) => {
        this.last_invoice = data;
      });
      evntBus.$on('freeze', (data) => {
        this.freeze = true;
        this.freezeTitle = data.title;
        this.freezeMsg = data.msg;
      });
      evntBus.$on('unfreeze', () => {
        this.freeze = false;
        this.freezTitle = '';
        this.freezeMsg = '';
      });
    });
  },
};
</script>

<style scoped>
.margen-top {
  margin-top: 0px;
}
</style>
