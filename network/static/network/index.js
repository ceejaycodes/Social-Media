
const lkbtn = document.querySelectorAll(".likebtn");
const editbtn = document.querySelectorAll(".editable");
const parent = document.querySelector('#edit');
const submitbtn = document.querySelector("#submitt");





document.addEventListener('DOMContentLoaded', function(){

document.querySelector('#root').style.display = 'block';
document.querySelector('#edit').style.display = 'none';






like_post();

edit_post();

sub_post();



});

async function like_post(){

  lkbtn.forEach(e => e.addEventListener('click', ()=>{
    const current = document.querySelector(`#c${e.id}`);
     if (e.dataset.like == 'true'){
    const new_val = parseInt(current.innerHTML) - 1;
    current.innerHTML = new_val
      e.dataset.like = 'false'
      e.src = "static/network/liken.svg"
       fetch(`/viewpost/${e.id}`, {
        method: 'PUT',
        body: JSON.stringify({
                liked_by : 'false'
           })
         })




    }
    else{
      const new_val = parseInt(current.innerHTML) + 1;
      current.innerHTML = new_val
      e.dataset.like = 'true'
      e.src = "static/network/like.svg"
     fetch(`/viewpost/${e.id}`, {
        method: 'PUT',
        body: JSON.stringify({
                liked_by : 'true'
           })
         })


    }
  }
  ))
};


function edit_post(){
editbtn.forEach(e => {e.addEventListener('click', ()=>{

document.querySelector('#edtfrm').innerHTML = e.dataset.post;
document.querySelector('#submitt').setAttribute('id', e.id)
document.querySelector('#root').style.display = 'none';
parent.style.display = 'block';
     

})

})

  
}


function sub_post(){
submitbtn.addEventListener('click', ()=>{
  fetch(`/viewpost/${submitbtn.id}`, {
    method: 'PUT',
    body: JSON.stringify({
            post : document.querySelector('#edtfrm').value
       })
     })
document.querySelector('#root').style.display = 'block';
document.querySelector('#edit').style.display = 'none';
  });


};