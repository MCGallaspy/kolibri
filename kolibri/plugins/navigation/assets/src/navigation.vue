<template>

  <header id="navigation-module">
    <nav class="titlebar">

      <div class="titlebar_left">
        <span class="titlebar_title">{{title_bar.title}}</span>
        <a class="titlebar_homelink" href="{{title_bar.home_link}}">Home</a>
      </div>

      <div class="titlebar_right">
        <span v-on:click="user_nav_display_toggle">{{user.first_name}}</span>
        <div class="usermenu" v-bind:style="{display: user_nav_display}">
          <ul>
            <li v-for="item in user_nav_items">
              <a href={{item.url}}>{{item.text}}</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <nav class="navlinks">
      <div class="navlinks_item" v-for="item in nav_items">
        <a href="{{item.url}}">{{ item.text }}</a>
      </div>
    </nav>
  </header>

</template>


<script>

  module.exports = {
    el: '#navigation-module',
    data: {
      // items that go in the title bar
      nav_items: global.kolibri_reserved.nav_items,
      title_bar: {
        title: 'Kolibri',
        home_link: '/',
      },
      user_nav_display: 'none',

      // items that go into the user menu
      user_nav_items: global.kolibri_reserved.user_nav_items,
      user: {
        username: 'foobar',
        first_name: 'Foo',
        last_name: 'Bar',
      },
    },
    methods: {
      user_nav_display_toggle() {
        if (this.user_nav_display === 'none') {
          this.user_nav_display = 'block';
        } else {
          this.user_nav_display = 'none';
        }
      },
    },
  };

</script>


<style lang="stylus" scoped>

  $kolibri_purple = #bd8cbf
  $kolibri_gray = #c4c4c4
  $kolibri_nav_fonts = sans-serif

  body
    // Getting rid of HTML's default margin
    margin:0
  header
    font-family: $kolibri_nav_fonts

  .titlebar
    // for consistent percentages. Maybe bring in normalize?
    box-sizing: border-box
    background-color: $kolibri_purple
    color: white

    // fix for the div float issue
    overflow: auto
    padding: 1 em
    width: 100%

    &_left
      float: left
      width:70%
    &_right
      float: right
      width: 30%
      span
        float: right

  .navlinks
    box-sizing: border-box
    overflow: auto
    width: 90%
    margin: 0 5% 0 5%
    padding-top: .5em
    border-bottom: 1px solid $kolibri_gray
    &_item
      float:left
      padding:0 .5em 0 .5em
      font-size: 1.5em
      a
        text-decoration: none
        color: $kolibri_gray

  .usermenu
    position:absolute
    top: 2em
    right: 1em
    box-shadow: 2px 2px 3px $kolibri_gray
    background-color: white
    ul
      padding: 3px
      list-style: none
    a
      color: $kolibri_gray
      text-decoration: none

</style>
