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
            name: 'btby',
            route: '/btby',
            icon: 'cil-contact',
            items: [
              {
                name: 'Lista BtBy',
                to: '/btby/lista',
              },
            ]
          }
        ]
      }]
    }
  }
}
</script>
