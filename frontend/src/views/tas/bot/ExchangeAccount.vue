<template>
  <CRow>
    <CCol sm="12">
      <CCard>

        <CCardHeader>
          <h5>My Exchange</h5>
        </CCardHeader>


        <CCardBody>

          <label class="text">Choose Exchange</label>
          <v-select
              label="name"
              :options="exchangeList"
              v-model="exchange"
          >
            <template slot="selected-option" slot-scope="option">
              {{ option.name }}
            </template>
            <template slot="option" slot-scope="option">
              {{ option.name }}
            </template>
            <span slot="no-options">Write name of exchange</span>

          </v-select>
          <br>

          <CInput
              label="Api Key"
              placeholder="Insert your api key"
              min-amount="1"
              v-model="apiKey"
          />

          <CInput
              label="Api Secret"
              placeholder="Insert your secret api key"
              min-amount="10"
              v-model="apiSecret"
          />


          <br>
          <CButton
              @click="saveUserEchange()"
              color="dark"
              size="md"
          >
            Save Exchange
          </CButton>

          <CModal
              size="lg"
              :centered="true"
              title="Create new Bot"
              :backdrop="true"
              :closeOnBackdrop="false"
              color="warning"
              :show.sync="modalCreateBot"
          >


            <CCol sm="12">

              <label class="text">Choose Exchange</label>
              <v-select
                  label=""
                  :options="coins"
                  v-model="selected_coins"
              >
                <template slot="selected-option" slot-scope="option">
                  {{ option.coins_exchange.symbol }}
                </template>
                <template slot="option" slot-scope="option">
                  {{ option.coins_exchange.symbol }}
                </template>
                <span slot="no-options">Write name of exchange</span>

              </v-select>
              <br>
            </CCol>

            <CCol sm="12">

            </CCol>
            <CCol sm="12">
              <label class="text">Live Mode</label>
              <br>
              <CSwitch
                  class="mx-1"
                  color="dark"
                  name="switch1"
                  :checked.sync="perpetual_mode"
              />
              <br>
              <br>
            </CCol>

          </CModal>


          <br>


        </CCardBody>
      </CCard>


      <CRow>
        <CCol sm="12">
          <CCard>

            <CCardHeader>
              <strong>Balance</strong>
            </CCardHeader>

            <CCardBody>
              <CDataTable
                  :items="loadedItems"
                  :fields="fields"
                  :table-filter-value.sync="tableFilterValue"
                  :items-per-page="50"
                  :active-page="1"
                  outlined
                  hover
                  :loading="loading"
              >

                <template #exchange="{item}">
                  <td>
                    <h6>{{ item.exchange.name }}</h6>
                  </td>
                </template>

                <template #id="{item}">
                  <td>
                    <CButton
                        class="custom-button-remove-bot"
                        @click="destroy(item.id)"
                        color="danger"
                        size="sm"
                    >
                      Remove
                    </CButton>

                  </td>
                </template>

              </CDataTable>
            </CCardBody>
          </CCard>
        </CCol>
      </CRow>

      <CRow>
        <CCol sm="12">
          <CCard>

            <CCardHeader>
              <strong>Balance</strong>
            </CCardHeader>

            <CCardBody>
              <table class="table">
                <thead>
                <tr>
                  <th>Futures balance</th>
                  <th>Spot balance</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                  <td>
                    <div>${{ balance_futures }}</div>
                  </td>
                  <td>
                    <div>${{ balance_spot }}</div>
                  </td>
                </tr>
                </tbody>
              </table>
            </CCardBody>
          </CCard>
        </CCol>
      </CRow>

    </CCol>


  </CRow>
</template>


<script>
const apiListUserExchange = '/api/v0/userexhcange/list';
const apiCreateUserExchange = '/api/v0/userexhcange/create';
const apiDestroyUserExchange = '/api/v0/userexhcange/destroy/';
const apiExchangeList = '/api/v0/exchangelist/list';

