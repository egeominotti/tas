<template>
  <CRow>
    <CCol sm="12">
      <CCard>

        <CCardHeader>
          <h5>My Trades</h5>
        </CCardHeader>

        <CCardBody>
          <CButton
              @click="modalCreateBot = true"
              color="dark"
              size="md"
          >
            Create new bot
          </CButton>

          <!--          <CButton-->
          <!--              @click="modalCreateBot = true"-->
          <!--              color="dark"-->
          <!--              size="md"-->
          <!--          >-->
          <!--            Create cluster bot-->
          <!--          </CButton>-->

          <CModal
              size="sm"
              :centered="true"
              title="Stop Bot"
              :backdrop="true"
              :closeOnBackdrop="false"
              color="dark"
              :show.sync="modalStopBot"
          >

            <template #footer>
              <CButton @click="modalStopBot = false" color="danger">Cancel</CButton>
              <CButton @click="update()" color="success">Stop bot</CButton>
            </template>

            <h6>Lorem ipsum, testo per confermare lo stop del bot</h6>
            <CCol sm="12">

              <!--              <CButton-->
              <!--                  color="warning"-->
              <!--                  size="lg"-->
              <!--                  @click="update()"-->
              <!--              >-->
              <!--                Yes-->
              <!--              </CButton>-->

              <!--              <CButton-->
              <!--                  color="success"-->
              <!--                  size="lg"-->
              <!--                  @click="modalStopBot=false"-->
              <!--              >-->
              <!--                No-->
              <!--              </CButton>-->
            </CCol>


          </CModal>

          <CModal
              size="lg"
              :centered="true"
              title="Create new Bot"
              :backdrop="true"
              :closeOnBackdrop="false"
              color="dark"
              :show.sync="modalCreateBot"
          >


            <template #footer>
              <CButton @click="modalCreateBot = false" color="danger">Cancel</CButton>
              <CButton @click="spawnbot()" color="success">Start trade</CButton>
            </template>


            <CCol sm="12">

              <label class="text">Choose Coin</label>
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
                <span slot="no-options">Write name of coins</span>

              </v-select>
              <br>
            </CCol>

            <CCol sm="12">

              <label class="text">Choose Strategy</label>
              <v-select
                  :options="strategy"
                  v-model="selected_strategy"
              >
                <template slot="selected-option" slot-scope="option">
                  {{ option.name }}
                </template>
                <template slot="option" slot-scope="option">
                  {{ option.name }}
                </template>
                <span slot="no-options">Write name of coins</span>

              </v-select>
              <br>
            </CCol>
          </CModal>
          <br>

          <CDataTable
              :items="loadedItems"
              :fields="fields"
              :table-filter-value.sync="tableFilterValue"
              :items-per-page="20"
              :active-page="1"
              outlined
              hover
              :loading="loading"
          >


            <template #id="{item}">
              <td>

                <CSpinner v-if="item.running" color="success" size="sm"/>
                <CBadge v-else color="danger" shape="pill">X</CBadge>
              </td>
            </template>


            <template #coins="{item}">
              <td>
                <h6>{{ item.coins.coins_exchange.symbol }}</h6>
              </td>
            </template>

            <template #strategy="{item}">
              <td>
                <h6>{{ item.strategy.name }}</h6>
              </td>
            </template>


            <template #time_frame="{item}">
              <td>
                <h6>{{ item.strategy.time_frame.time_frame }}</h6>
              </td>
            </template>

            <template #running="{item}">
              <td>
                <div v-if="item.running">
                  <CBadge color="success" shape="pill">Y</CBadge>
                </div>
                <div v-else>
                  <CBadge color="danger" shape="pill">N</CBadge>
                </div>
              </td>
            </template>

            <template #abort="{item}">
              <td>
                <div v-if="item.abort">
                  <CBadge color="success" shape="pill">Y</CBadge>
                </div>
                <div v-else>
                  <CBadge color="danger" shape="pill">N</CBadge>
                </div>
              </td>
            </template>

            <template #updated_at="{item}">
              <td>
                <CButton v-if="item.running"
                         class="custom-button-remove-bot"
                         @click="openModalStopBot(item.id)"
                         :disabled="false"
                         color="danger"
                         size="sm"
                >
                  Stop
                </CButton>

                <CButton v-else
                         class="custom-button-remove-bot"
                         :disabled="true"
                         color="danger"
                         size="sm"
                >
                  Stop
                </CButton>
              </td>
            </template>

            <template #flgEnable="{item}">
              <td>
                <CButton v-if="item.abort"
                         class="custom-button-remove-bot"
                         @click="destroy(item.id)"
                         :disabled="false"
                         color="danger"
                         size="sm"
                >
                  Remove
                </CButton>

                <CButton v-else
                         :disabled="true"
                         class="custom-button-remove-bot"
                         color="danger"
                         size="sm"
                >
                  Remove
                </CButton>

              </td>
            </template>

            <template #market_spot="{item}">
              <td>
                <div v-if="item.market_stop">
                  <CBadge color="success" shape="pill">Y</CBadge>
                </div>
                <div v-else>
                  <CBadge color="danger" shape="pill">N</CBadge>
                </div>
              </td>
            </template>

            <template #market_futures="{item}">
              <td>
                <div v-if="item.market_futures">
                  <CBadge color="success" shape="pill">Y</CBadge>
                </div>
                <div v-else>
                  <CBadge color="danger" shape="pill">N</CBadge>
                </div>
              </td>
            </template>

          </CDataTable>

        </CCardBody>
      </CCard>

    </CCol>
  </CRow>
