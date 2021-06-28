<template>
  <CChartLine
      :datasets="defaultDatasets"
      :options="defaultOptions"
      :labels="labels"
  />
</template>

<script>
import {CChartLine} from '@coreui/vue-chartjs'
import {getStyle, hexToRgba} from '@coreui/utils/src'

export default {
  name: 'MainChartExample',
  components: {
    CChartLine
  },
    data() {
    return {
      info: null,
      todosList: [],
      selected: 'Month',
    }
  },
  computed: {
    defaultDatasets() {
      const brandSuccess = getStyle('success') || '#4dbd74'
      const brandInfo = getStyle('info') || '#20a8d8'
      const brandDanger = getStyle('danger') || '#f86c6b'

      const data1 = [10, 20, 30, 40, 50, 60, 70, 80, 100, 110, 120, 130]

      return [
        {
          label: 'Manifesto Caricati',
          backgroundColor: hexToRgba(brandInfo, 10),
          borderColor: brandInfo,
          pointHoverBackgroundColor: brandInfo,
          borderWidth: 3,
          data: data1
        }
      ]
    },
    defaultOptions() {
      return {
        maintainAspectRatio: false,
        legend: {
          display: false
        },
        scales: {
          xAxes: [{
            gridLines: {
              drawOnChartArea: true
            }
          }],
          yAxes: [{
            ticks: {
              beginAtZero: true,
              maxTicksLimit: 5,
              stepSize: Math.ceil(250 / 5),
              //max: 1000
            },
            gridLines: {
              display: true
            }
          }]
        },
        elements: {
          point: {
            radius: 1,
            hitRadius: 10,
            hoverRadius: 4,
            hoverBorderWidth: 3
          }
        }
      }
    },
    methods: {
    getData() {
      axios.get('/dashboard/api/v0/statistiche/view').then((response) => {
        if (response.statusText === 'OK' && response.status === 200) {
          this.data = _.first(response.data.results);
          console.log(this.data)

          this.visualizzazioni_pagina_azienda = this.data.visualizzazioni_pagina_azienda.toString();
          this.visualizzazioni_manifesti = this.data.visualizzazioni_manifesti.toString();
          this.visualizzazioni_necrologi = this.data.visualizzazioni_necrologi.toString();
          this.servizi_acquistati = this.data.servizi_acquistati.toString();
          this.manifesti_caricati = this.data.manifesti_caricati.toString();
          this.necrologi_caricati = this.data.necrologi_caricati.toString();

          this.visualizzazioni_pagina_azienda_json = _.values(this.data.visualizzazioni_pagina_azienda_json);
          this.visualizzazioni_manifesti_json = _.values(this.data.visualizzazioni_manifesti_json);
          this.visualizzazioni_necrologi_json = _.values(this.data.visualizzazioni_necrologi_json);
          this.servizi_acquistati_json = _.values(this.data.servizi_acquistati_json);
          this.manifesti_caricati_json = _.values(this.data.manifesti_caricati_json);
          this.necrologi_caricati_json = _.values(this.data.necrologi_caricati_json);

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
}
</script>