const fields = [
  {
    key: 'exchange',
    label: 'Exchange',
    sort: false,
    filter: false
  },
  {
    key: 'api_key',
    label: 'Api Key',
    sort: false,
    filter: false
  },
  {
    key: 'api_secret',
    label: 'Api Secret',
    sort: false,
    filter: false
  },
  {
    key: 'id',
    label: 'Operation',
    sort: false,
    filter: false
  },
]

export default {
  name: 'Account',
  data() {
    return {
      live_mode: false,
      coins: [],
      selected_coins: null,
      strategy: [],
      apiKey: null,
      apiSecret: null,
      liveMode: false,
      exchangeList: [],
      exchange: null,
      selected_strategy: null,
      perpetual_mode: false,
      columnFilterValue: {},
      tableFilterValue: '',
      activePage: 1,
      loadedItems: [],
      itemsPerPage: 10,
      message: '',
      loading: false,
      modalCreateBot: false,
      pages: 0,
      currentPages: 1,
      fields: fields,
      balance_futures: 0,
      balance_spot: 0
    }
  },
  watch: {
    reloadParams() {
      this.onTableChange()
    }
  },
  computed: {
    reloadParams() {
      return [
        this.sorterValue,
        this.columnFilterValue,
        this.tableFilterValue,
        this.activePage
      ]
    }
  },
  methods: {

    onTableChange() {
      this.loading = true
      setTimeout(() => {
        this.loading = false
        this.getData();
      }, 500)
    },

    saveUserEchange() {
      axios.post(apiCreateUserExchange,
          {
            exchange: this.exchange.id,
            api_key: this.apiKey,
            api_secret: this.apiSecret,
            live: this.liveMode
          }, {
            headers: {
              'Authorization': 'Token ' + localStorage.getItem('token')
            }
          }
      ).then((response) => {
        if (response.status === 500) {
        }
        if (response.status === 201 && response.statusText === 'Created') {
          this.getData();
          this.getExchangeList()
          this.apiKey = null;
          this.apiSecret = null;
          this.liveMode = false;
          this.exchange = null;

        }
        console.log(response);
      }, (error) => {
        console.log(error.response.data);
        console.log(error.response.status);
        console.log(error.response.headers);
      });

    },

    destroy(id) {

      axios.delete(apiDestroyUserExchange + id, {
            headers: {
              'Authorization': 'Token ' + localStorage.getItem('token')
            }
          }
      ).then((response) => {
        if (response.status === 500) {
        }
        if (response.status === 204 && response.statusText === 'No Content') {
          this.getData();
        }
        console.log(response);
      }, (error) => {
        console.log(error.response.data);
        console.log(error.response.status);
        console.log(error.response.headers);
      });
    },

    getData() {
      let header = {headers: {'Authorization': 'Token ' + localStorage.getItem('token')}};

      axios
          .get(apiListUserExchange, header)
          .then((response) => {
            console.log(response);
            if (response.statusText === 'OK' && response.status === 200) {
              this.loadedItems = response.data.results;
              console.log(response.data.results);
              this.balance_spot = response.data.results[0].balance_spot;
              this.balance_futures = response.data.results[0].balance_futures;
              // this.apiKey = response.data.results[0].api_key;
              // this.apiSecret = response.data.results[0].api_secret;
              // this.liveMode = response.data.results[0].live;
              // this.exchange = response.data.results[0].exchange;
            }
          }, (error) => {
            console.log(error);
          });
    },

    getExchangeList() {
      let header = {headers: {'Authorization': 'Token ' + localStorage.getItem('token')}};

      axios
          .get(apiExchangeList, header)
          .then((response) => {
            console.log(response);
            if (response.statusText === 'OK' && response.status === 200) {
              this.exchangeList = response.data.results;
              console.log(response.data.results);
            }
          }, (error) => {
            console.log(error);
          });
    },
  },

  mounted() {
    this.getData();
    this.getExchangeList()
  },

}
</script>
