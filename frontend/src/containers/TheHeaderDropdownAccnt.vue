<template>
  <CDropdown
      inNav
      class="c-header-nav-items"
      placement="bottom-end"
      add-menu-classes="pt-0"
  >
    <template #toggler>
      <CHeaderNavLink>

        <div>
          My Account
        </div>
      </CHeaderNavLink>
    </template>
    <CDropdownHeader tag="div" class="text-center" color="light">
      <strong>Info</strong>
    </CDropdownHeader>

    <CDropdownItem>
      Account
    </CDropdownItem>

    <CDropdownItem>
      My Trades
    </CDropdownItem>

    <CDropdownItem v-on:click="logout">
      Login Page
    </CDropdownItem>

  </CDropdown>
</template>

<script>
export default {
  name: 'TheHeaderDropdownAccnt',
  data() {
    return {}
  },
  methods: {
    logout() {
      this.$router.push({
        name: 'Login',
      });
    },
  },
}
</script>

<style scoped>
.c-icon {
  margin-right: 0.3rem;
}
</style>