</template>


<script>
const titleList = "Bot"
const apiList = '/api/v0/bot/list';
const apiCreateBot = 'api/v0/bot/create';
const apiDestroyBot = 'api/v0/bot/destroy/';
const apiUpdateBot = 'api/v0/bot/update/';
const apiGetListCoins = '/api/v0/coins/list'
const apiGetListStrategy = '/api/v0/strategybot/list'

const fields = [
  {
    key: 'id',
    label: 'Status',
    sort: false,
    filter: false
  },
  {
    key: 'name',
    label: 'Bot Id',
    sort: false,
    filter: false
  },
  {
    key: 'coins',
    label: 'Coin',
    sort: false,
    filter: false
  },
  {
    key: 'time_frame',
    label: 'Time Frame',
    sort: false,
    filter: false
  },
  {
    key: 'strategy',
    label: 'Strategy',
    sort: false,
    filter: false
  },
  {
    key: 'running',
    label: 'Running',
    sort: false,
    filter: false
  },
  {
    key: 'abort',
    label: 'Abort',
    sort: false,
    filter: false
  },
  {
    key: 'market_spot',
    label: 'Market Spot',
    sort: false,
    filter: false
  },
  {
    key: 'market_futures',
    label: 'Market Futures',
    sort: false,
    filter: false
  },
  {
    key: 'leverage',
    label: 'Leverage',
    sort: false,
    filter: false
  },
  {
    key: 'updated_at',
    label: 'Operation',
    sort: false,
    filter: false
  },
  {
    key: 'created_at',
    label: 'Created',
    sort: false,
    filter: false
  },
  {
    key: 'flgEnable',
    label: 'Remove',
    sort: false,
    filter: false
  },
]

export default {
  name: 'Bot',
  data() {
    return {
      coins: [],
      selected_coins: null,
      strategy: [],
      selected_strategy: null,
      perpetual_mode: false,
      columnFilterValue: {},
      tableFilterValue: '',
      titleList: titleList,
      activePage: 1,
      loadedItems: [],
      itemsPerPage: 10,
      message: '',
      loading: false,
      modalCreateBot: false,
      modalStopBot: false,
      pages: 0,
      currentPages: 1,
      currentbotid: null,
      fields: fields
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

    openModalStopBot(item) {
      this.modalStopBot = true
      this.currentbotid = item
    },

    getCoins() {
      axios
          .get(apiGetListCoins)
          .then((response) => {
            console.log(response);
            if (response.statusText === 'OK' && response.status === 200) {
              this.coins = response.data.results;
            }
          }, (error) => {
            console.log(error);
          });
    },
    getStrategy() {
      axios
          .get(apiGetListStrategy)
          .then((response) => {
            console.log(response);
            if (response.statusText === 'OK' && response.status === 200) {
              this.strategy = response.data.results;
            }
          }, (error) => {
            console.log(error);
          });
    },

    destroy(id) {

      axios.delete(apiDestroyBot + id, {
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

    update() {

      axios.patch(apiUpdateBot + this.currentbotid,
          {
            //abort: true,
            running: false
          }, {
            headers: {
              'Authorization': 'Token ' + localStorage.getItem('token')
            }
          }
      ).then((response) => {
        if (response.status === 500) {
        }
        if (response.status === 200 && response.statusText === 'OK') {
          this.modalStopBot = false
          this.getData();

        }
        console.log(response);
      }, (error) => {
        console.log(error.response.data);
        console.log(error.response.status);
        console.log(error.response.headers);
      });
    },

    spawnbot() {

      console.log(this.selected_coins);
      console.log(this.selected_strategy);
      axios.post(apiCreateBot,
          {
            coins: this.selected_coins.id,
            strategy: this.selected_strategy.id,
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
          this.modalCreateBot = false

        }
        console.log(response);
      }, (error) => {
        console.log(error.response.data);
        console.log(error.response.status);
        console.log(error.response.headers);
      });


    },

    onTableChange() {
      this.loading = true
      setTimeout(() => {
        this.loading = false
        this.getData();
      }, 0)
    },

    getData() {
      let header = {headers: {'Authorization': 'Token ' + localStorage.getItem('token')}};

      if (this.tableFilterValue.length > 0) {
        axios
            .get(apiList, header)
            .then((response) => {
              console.log(response);
              if (response.statusText === 'OK' && response.status === 200) {
                this.loadedItems = response.data.results;
              }
            }, (error) => {
              console.log(error);
            });
      } else {
        axios
            .get(apiList, header)
            .then((response) => {
              console.log(response);
              if (response.statusText === 'OK' && response.status === 200) {
                this.loadedItems = response.data.results;
              }
            }, (error) => {
              console.log(error);
            });
      }

    },
  },

  mounted() {
    this.getCoins();
    this.getStrategy();
    this.getData();
  },

  created() {
    setInterval(function () {
      this.getData();
    }.bind(this), 5000);
  }

}
</script>
