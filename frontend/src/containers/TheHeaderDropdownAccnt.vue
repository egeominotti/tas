<template>
  <CDropdown
      inNav
      class="c-header-nav-items"
      placement="bottom-end"
      add-menu-classes="pt-0"
  >
    <template #toggler>
      <CHeaderNavLink>
        <div class="c-avatar">
          <img
              class="c-avatar-img"
          />
        </div>
      </CHeaderNavLink>
    </template>
    <CDropdownHeader tag="div" class="text-center" color="light">
      <strong>Account</strong>
    </CDropdownHeader>

    <!--    <CDropdownItem>-->
    <!--      <CIcon name="cil-bell"/> Updates-->
    <!--      <CBadge color="info" class="mfs-auto">{{ itemsCount }}</CBadge>-->
    <!--    </CDropdownItem>-->
    <!--    <CDropdownItem>-->
    <!--      <CIcon name="cil-envelope-open" /> Messages-->
    <!--      <CBadge color="success" class="mfs-auto">{{ itemsCount }}</CBadge>-->
    <!--    </CDropdownItem>-->
    <!--    <CDropdownItem>-->
    <!--      <CIcon name="cil-task" /> Tasks-->
    <!--      <CBadge color="danger" class="mfs-auto">{{ itemsCount }}</CBadge>-->
    <!--    </CDropdownItem>-->
    <!--    <CDropdownItem>-->
    <!--      <CIcon name="cil-comment-square" /> Comments-->
    <!--      <CBadge color="warning" class="mfs-auto">{{ itemsCount }}</CBadge>-->
    <!--    </CDropdownItem>-->

    <!--    <CDropdownItem>-->
    <!--      <CIcon name="cil-user"/>-->
    <!--      Profilo-->
    <!--    </CDropdownItem>-->
    <!--    <CDropdownItem>-->
    <!--      <CIcon name="cil-settings"/>-->
    <!--      Impostazioni-->
    <!--    </CDropdownItem>-->

    <CDropdownItem v-on:click="logout">
      <CIcon
          name="cil-lock-locked"
      />
      Cambia account
    </CDropdownItem>

  </CDropdown>
</template>

<script>
export default {
  name: 'TheHeaderDropdownAccnt',
  data() {
    return {
    }
  },
  methods: {
    logout() {
      this.$router.push({
        name: 'Login',
      });
    },
  },
  mounted() {
    this.getData();
  }
}
</script>

<style scoped>
.c-icon {
  margin-right: 0.3rem;
}
</style>
