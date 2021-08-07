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
              size="lg"
              :centered="true"
              title="Create new Bot"
              :backdrop="true"
              :closeOnBackdrop="false"
              color="warning"
              :show.sync="modalCreateBot"
          >


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
            <CCol sm="12">
              <label class="text">Perpetual Mode</label>
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
            <CCol sm="12">

              <!--              <CCol sm="6">-->
              <!--                <CImg-->
              <!--                    :fluid="true"-->
              <!--                    width="150"-->
              <!--                    height="150"-->
              <!--                    src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRXCpYPKA9Tar0qJRWzoiGvhbbwPoKooLYxgg&usqp=CAU"></CImg>-->
              <!--              </CCol>-->
              <CButton
                  class="custom-bot-spawn-bot"
                  color="dark"
                  size="lg"
                  @click="spawnbot()"

              >
                Start Trade
              </CButton>

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
    key: 'created_at',
    label: 'Created',
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
      pages: 0,
      currentPages: 1,
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

    spawnbot() {

      console.log(this.selected_coins);
      console.log(this.selected_strategy);
      console.log(this.perpetual_mode)
      axios.post(apiCreateBot,
          {
            coins: this.selected_coins.id,
            strategy: this.selected_strategy.id,
            perpetual: this.perpetual_mode
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

  // created() {
  //   setInterval(function () {
  //     this.getData();
  //   }.bind(this), 5000);
  // }

}
</script>

<style>
footer.modal-footer {
  display: none;
}

button.btn {
  background-color: #262626;
}

button.btn:hover {
  background-color: #c03d3d;
}

.modal-warning .modal-header {
  color: #fff;
  background-color: #262625;
  text-align: center !important;
}

button.btn.custom-bot-spawn-bot.btn-success.btn-lg {
  width: 100%;
}

label.text {
  font-size: 16px !important;
  font-weight: 700;
}

</style>
