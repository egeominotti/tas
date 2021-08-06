<template>
  <div class="c-app flex-row align-items-center" :class="{ 'c-dark-theme': $store.state.darkMode }">
    <CContainer>
      <CRow class="justify-content-center">
        <CCol md="8">
          <CCardGroup>
            <CCard class="p-4">
              <CCardBody>
                <CForm>
                  <h1 class="text-center">Login</h1>
                  <p class="text-muted text-center">Access the TAS dashboard</p>
                  <CInput
                      v-model="username"
                      placeholder="Type Username"
                      autocomplete="email"
                  >
                    <template #prepend-content>
                      <CIcon name="cil-user"/>
                    </template>
                  </CInput>
                  <CInput
                      v-model="password"
                      placeholder="Type Password"
                      type="password"
                  >
                    <template #prepend-content>
                      <CIcon name="cil-lock-locked"/>
                    </template>
                  </CInput>
                  <CRow>
                    <CCol col="12" class="text-center">
                      <CButton
                          v-on:click="login"
                          color="dark"
                          size="lg"
                          class="px-4">
                        Log in now

                      </CButton>
                    </CCol>
                  </CRow>
                </CForm>
              </CCardBody>
            </CCard>
          </CCardGroup>
        </CCol>
      </CRow>
    </CContainer>
  </div>
</template>

<script>

const urlApiLogin = '/api-token-auth/'

export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: '',
    }
  },
  methods: {
    login() {
      axios.post(urlApiLogin, {
        username: this.username,
        password: this.password,
      }).then((response) => {
        console.log(response);
        localStorage.setItem('token', response.data.token)
        localStorage.setItem('username', this.username)
        localStorage.setItem('password', this.password)
        this.$router.push('/dashboard')
      }, (error) => {
        console.log(error);
      });
    },
  },
  mounted() {
    if (localStorage.getItem('username')) {
      this.username = localStorage.getItem('username');
    }

    if (localStorage.getItem('password')) {
      this.password = localStorage.getItem('password');
    }
  },
}
</script>
