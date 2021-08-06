<template>
  <CRow>
    <CCol sm="12">
      <CCard>

        <CCardHeader>
          <h5>Bot history</h5>
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
  {
    key: 'bot_id',
    label: 'Bot name',
    sort: false,
    filter: false
  },
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
