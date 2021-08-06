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
            route: '/btby',
            icon: 'cil-contact',
            items: [
              {
                name: 'Engine Bot',
                to: '/btby/lista',
              },
              // {
              //   name: 'List Bot',
              //   to: '/btby/lista',
              // },
              // {
              //   name: 'Log Bot',
              //   to: '/btby/lista',
              // },
            ]
          },
          {
            _name: 'CSidebarNavDropdown',
            name: 'Statistics',
            route: '/btby',
            icon: 'cil-contact',
            items: [
              {
                name: 'List statistics',
                to: '/btby/lista',
              },
            ]
          },
          // {
          //   _name: 'CSidebarNavDropdown',
          //   name: 'btby',
          //   route: '/btby',
          //   icon: 'cil-contact',
          //   items: [
          //     {
          //       name: 'Lista BtBy',
          //       to: '/btby/lista',
          //     },
          //   ]
          // }
        ]
      }]
    }
  }
}
</script>
