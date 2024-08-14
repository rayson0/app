btn_see_password1 = document.getElementsByClassName('see_password')[0]
btn_see_password2 = document.getElementsByClassName('see_password')[1]

if (btn_see_password1 != undefined){
  btn_see_password1.onclick = eye1
}
if (btn_see_password2 != undefined){
  btn_see_password2.onclick = eye2
}

function eye1(){
  input_password1 = document.getElementsByClassName('password')[0]
  if (input_password1.type == 'password'){
    input_password1.type = 'text';
    btn_see_password1.src = '/static/images/eye_open.png'
  }
  else{
    input_password1.type = 'password'
    btn_see_password1.src = '/static/images/eye_close.png'
  }
}

 function eye2(){
   input_password2 = document.getElementsByClassName('password')[1]
   if (input_password2.type == 'password'){
     input_password2.type = 'text';
     btn_see_password2.src = '/static/images/eye_open.png'
   }
   else{
     input_password2.type = 'password';
     btn_see_password2.src = '/static/images/eye_close.png'
   }
}

checkbox = document.getElementById('checkbox-0')
function remember(){
  if (checkbox.checked){
    checkbox.value = true
  }
  else{
    checkbox.value = false
  }
}
