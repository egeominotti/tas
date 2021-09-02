<template>
  <CRow>
    <div v-for="item in data" :key="item.id" class="iteration-for">

      <!--
      <div v-if="values(item.data).rsi > 30 && values(item.data).rsi < 70">
        <CCard>
          <CCardHeader>
            <p>{{ item.symbol }} - {{ item.time_frame }}</p>
          </CCardHeader>
          <CCardBody class="neutral-status">
            <p class="micro-condition"> RSI - {{ values(item.data).rsi }} </p>
          </CCardBody>
        </CCard>
      </div>
      -->

      <div v-if="values(item.data).rsi < 30">
        <CCard>
          <CCardHeader>
            <h5>{{ item.symbol }} - {{ item.time_frame }}</h5>
            <h5> Possible Long </h5>
          </CCardHeader>
          <CCardBody class="low-status">
            <h5>RSI - {{ values(item.data).rsi }}</h5>
            <h5>Close - {{ values(item.data).close }}</h5>
            <h5>Upperband - {{ values(item.data).upperband }}</h5>
            <h5>Middleband - {{ values(item.data).middleband }}</h5>
            <h5>Lowerband - {{ values(item.data).lowerband }}</h5>
          </CCardBody>
        </CCard>
      </div>

      <div v-if="values(item.data).rsi > 75">
        <CCard>
          <CCardHeader>
            <h5>{{ item.symbol }} - {{ item.time_frame }}</h5>
            <h5> Possible Short </h5>
          </CCardHeader>
          <CCardBody class="high-status">
            <h5>RSI - {{ values(item.data).rsi }}</h5>
            <h5>Close - {{ values(item.data).close }}</h5>
            <h5>Upperband - {{ values(item.data).upperband }}</h5>
            <h5>Middleband - {{ values(item.data).middleband }}</h5>
            <h5>Lowerband - {{ values(item.data).lowerband }}</h5>
          </CCardBody>
        </CCard>
      </div>


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
      polling: null
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

    getDataPolling() {
      this.polling = setInterval(() => {
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
      }, 5000)
    },

  },
  created() {
    this.getData();
    this.getDataPolling();
  },
  beforeDestroy() {
    clearInterval(this.polling)
  }
}
</script>

<style>
.card-body.neutral-status {
  background-color: #d0cfcf;
  font-weight: 100;
  text-align: center;
}

.card-body.high-status {
  background-color: #e55353;
  color: antiquewhite;
  font-weight: 900;
  text-align: center;
}

.card-body.low-status {
  background-color: #2eb85c;
  color: antiquewhite;
  font-weight: 900;
  text-align: center;
}

header.card-header {
  font-size: 10px;
  margin: 0;
  /* padding: 0; */
  text-align: center;
  padding-bottom: 0;
}

.card {
  border-radius: 10px 10px 10px 11px !important;
  border-color: black !important;
}

p.micro-condition {
  padding: 0;
  margin: 0;
  color: black;
  font-weight: 200;
}

.card {
  margin-right: 18px;
}

</style>
