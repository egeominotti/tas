<template>
  <CSidebar
      :minimize="minimize"
      unfoldable
      :show="show"
      @update:show="(value) => $store.commit('set', ['sidebarShow', value])"
  >
<!--    <CSidebarBrand class="d-md-down-none" to="/">-->
<!--      <img-->
<!--           src="@/assets/logo/logo_dashboard_sfondo_scuro.svg"-->
<!--           class="c-sidebar-brand-full"-->
<!--           height="35"-->
<!--      >-->

<!--      <img-->
<!--           src="@/assets/logo/logo_dashboard_sfondo_scuro.svg"-->
<!--           class="c-sidebar-brand-minimized"-->
<!--           height="35"-->
<!--      >-->
<!--    </CSidebarBrand>-->
    <CRenderFunction flat :contentToRender="sidebarItems"/>
    <CSidebarMinimizer
        class="c-d-md-down-none"
        @click.native="$store.commit('toggle', 'sidebarMinimize')"
    />
  </CSidebar>
</template>

<script>
import SidebarItems from './SidebarItems'

export default {
  name: 'TheSidebar',
  extends: SidebarItems,
  computed: {
    show() {
      return this.$store.state.sidebarShow
    },
    minimize() {
      return this.$store.state.sidebarMinimize
    }
  }
}
</script>

