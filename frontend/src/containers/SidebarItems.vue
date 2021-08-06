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
            icon: 'cil-contact',
            items: [
              {
                name: 'My trades',
                to: '/bot/list',
              },
              {
                name: 'Trades History',
                to: '/bot/list',
              },
            ]
          },
          // {
          //   _name: 'CSidebarNavDropdown',
          //   name: 'Statistics',
          //   route: '/btby',
          //   icon: 'cil-contact',
          //   items: [
          //     {
          //       name: 'List statistics',
          //       to: '/btby/lista',
          //     },
          //   ]
          // },
        ]
      }]
    }
  }
}
</script>
