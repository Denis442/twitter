const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))



const active_Page = window.location.pathname;
const navLinks = document.querySelectorAll('a').forEach(link => {
  if( active_Page !=='/1' ){
    if(link.href.includes(`${active_Page}`)){
      link.classList.add('active');
    }}
})

let cords = ['scrollX','scrollY'];
// Перед закрытием записываем в локалсторадж window.scrollX и window.scrollY как scrollX и scrollY
window.addEventListener('unload', e => cords.forEach(cord => localStorage[cord] = window[cord]));
// Прокручиваем страницу к scrollX и scrollY из localStorage (либо 0,0 если там еще ничего нет)
window.scroll(...cords.map(cord => localStorage[cord]));

let coll = document.getElementsByClassName('sidebarOption')
for(let i =0;i < coll.length; i++){

  coll[i].addEventListener('click', function(){
    let content = this.nextElementSibling
    if(content.style.maxHeight){
      content.style.maxHeight = null
    }else {
      content.style.maxHeight = content.scrollHeight + 'px'
    }

  })
}

textarea = document.querySelector("textarea");
textarea.addEventListener('keyup', e => {
textarea.style.height = "59px"
let scHeight = e.target.scrollHeight;
textarea.style.height = `${scHeight}px`
});

text_area = document.querySelector("#text_area");
text_area.addEventListener('keyup', e => {
text_area.style.height = "59px"
let scHeight = e.target.scrollHeight;
text_area.style.height = `${scHeight}px`
});



//------------------ profile------------------

var srcDefault = ''
$('.custom-input').on('change', function() {
  var input = $(this);
  if(input[0] && input[0].files && input[0].files[0]) {
    if(!input[0].files[0].type.includes("image")) { 
      $('#image').attr('src', srcDefault);
      return false;                                                 
    }
    var reader = new FileReader();
    reader.onload = function (e) {
      $('#image')
        .attr('src', e.target.result);
    };
    reader.readAsDataURL(input[0].files[0]);
  }
});




// vars
let act = document.querySelector('.act');
let result = document.querySelector('.result'),
result_img = document.querySelector('.result_img'),
upload = document.querySelector('#file-input');


// on change show image with crop options
if (upload){
  upload.addEventListener('change', (e) => {
    if (e.target.files.length) {
      // start file reader
      const reader = new FileReader();
      reader.onload = (e)=> {
        if(e.target.result){
          // create new image
          let img = document.createElement('img');
          img.id = 'image_tweet';
          img.src = e.target.result
          // clean result before
          result.innerHTML = '';
          result_img.innerHTML = '';
          // append new image
          result.appendChild(img);

          act.style.opacity = '1' 
        }
      };
      reader.readAsDataURL(e.target.files[0]);
    }
  });
}

function del_img () {
  act.style.opacity = '0'
	result.innerHTML = '';
}

function dddd () {
  document.querySelector('.h').classList.add('active' ? 'noactive' : 'active')
}




// like
$(function() {
  $( "i" ).click(function() {
    $( "i,span" ).toggleClass( "press" );
  });
});


// let isactive_like = true;
// let nums = 0
// function like_add (value,object) {

// i = document.querySelector(`#like${value}`);
// num_like = document.querySelector(`#num${value}`);

// if (isactive_like){
//   nums += 1
//   isactive_like = false
//   num_like.innerHTML = nums
// }

// else {
//   nums -= 1
//   isactive_like = true
//   if (nums === 0){
//     num_like.innerHTML = ''
//   }
//   else num_like.innerHTML = nums
// }}

// ----------------btn_follow--------------

// btn_follow = document.querySelectorAll(".btn_follow");
// for (let btn of btn_follow) {
//   btn.addEventListener('click',function(){
//     if (btn.innerHTML === "Follow"){
//       btn.innerHTML = "Unfollow"
//     }
//     else {
//       btn.innerHTML = "Follow"
//     }
  
//   })

// }



// ----------smile_add----------------------
text_area = document.querySelector('#text_area')
function tw_smile_add (value,object) {
      text_area.value += value
      
  }

function smile_add (value,object) {
    
    textarea.value += value

}


// function bookmark_add(value,object){
//   num_like = document.querySelector(`#bookmark${value}`);
//   if (num_like.style.color === 'black' ){
//     num_like.style.color = "rgb(25, 192, 207)"
//   }
 
//   else {
//     num_like.style.color = "black"
//   }
// }


function darkmode(){
  const body = document.body
  const wasDarkmode = localStorage.getItem('darkmode')==='true'
  console.log('dddd')
  localStorage.setItem('darkmode',!wasDarkmode)
  body.classList.toggle('dark-mode',!wasDarkmode)

}
document.querySelector('.dark').addEventListener('click',darkmode)
function onload(){
document.querySelector('.dark').addEventListener('click',darkmode)
document.body.classList.toggle('dark-mode', localStorage.getItem('darkmode')==='true')
}
document.addEventListener('DOMContentLoaded',onload)

function get_follow(val,object) {
  $.ajax({
      type: "GET",
      url: `/add_follow/${val}`,
      success: function(response) {
          var json = jQuery.parseJSON(response)
          console.log(json.is);
          i = document.querySelector(`#btn_follow_${val}`);    
          console.log(val) 
          if (json.is === true){
              i.innerHTML = 'Unfollow'
          }
          else {
            i.innerHTML = 'Follow'
          }
      },
      error: function(error) {
          console.log(error);
      }
  });
}




function get_len(val,object) {
  $.ajax({
      type: "GET",
      url: `/add_like/${val}`,
  //     data: $('form').serialize(),
  //     type: 'POST',
      success: function(response) {
          var json = jQuery.parseJSON(response)
          // $('#len').html(json.len)
          console.log(json.nums);
          i = document.querySelector(`.like_${val}`);
          num_like = document.querySelector(`.num_like_${val}`);
          if (json.is === true || json.is2 === true){
              i.innerHTML = "&#128420"
          }
          else {
            i.innerHTML = "&#128151"
            // num_like.innerHTML =  json.nums
          
          }
          if (json.nums != 0) {
            console.log(num_like);
            num_like.innerHTML = json.nums
          }
         
         else num_like.innerHTML =  ''     
      },
      error: function(error) {
          console.log(error);
      }
  });
}