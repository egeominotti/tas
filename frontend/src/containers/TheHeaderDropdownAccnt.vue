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
        </div>
      </CHeaderNavLink>
    </template>
    <CDropdownHeader tag="div" class="text-center" color="light">
      <strong>Account</strong>
    </CDropdownHeader>

  </CDropdown>
</template>
