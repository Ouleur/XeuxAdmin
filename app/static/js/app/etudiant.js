$(document).ready(function(e){
  $("#dataTableControle").dataTable({
    destroy : true,
    responsive: true,
    dom: 'Bfrtip',
    fixedHeader: true,
    buttons: [
        'excel'
    ],
    paging: false
 });
    let date = document.querySelector('input[name=date_naissance_edit]').value
  //   result = date.split('/')
  //   console.log(result)
  // document.querySelector('input[name=date_edit]').defaultValue = `${result[2]}-${result[1]}-${result[0]}`
  document.querySelector('input[name=date_edit]').defaultValue = date
})

if(document.querySelector('input[name=date_edit]')){
  document.querySelector('input[name=date_edit]').addEventListener('change',function(e){
      let date = e.target.value
      result = date.split('-')
      document.querySelector('input[name=date_naissance_edit]').defaultValue = `${result[0].trim()}`
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

  $(".photo-btn").click(function () {
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



infos_check_et = document.querySelector('#etudiant_check_infos')


if(infos_check_et){
  infos_check_et.addEventListener('submit', async function(e){
        e.preventDefault()
    
        data = new FormData(this)
    
        const response = await fetch('/etudiant/etudiant_check_infos',{
            method : 'POST',
            body : data
        })
        const json = await response.json()
    
        if(response.ok){
            window.location.href = '/etudiant/check_result'
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
    $("#nombre_present").html(eval($("#nombre_present").html())+1)

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
    }).DataTable({
      destroy : true,
      responsive: true,
      dom: 'Bfrtip',
      fixedHeader: true,
      buttons: [
          'excel'
      ],
    paging: false
  });

  var date = document.getElementById('date');

  function checkValue(str, max) {
    if (str.charAt(0) !== '0' || str == '00') {
      var num = parseInt(str);
      if (isNaN(num) || num <= 0 || num > max) num = 1;
      str = num > parseInt(max.toString().charAt(0)) && num.toString().length == 1 ? '0' + num : num.toString();
    };
    return str;
  };
  
  date.addEventListener('input', function(e) {
    this.type = 'text';
    var input = this.value;
    if (/\D\/$/.test(input)) input = input.substr(0, input.length - 3);
    var values = input.split('/').map(function(v) {
      return v.replace(/\D/g, '')
    });
    if (values[0]) values[0] = checkValue(values[0], 31);
    if (values[1]) values[1] = checkValue(values[1], 12);
    var output = values.map(function(v, i) {
      return v.length == 2 && i < 2 ? v + '/' : v;
    });
    this.value = output.join('').substr(0, 10);
  });
  
  date.addEventListener('blur', function(e) {
    this.type = 'text';
    var input = this.value;
    var values = input.split('/').map(function(v, i) {
      return v.replace(/\D/g, '')
    });
    var output = '';
    
    if (values.length == 3) {
      var year = values[2].length !== 4 ? parseInt(values[2]) + 2000 : parseInt(values[2]);
      var month = parseInt(values[1]) - 1;
      var day = parseInt(values[0]);
      var d = new Date(year, month, day);
      if (!isNaN(d)) {
        document.getElementById('result').innerText = d.toString();
        var dates = [ d.getDate(), d.getMonth() + 1, d.getFullYear()];
        output = dates.map(function(v) {
          v = v.toString();
          return v.length == 1 ? '0' + v : v;
        }).join('/');
      };
    };
    this.value = output;
  });
  
  