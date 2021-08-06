<template>
  <CRow>
    <CCol sm="12">
      <CCard>

        <CCardHeader>
          <h5>List/Create your bot</h5>
        </CCardHeader>

        <CCardBody>
          <CButton
              @click="modalCreateBot = true"
              color="success"
              size="lg"
          >
            New Bot
          </CButton>
          <CModal
              size="md"
              :centered="true"
              title="Create new Bot"
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
                  color="success"
                  size="lg"
                  @click="spawnbot()"

              >
                Spawn Bot
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
    key: 'name',
    label: 'Id',
    sort: false,
    filter: false
  },
  {
    key: 'coins',
    label: 'Coins',
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
          this.modalCreateBot = false
        }
        console.log(response);
      }, (error) => {
        console.log(error.response.data);
        console.log(error.response.status);
        console.log(error.response.headers);
      });

      this.getData()
    },

    onTableChange() {
      this.loading = true
      setTimeout(() => {
        this.loading = false
        this.getData();
      }, 10)
    },

    getData() {

      if (this.tableFilterValue.length > 0) {
        axios
            .get(apiList)
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
            .get(apiList)
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
