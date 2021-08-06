<template>
  <CRow>
    <CCol sm="12">
      <CCard>

        <CCardHeader>
          <h5>My Exchange</h5>
        </CCardHeader>

        <CCardBody>
         <CButton
              @click="modalCreateBot = true"
              color="dark"
              size="md"
          >
            Add Exchange
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

            <template #live="{item}">
              <td>
                <div v-if="item.live">
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
const apiListUserExchange = '/api/v0/userexhcange/list';
const apiCreateUserExchange = 'api/v0/userexhcange/create';

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
    key: 'balance_futures',
    label: 'Balance Futures',
    sort: false,
    filter: false
  },
  {
    key: 'balance_spot',
    label: 'Balance Spot',
    sort: false,
    filter: false
  },
  {
    key: 'leverage',
    label: 'Global Leverage',
    sort: false,
    filter: false
  },
  {
    key: 'live',
    label: 'Live',
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

    onTableChange() {
      this.loading = true
      setTimeout(() => {
        this.loading = false
        this.getData();
      }, 0)
    },

    getData() {
      let header = {headers: {'Authorization': 'Token ' + localStorage.getItem('token')}};

      axios
          .get(apiListUserExchange, header)
          .then((response) => {
            console.log(response);
            if (response.statusText === 'OK' && response.status === 200) {
              this.loadedItems = response.data.results;
            }
          }, (error) => {
            console.log(error);
          });

    },
  },

  mounted() {
    this.getData();
  },

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
