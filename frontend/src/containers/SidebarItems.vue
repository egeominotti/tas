<script>
export default {
  name: 'nav',
  computed: {
    sidebarItems() {
      return [{
        _name: 'CSidebarNav',
        _children: [{
          _name: 'CSidebarNavItem',
          name: this.$t('menu.dashboard'),
          to: '/dashboard',
          icon: 'cil-speedometer',
          badge: {
            color: 'danger'
          },
        },
          {
            _name: 'CSidebarNavDropdown',
            name: 'Bot',
            route: '/bot',
            icon: 'cib-probot',
            items: [
              {
                name: 'Trades Futures',
                to: '/bot/listFutures',
              },
              {
                name: 'Trades Spot',
                to: '/bot/listSpot',
              },
              {
                name: 'Trades History',
                to: '/bot/history',
              },
            ]
          },
          {
            _name: 'CSidebarNavDropdown',
            name: 'Account',
            route: '/account',
            icon: 'cil-contact',
            items: [
              {
                name: 'Exchange',
                to: '/account/viewExchange',
              },
            ]
          },
        ]
      }]
    }
  }
}
</script>
