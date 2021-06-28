<template>
  <CRow>
    <CCol sm="12">
      <CCard>

        <CCardHeader>
          <h5>Lista BTC/Long Short Ratio Index</h5>
        </CCardHeader>

        <CCardBody>

          <h5> Tabella Ratio 5 minuti</h5>
          <br>
          <CSelect
              label="Symbol"
              :value.sync="symbolSelected"
              :options="symbols"
              @change="test"
          />

          <br>
          <CDataTable
              :items="loadedItems"
              :fields="fields"
              :table-filter-value.sync="tableFilterValue"
              :items-per-page="288"
              :active-page="1"
              outlined
              hover
              :loading="loading"
          >

            <template #creato="{item}">
              <td>
                <h6>{{ resolveDatetime(item.created_at) }}</h6>
              </td>
            </template>

            <template #Trigger="{item}">
              <td>

                <CAlert v-if="computerResultFromRatio(item)==0" color="success" class="buy-alert">
                  BUY
                </CAlert>

                <CAlert v-if="computerResultFromRatio(item)==1" color="danger" class="sell-alert">
                  SELL
                </CAlert>

                <CAlert v-if="computerResultFromRatio(item)==2">
                </CAlert>

              </td>
            </template>

          </CDataTable>

        </CCardBody>
      </CCard>

    </CCol>
  </CRow>
</template>


<script>
const titleList = "BtBYList"
const bodyModal = "Attenzione! Sei sicuro di voler cancellare permanentemente questo manifesto?";
const titleModal = "Eliminazione Manifesto";
const apiList = '/api/analytics/bybt/';

const fields = [
  {
    key: 'creato',
    label: 'Data e Ora',
    sort: false,
    filter: false
  },
  {
    key: 'longShortRateListLast',
    label: 'Indice',
    sort: false,
    filter: false
  },
  {
    key: 'Trigger',
    label: 'Operazioni',
    sort: false,
    filter: false
  },
]

export default {
  name: 'ListlongShortRateListLast',
  data() {
    return {
      symbols: [
        'BTC',
        'ETH',
        'EOS',
        'LTC',
        'XRP',
        'BSV',
        'ETC',
        'TRX',
        'LINK',
      ],
      symbolSelected: 'BTC',
      columnFilterValue: {},
      tableFilterValue: '',
      titleList: titleList,
      titleModal: titleModal,
      bodyModal: bodyModal,
      activePage: 1,
      loadedItems: [],
      itemsPerPage: 12,
      message: '',
      loading: false,
      warningModal: false,
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

    computerResultFromRatio(item) {
      if (item.longShortRateListLast >= 1.31) {
        return 0;
      } else if (item.longShortRateListLast <= 0.78) {
        return 1;
      } else {
        return 2;
      }
    },

    resolveDatetime(datetimeObj) {
      return new Date(datetimeObj).toLocaleString()
    },

    onTableChange() {
      this.loading = true
      setTimeout(() => {
        this.loading = false
        this.getData();
      }, 1000)
    },

    test() {
      this.getData();
    },

    getData() {

      if (this.tableFilterValue.length > 0) {
        axios
            .get(apiList + '?symbol=' + this.symbolSelected)
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
            .get(apiList + '?symbol=' + this.symbolSelected)
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
  created() {
    setInterval(function () {
      this.getData();
    }.bind(this), 10000);
  }

}
</script>

<style>
tr {
  height: 40px;
  font-weight: 700;
}

td {
  height: 65px;
  font-weight: 700;
}

.buy-alert.alert.alert-success {
  text-align: center;
  font-weight: 800;
  /* width: 85px; */
  margin: auto;
}

.sell-alert.alert.alert-danger {
  text-align: center;
  font-weight: 800;
  /* width: 85px; */
  margin: auto;
}

</style>
