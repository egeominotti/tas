<template>
  <CRow>
    <CCol sm="12">
      <CCard>

        <CCardHeader>
          <h5>Trades History</h5>
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

            <template #stop_loss="{item}">
              <td>
                <div v-if="item.stop_loss">
                  <CBadge color="success" shape="pill">Y</CBadge>
                </div>
                <div v-else>
                  <CBadge color="danger" shape="pill">N</CBadge>
                </div>
              </td>
            </template>

            <template #take_profit="{item}">
              <td>
                <div v-if="item.take_profit">
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
const apiList = '/api/v0/botlogger/list';

const fields = [
  // {
  //   key: 'bot_id',
  //   label: 'Bot name',
  //   sort: false,
  //   filter: false
  // },
  {
    key: 'start_balance',
    label: 'Start balance',
    sort: false,
    filter: false
  },
  {
    key: 'end_balance',
    label: 'End balance',
    sort: false,
    filter: false
  },
  {
    key: 'entry_candle',
    label: 'Entry Candle Value',
    sort: false,
    filter: false
  },
  {
    key: 'entry_candle_date',
    label: 'Entry Candle Date',
    sort: false,
    filter: false
  },
  {
    key: 'take_profit',
    label: 'Take profit',
    sort: false,
    filter: false
  },
  {
    key: 'candle_take_profit',
    label: 'Candle Take Profit Value',
    sort: false,
    filter: false
  },
  {
    key: 'candle_take_profit_date',
    label: 'Candle Take Profit Date',
    sort: false,
    filter: false
  },
  {
    key: 'stop_loss',
    label: 'Stop loss',
    sort: false,
    filter: false
  },
  {
    key: 'candle_stop_loss',
    label: 'Candle Stop Loss Value',
    sort: false,
    filter: false
  },
  {
    key: 'candle_stop_loss_date',
    label: 'Candle Stop Loss Date',
    sort: false,
    filter: false
  },

  {
    key: 'take_profit_ratio',
    label: 'Take profit ratio',
    sort: false,
    filter: false
  },
  {
    key: 'stop_loss_ratio',
    label: 'Stop loss ratio',
    sort: false,
    filter: false
  },
]

export default {
  name: 'BotHistory',
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

    onTableChange() {
      this.loading = true
      setTimeout(() => {
        this.loading = false
        this.getData();
      }, 200)
    },

    getData() {
      const header = {headers: {'Authorization': 'Token ' + localStorage.getItem('token')}};

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
    this.getData();
  },
}

</script>
