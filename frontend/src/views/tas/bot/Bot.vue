<template>
  <CRow>
    <CCol sm="12">
      <CCard>

        <CCardHeader>
          <h5>List/Create your bot</h5>
        </CCardHeader>

        <CCardBody>

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
      columnFilterValue: {},
      tableFilterValue: '',
      titleList: titleList,
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

    onTableChange() {
      this.loading = true
      setTimeout(() => {
        this.loading = false
        this.getData();
      }, 100)
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
  created() {
    setInterval(function () {
      this.getData();
    }.bind(this), 5000);
  }

}
</script>
