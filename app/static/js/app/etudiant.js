$(document).ready(function(e){
  $("#dataTableControle").dataTable({
    destroy : true,
    responsive: true,
    dom: 'Bfrtip',
    buttons: [
         'excel'
    ],
    paging: false
 });
    let date = document.querySelector('input[name=date_naissance_edit]').value
    result = date.split('/')
    console.log(result)
  document.querySelector('input[name=date_edit]').defaultValue = `${result[2]}-${result[1]}-${result[0]}`
})

if(document.querySelector('input[name=date_edit]')){
  document.querySelector('input[name=date_edit]').addEventListener('change',function(e){
      let date = e.target.value
      result = date.split('-')
      document.querySelector('input[name=date_naissance_edit]').defaultValue = `${result[2]}/${result[1]}/${result[0]}`
    })
}
var photo;
  
  $('#image').on('input', function () {
    var file = this.files[0];
    var reader = new FileReader();

    reader.onloadend = function (e) {
      $('#avatar').attr('src', reader.result)
      photo = reader.result;
      // alert(reader.result)
    }
      console.log(reader.readAsDataURL(file))


    reader.readAsDataURL(file);
  });

  $("#avatar").click(function () {
    document.getElementById('image').click();
  });

  infos_et = document.querySelector('#etudiant_infos')


if(infos_et){
    infos_et.addEventListener('submit', async function(e){
        e.preventDefault()
    
        data = new FormData(this)
    
        const response = await fetch('/etudiant/infos',{
            method : 'POST',
            body : data
        })
        const json = await response.json()
    
        if(response.ok){
            window.location.href = '/etudiant/result'
        } else{
            document.querySelector('#error_etudiant').style.display = 'block'
        }
    })
    
}




$(".tr_controle").on('click', function(e){
  $("#controleModal").modal({
    show : true
  })
  let matricule = this.dataset.matricule
  this.classList.add('active')
  $("#Editer_controle").attr('data-matricule', matricule)
  $("#present_controle").attr('data-matricule', matricule)
  $("#absent_controle").attr('data-matricule', matricule)
  console.log(matricule)
  
})

$("#Editer_controle").on('click',  function(e){
    let matricule = this.dataset.matricule
    window.location.href = `/controle/${matricule}`    
})

$("#present_controle").on('click', async function(e){
  let matricule = this.dataset.matricule
  let last = document.querySelector('.tr_controle.active').lastElementChild
  let response = await fetch(`/controle/etat/${matricule}`)
  let json =   await response.json
  
  if(response.ok){
  if(last.textContent == 'ABSENT(E)'){
    last.textContent = 'PRESENT(E)'
    last.classList.remove('abs')
    last.classList.add('pst')
    document.querySelector('.tr_controle.active').classList.remove('active')
  }
   
  }
})

$("#add_controle").on('click',  function(e){
  
  window.location.href = `/controle/etudiant/new`    
})



$('#dataTableControle')
    
    .on('draw.dt', function(){
        children = document.querySelectorAll("table td");

    [...children].forEach(el=>{
        if(el.textContent === 'PRESENT(E)'){
            
            el.classList.add('pst')
        } else if(el.textContent === 'ABSENT(E)') {
            
         el.classList.add('abs')
        }
    })
    }).DataTable()

