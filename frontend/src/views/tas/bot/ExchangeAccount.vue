<template>


  <CRow>

    <CCol sm="12">
      <CCard>

        <CCardHeader>
          <strong>Add yor preferite exchange</strong>
        </CCardHeader>

        <CCardBody>
          <CButton
              @click="modalCreateBot = true"
              color="dark"
              size="md"
          >
            Add Exchange
          </CButton>
        </CCardBody>
      </CCard>
    </CCol>

    <CCol sm="12">
      <CCard>

        <CCardHeader>
          <h5>My Exchange</h5>
        </CCardHeader>


        <CCardBody>


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
                    <div>${{ balance_futures }} </div>
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
              console.log(response.data.results);
              this.balance_spot = response.data.results[0].balance_spot;
              this.balance_futures = response.data.results[0].balance_futures;
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
