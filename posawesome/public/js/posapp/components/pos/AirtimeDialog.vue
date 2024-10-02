<template>
    <v-dialog v-model="isVisible" max-width="800px">
        <v-card>
            <!-- Full-Width Centered Header -->
            <div class="dialog-title-wrapper">
                <h1 class="dialog-title">Airtime Sale</h1>
            </div>
            <!-- Subtitle: Only shown if purchase is not yet successful -->
            <v-card-subtitle class="dialog-subtitle" v-if="!selectedNetworkPin">
                {{ subtitleText }}
            </v-card-subtitle>
            <v-card-text>
                <!-- Carrier Selection Screen -->
                <v-row v-if="!selectedCarrier && !selectedNetworkPin" justify="center">
                    <!-- Box for Airtel -->
                    <v-col cols="4" class="d-flex justify-center">
                        <v-card
                            class="pa-2 text-center carrier-card square-card"
                            @click="selectCarrier('Airtel')"
                        >
                            <v-img
                                src="/assets/posawesome/js/posapp/components/pos/Airtel.png"
                                alt="Airtel"
                                contain
                                height="100"
                                width="100"
                            ></v-img>
                        </v-card>
                    </v-col>
                    <!-- Box for MTN -->
                    <v-col cols="4" class="d-flex justify-center">
                        <v-card
                            class="pa-2 text-center carrier-card square-card"
                            @click="selectCarrier('MTN')"
                        >
                            <v-img
                                src="/assets/posawesome/js/posapp/components/pos/MTN.png"
                                alt="MTN"
                                contain
                                height="100"
                                width="100"
                            ></v-img>
                        </v-card>
                    </v-col>
                    <!-- Box for Glo -->
                    <v-col cols="4" class="d-flex justify-center">
                        <v-card
                            class="pa-2 text-center carrier-card square-card"
                            @click="selectCarrier('Glo')"
                        >
                            <v-img
                                src="/assets/posawesome/js/posapp/components/pos/Glo.png"
                                alt="Glo"
                                contain
                                height="100"
                                width="100"
                            ></v-img>
                        </v-card>
                    </v-col>
                </v-row>

                <!-- After selecting a carrier -->
                <v-row
                    v-if="selectedCarrier && !selectedAirtimeValue && !selectedNetworkPin"
                    align="center"
                >
                    <!-- Display selected carrier logo on the left -->
                    <v-col cols="4" class="d-flex justify-center">
                        <v-card class="pa-2 text-center carrier-card square-card">
                            <v-img
                                :src="carrierLogo[selectedCarrier]"
                                :alt="selectedCarrier"
                                contain
                                height="100"
                                width="100"
                            ></v-img>
                        </v-card>
                    </v-col>
                    <!-- Display airtime value buttons or message -->
                    <v-col cols="8" class="d-flex flex-column align-center justify-center">
                        <template v-if="isFetching">
                            <v-progress-circular indeterminate color="primary"></v-progress-circular>
                        </template>
                        <div v-else-if="airtimeValues.length > 0">
                            <v-btn
                                v-for="value in airtimeValues"
                                :key="value"
                                class="my-2 mx-2"
                                color="primary"
                                @click="selectAirtimeValue(value)"
                            >
                                {{ formatCurrency(value) }}
                            </v-btn>
                        </div>
                        <div v-else>
                            Not available for recharge at this time. Please try again later.
                        </div>
                    </v-col>
                </v-row>

                <!-- After selecting an airtime value -->
                <v-row v-if="selectedAirtimeValue && !selectedNetworkPin" align="center">
                    <!-- Display selected carrier logo and amount on the left -->
                    <v-col cols="4" class="d-flex flex-column justify-center align-center">
                        <v-card class="pa-2 text-center carrier-card square-card">
                            <v-img
                                :src="carrierLogo[selectedCarrier]"
                                :alt="selectedCarrier"
                                contain
                                height="100"
                                width="100"
                            ></v-img>
                        </v-card>
                        <!-- Display selected amount -->
                        <div class="selected-amount mt-2">
                            {{ formatCurrency(selectedAirtimeValue) }}
                        </div>
                    </v-col>
                    <!-- Display payment mode select field -->
                    <v-col cols="8" class="d-flex flex-column align-center justify-center">
                        <v-select
                            v-if="paymentModes.length > 0"
                            v-model="selectedPaymentMode"
                            :items="paymentModes"
                            label="Select Mode of Payment"
                            outlined
                            dense
                            class="my-2"
                        ></v-select>
                        <!-- Process Purchase Button -->
                        <v-btn
                            v-if="selectedPaymentMode"
                            color="primary"
                            @click="processPurchase"
                        >
                            Process Purchase
                        </v-btn>
                    </v-col>
                </v-row>

                <!-- Display Serial, PIN, and Print Button after successful purchase -->
                <v-row v-if="selectedNetworkPin" align="center">
                    <!-- Display selected carrier logo on the left -->
                    <v-col cols="4" class="d-flex justify-center">
                        <v-card class="pa-2 text-center carrier-card square-card">
                            <v-img
                                :src="carrierLogo[selectedCarrier]"
                                :alt="selectedCarrier"
                                contain
                                height="100"
                                width="100"
                            ></v-img>
                        </v-card>
                    </v-col>
                    <!-- Display serial, pin, and other details -->
                    <v-col cols="8" class="d-flex flex-column align-center">
                        <h3>Purchase Successful</h3>
                        <v-card class="pa-2 text-center mt-4">
                            <div><strong>Serial:</strong> {{ selectedNetworkPin.serial }}</div>
                            <div><strong>PIN:</strong> {{ selectedNetworkPin.pin }}</div>
                            <div><strong>Amount:</strong> {{ formatCurrency(selectedAirtimeValue) }}</div>
                            <div><strong>Ref:</strong> {{ salesInvoiceRef }}</div>
                            <div><strong>Date:</strong> {{ salesInvoiceDate }}</div>
                            <div><strong>Cashier:</strong> {{ this.user_full_name }}</div>
                        </v-card>
                        <v-btn color="primary" class="mt-4" @click="printReceipt">
                            <v-icon left>mdi-printer</v-icon> Print
                        </v-btn>
                    </v-col>
                </v-row>
            </v-card-text>
            <v-card-actions class="justify-space-between">
                <!-- Back Button -->
                <v-btn
                    v-if="selectedCarrier && !selectedNetworkPin"
                    color="primary"
                    text
                    @click="goBackToCarriers"
                >
                    Back
                </v-btn>
                <v-btn color="primary" text @click="closeDialog">Close</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

  
  
  <script>
  import { evntBus } from '../../../../js/posapp/bus';
  
  export default {
    props: {
      isVisible: {
        type: Boolean,
        default: false,
      },
    },
    data() {
      return {
        subtitleText: 'Select Carrier',
        selectedCarrier: '',
        airtimeValues: [],
        selectedAirtimeValue: null,
        paymentModes: [],
        selectedPaymentMode: null,
        isFetching: false, // Tracks the loading state
        carrierLogo: {
          Airtel: '/assets/posawesome/js/posapp/components/pos/Airtel.png',
          MTN: '/assets/posawesome/js/posapp/components/pos/MTN.png',
          Glo: '/assets/posawesome/js/posapp/components/pos/Glo.png',
        },
        pos_profile: null, // Initialize pos_profile as null
        selectedNetworkPin: null, // Stores the selected Network PIN details
        salesInvoiceRef: '', // Reference for the Sales Invoice
        salesInvoiceDate: '', // Date for the Sales Invoice
      };
    },
    methods: {
      closeDialog() {
        this.resetData(); // Clear data before closing the dialog
        this.$emit('close');
      },
      resetData() {
        this.subtitleText = 'Select Carrier';
        this.selectedCarrier = '';
        this.airtimeValues = [];
        this.selectedAirtimeValue = null;
        this.paymentModes = [];
        this.selectedPaymentMode = null;
        this.isFetching = false;
        this.selectedNetworkPin = null;
        this.salesInvoiceRef = '';
        this.salesInvoiceDate = '';
        },
      selectCarrier(carrier) {
        this.selectedCarrier = carrier;
        this.subtitleText = 'Select Recharge Amount';
        this.fetchAirtimeValues(carrier);
      },
      async fetchAirtimeValues(network) {
        this.isFetching = true; // Start loading state
        try {
          const response = await frappe.call({
            method: 'pricewise.api.api.get',
            args: {
              doctype: 'Network PIN',
              filters: {
                network: network,
                status: 'Available',
              },
              fields: ['value'], // Assuming 'value' is the field representing the airtime value
            },
          });
  
          // Extract unique airtime values and sort them in ascending order
          const uniqueValues = [...new Set(response.message.map(item => item.value))];
          this.airtimeValues = uniqueValues.sort((a, b) => a - b);
        } catch (error) {
          console.error('Error fetching airtime values:', error);
          this.airtimeValues = [];
        } finally {
          this.isFetching = false; // End loading state
        }
      },
      selectAirtimeValue(value) {
        this.selectedAirtimeValue = value;
        this.subtitleText = 'Select Mode of Payment';
        this.fetchPaymentModes();
      },
      async fetchPaymentModes() {
        try {
          const response = await frappe.call({
            method: 'frappe.client.get_list',
            args: {
              doctype: 'Mode of Payment',
              fields: ['name'],
            },
          });
  
          // Populate payment modes
          this.paymentModes = response.message.map(item => item.name);
        } catch (error) {
          console.error('Error fetching payment modes:', error);
          this.paymentModes = [];
        }
      },
      goBackToCarriers() {
        // Reset the selected carrier and subtitle
        this.selectedCarrier = '';
        this.selectedAirtimeValue = null;
        this.selectedPaymentMode = null;
        this.subtitleText = 'Select Carrier';
        this.airtimeValues = [];
      },
      formatCurrency(value) {
        // Format the value as currency with ₦ symbol and .00
        return `₦${value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
      },
      async processPurchase() {
        // Ensure pos_profile is available
        if (!this.pos_profile) {
            frappe.msgprint('POS Profile details are missing. Please ensure the data is loaded.');
            return;
        } else if (!this.pos_profile.customer) {
          frappe.msgprint('Default Customer missing in POS Profile. Please set default customer in POS Profile.');
          return;        
        }

        // Construct the item code using the selected carrier and value
        const item = `${this.selectedCarrier}-${this.selectedAirtimeValue}`;
      
        // Collect necessary data to create Sales Invoice
        const customer = this.pos_profile.customer;
        const branch = this.pos_profile.branch;
        const cost_center = this.pos_profile.cost_center;
        const qty = 1;
        const rate = this.selectedAirtimeValue;
        const mode_of_payment = this.selectedPaymentMode;
        const amount = rate;

        // Create Sales Invoice data
        const salesInvoiceData = {
            doctype: "Sales Invoice",
            customer: customer,
            branch: branch,
            is_pos: 1,
            update_stock: 1,
            set_warehouse: "Stores - PW",
            items: [
            {
                item_code: item,
                qty: qty,
                rate: rate,
                cost_center: cost_center,
                warehouse: "Stores - PW",
            },
            ],
            payments: [
            {
                mode_of_payment: mode_of_payment,
                amount: amount,
            },
            ],
        };

        try {
            // Create and submit the Sales Invoice
            const response = await frappe.call({
                method: "frappe.client.insert",
                args: {
                    doc: salesInvoiceData,
                },
            });

            if (response.message) {
                const submittedInvoice = await frappe.call({
                    method: "frappe.client.submit",
                    args: {
                        doc: response.message,
                    },
                });

                // Save additional details for successful screen
                this.salesInvoiceRef = submittedInvoice.message.name;
                this.salesInvoiceDate = submittedInvoice.message.posting_date;

                // Change subtitle
                this.subtitleText = 'Purchase Successful';

                // Fetch the Network PIN record for the selected carrier and value
                this.fetchNetworkPin(submittedInvoice.message);
            }
        } catch (error) {
            console.error('Error creating Sales Invoice:', error);
            frappe.msgprint('Failed to create Sales Invoice. Please try again.');
        }
    },
    printReceipt() {
        // Extract just the invoice number part from salesInvoiceRef
        const invoiceNumber = this.salesInvoiceRef.replace(/.*-SINV/, 'SINV');

        // Format the PIN into groups of 4 digits
        const formattedPin = this.selectedNetworkPin.pin.match(/.{1,4}/g).join(' ');

        const printContent = `
            <div style="font-size: 12px; text-align: center;">
                <!-- Carrier Logo -->
                <img src="${this.carrierLogo[this.selectedCarrier]}" alt="${this.selectedCarrier}" style="height: 80px; width: auto;" />
                <h2>Recharge Voucher</h2>
                <p><strong>${this.selectedCarrier}</strong> - ${this.formatCurrency(this.selectedAirtimeValue)} Pay as you Go</p>
                <hr>
                <!-- Make PIN larger and bolder -->
                <p style="font-size: 20px; font-weight: bold; margin-top: 10px;"><strong>PIN:</strong> ${formattedPin}</p>
                <p><strong>Amount:</strong> ${this.formatCurrency(this.selectedAirtimeValue)}</p>
                <p><strong>Serial:</strong> ${this.selectedNetworkPin.serial}</p>
                <p><strong>Ref:</strong> ${invoiceNumber}</p>
                <p><strong>Date:</strong> ${this.salesInvoiceDate}</p>
                <p><strong>Cashier:</strong> ${this.user_full_name}</p>
                <hr>
                <p>- Print Done -</p>
            </div>
        `;
        
        // Create a new window and print
        const printWindow = window.open('', '', 'height=600,width=800');
        printWindow.document.write('<html><head><title>Print Voucher</title>');
        printWindow.document.write('</head><body >');
        printWindow.document.write(printContent);
        printWindow.document.write('</body></html>');
        printWindow.document.close();
        printWindow.print();
    },

      async fetchNetworkPin(salesInvoice) {
        try {
          const response = await frappe.call({
            method: 'frappe.client.get_list',
            args: {
              doctype: 'Network PIN',
              filters: {
                network: this.selectedCarrier,
                value: this.selectedAirtimeValue,
                status: 'Available',
              },
              fields: ['name', 'pin', 'date_added'], // Fetching relevant fields
              order_by: 'date_added asc', // Get the oldest date added
              limit: 1, // Fetch the oldest available record
            },
          });
  
          if (response.message && response.message.length > 0) {
            // Get the first (and only) Network PIN record
            const networkPin = response.message[0];
  
            // Display Serial and PIN
            this.selectedNetworkPin = {
              serial: networkPin.name,
              pin: networkPin.pin,
            };
  
            // Update Network PIN status to Sold
            this.updateNetworkPinStatus(networkPin.name, salesInvoice);
          } else {
            frappe.msgprint('No available Network PIN found for this carrier and value.');
          }
        } catch (error) {
          console.error('Error fetching Network PIN:', error);
          frappe.msgprint('Failed to fetch Network PIN. Please try again.');
        }
      },
  
      async updateNetworkPinStatus(pinName, salesInvoice) {
        try {
          // Update the Network PIN record
          await frappe.call({
            method: 'frappe.client.set_value',
            args: {
              doctype: 'Network PIN',
              name: pinName,
              fieldname: {
                status: 'Sold',
                sales_invoice: salesInvoice.name,
                sold_by: salesInvoice.sales_user, // Assuming sales_user is part of Sales Invoice
                branch: salesInvoice.branch,
                date_sold: salesInvoice.posting_date,
              },
            },
          });
  
        } catch (error) {
          console.error('Error updating Network PIN status:', error);
          frappe.msgprint('Failed to update Network PIN status. Please try again.');
        }
      },
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
    },
    created() {
        this.fetchUserFullName();
    },
    mounted() {
      // Listen for the register_pos_profile event to receive pos_profile data
      evntBus.$on('register_pos_profile', (data) => {
        this.pos_profile = data.pos_profile;
        console.log('POS Profile received in AirtimeDialog:', this.pos_profile);
      });
    },
  };
  </script>
  
  
  <style scoped>
  .dialog-title-wrapper {
    background: linear-gradient(145deg, #ffffff, #e0e0e0);
    padding: 20px;
    box-shadow: 3px 3px 6px #b8b9be, -3px -3px 6px #fff;
    text-align: center;
    border-radius: 8px 8px 0 0;
  }
  
  .dialog-title {
    font-size: 28px;
    font-weight: bold;
    text-transform: uppercase;
    margin: 0;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    color: #0d47a1;
  }
  
  .dialog-subtitle {
    text-align: center;
    font-size: 16px;
    margin-top: 8px;
    margin-bottom: 16px;
  }
  
  .carrier-card {
    cursor: pointer;
    transition: transform 0.2s ease-in-out;
    padding: 8px;
  }
  
  .carrier-card:hover {
    transform: scale(1.05);
  }
  
  .square-card {
    height: 120px;
    width: 120px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 8px;
    box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.16);
    background-color: #fff;
  }
  
  .selected-amount {
    font-size: 20px;
    font-weight: bold;
  }
  
  .v-card-actions {
    padding: 10px;
  }
  
  .print-content {
    font-size: 12px;
    font-family: 'Courier New', Courier, monospace;
  }
  </style>
  