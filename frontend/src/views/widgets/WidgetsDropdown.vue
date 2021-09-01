<template>
  <CRow>
    <div v-for="item in data" :key="item.id">

      <CCol sm="12">
        <CCard>
          <CCardHeader>
            <h5>{{ item.symbol }} - {{ item.time_frame }}</h5>
          </CCardHeader>

          <div v-if="values(item.data).rsi > 30 && values(item.data).rsi < 70">
            <CCardBody class="neutral-status">
              <h5> RSI - {{ values(item.data).rsi }} </h5>
            </CCardBody>
          </div>

          <div v-if="values(item.data).rsi < 30">
            <CCardBody class="low-status">
                <h5> RSI - {{ values(item.data).rsi }} </h5>
            </CCardBody>
          </div>

          <div v-if="values(item.data).rsi > 70">
            <CCardBody class="high-status">
              <h5>RSI - {{ values(item.data).rsi }}</h5>
            </CCardBody>
          </div>

        </CCard>
      </CCol>

    </div>

  </CRow>
</template>

<script>

import {CChartLineSimple, CChartBarSimple} from '../charts'
import {CChartBar, CChartLine} from '@coreui/vue-chartjs'
import CChartBarExample from "@/views/charts/CChartBarExample";

export default {
  name: 'WidgetsDropdown',
  components: {CChartBarExample, CChartLineSimple, CChartBarSimple, CChartBar, CChartLine},
  data() {
    return {
      data: {},
    };
  },
  methods: {

    values(item) {
      return JSON.parse(item)
    },

    getData() {
      axios
          .get('/api/v0/computedata/list', {
            headers: {
              'Authorization': 'Token ' + localStorage.getItem('token')
            }
          })
          .then((response) => {
            if (response.statusText === 'OK' && response.status === 200) {
              this.data = response.data.results
            }
          }, (error) => {
            console.log(error);
          });
    },
  },
  created() {
    this.getData();
  },
}
</script>

<style>
.card-body.neutral-status {
  background-color: #d0cfcf;
}

.card-body.high-status {
  background-color: #e55353;
}

.card-body.low-status {
  background-color: #2eb85c;
}
</style>
