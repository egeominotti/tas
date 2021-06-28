<template>
  <div>
    <WidgetsDropdown/>
  </div>
</template>

<script>
import MainChartExample from './charts/MainChartExample'
import WidgetsDropdown from './widgets/WidgetsDropdown'
import WidgetsBrand from './widgets/WidgetsBrand'
import {CChartBar} from '@coreui/vue-chartjs'

export default {
  name: 'Dashboard',
  components: {
    MainChartExample,
    WidgetsDropdown,
    WidgetsBrand,
    CChartBar,
  },
}
</script>
