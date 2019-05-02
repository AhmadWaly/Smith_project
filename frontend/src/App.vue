<template>
  <div id="app">
    <b-navbar fixed="top" toggleable="sm" type="dark" variant="dark">
      <b-navbar-toggle class="mr-auto" target="nav-collapse"></b-navbar-toggle>
      <b-navbar-brand to="/">Smith Login System</b-navbar-brand>
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav class="ml-auto">
          <b-nav-item to="/login">Login</b-nav-item>
          <b-nav-item to="/register">Register</b-nav-item>
        </b-navbar-nav>
      </b-collapse>

    </b-navbar>

    <router-view />
  </div>
</template>

<style>

.router-link-active{
  color: white !important;
}

#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
