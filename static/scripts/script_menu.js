menu_links_header_text_div = document.getElementsByClassName('menu_links_header_text_div')[0]

menu_links_header_text_div.style.display = 'none'

function open_menu_links_header(){
  dark_screen = document.getElementsByClassName('dark_screen')[0]
  window_profile_div = document.getElementsByClassName('window_profile_div')[0]
  if (menu_links_header_text_div.style.display == 'none'){
    menu_links_header_text_div.style.display = 'flex';
    dark_screen.style.background = 'rgba(0, 0, 0, 0.04)'
    window_profile_div.style.filter = 'blur(2px)'
  }
  else{
    menu_links_header_text_div.style.display = 'none'
    dark_screen.style.background = 'none'
    window_profile_div.style.filter = 'none'
  }
}
