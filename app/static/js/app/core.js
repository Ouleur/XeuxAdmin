if ( window.history.replaceState ) {
    window.history.replaceState( null, null, window.location.href );
  }


  
  
$(".agence").on("change",function(){
    fetch("/xeux/change_service/"+$(this).val()).then(function(response){
        response.json().then(function(data){
            options = '';
            for(service of data.services ){

                options +='<option value="'+service.id+'">'+service.denomination+'</option>';
            }
            $(".service").html(options);
        });
        
    });
})



// Update offre
$(".update_offre").on('click',function(){
    data = $(this).data("offre").split(":");
    $("#update_form #titre").val(data[1]);
    $("#update_form #prix").val(data[2]);
    $("#update_form #temps").val(data[3]);
    $("#update_form #description").val(data[4]);
    $("#update_form").attr("action","/pozy/update_offre/"+data[0])
})

var offre_id=0;
// Delete Offre
$(".delete_item").on('click',function(){
    offre_id = $(this).data("id");
});

$(".delete_valide").on("click", function(){
    fetch("/xeux/del_offre/"+offre_id).then(function(response){
        location.reload(); 
    });
});


// Payement
var payement = 0;
$(".offre").on("click", function(){
    data = $(this).data("offre").split(":");
    $(".titre").html(data[1]);
    $(".prix").html(data[2] +" Fcfa");
    $(".temps").html(data[3] +" Jours");
    $(".description").html(data[4]);
    payement = data[0];
})

$(".achat").on("click", function(){
    fetch("/xeux/achat_offre/"+payement).then(function(response){
        payement = 0 ;
        location.reload(); 
    });
})


// Delete achat
var achat_id = 0;

$(".cancel_item").on('click',function(){
    achat_id = $(this).data("id");
});

$(".cancel_valide").on("click", function(){
    fetch("/xeux/annuler_offre/"+achat_id).then(function(response){
        location.reload(); 
    });
});


// accept achat
var achat_id = 0;

$(".valid_item").on('click',function(){
    achat_id = $(this).data("id");
});

$(".valid_valide").on("click", function(){
    fetch("/xeux/valider_offre/"+achat_id).then(function(response){
        location.reload(); 
    });
});


var btncopy = document.querySelector('.js-copy');
if(btncopy) {
    btncopy.addEventListener('click', docopy);
}

function docopy() {
    // Cible de l'??l??ment qui doit ??tre copi??
    var target = this.dataset.target;
    var fromElement = document.querySelector(target);
    if(!fromElement) return;

    // S??lection des caract??res concern??s
    var range = document.createRange();
    var selection = window.getSelection();
    range.selectNode(fromElement);
    selection.removeAllRanges();
    selection.addRange(range);

    try {
        // Ex??cution de la commande de copie
        var result = document.execCommand('copy');
        if (result) {
            // La copie a r??ussi
            this.setAttribute("title","Lien copi?? !");
            
        }
    }
    catch(err) {
        // Une erreur est surevnue lors de la tentative de copie
        alert(err);
    }

    // Fin de l'op??ration
    selection = window.getSelection();
    if (typeof selection.removeRange === 'function') {
        selection.removeRange(range);
    } else if (typeof selection.removeAllRanges === 'function') {
        selection.removeAllRanges();
    }
}


$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();   
  });
  
var qr;


function preview_image(event) 
{
    var reader = new FileReader();
    reader.onload = function()
    {
        var output = document.getElementById('output_image');
        output.src = reader.result;
    }
    reader.readAsDataURL(event.target.files[0]);
}

$("#output_image").click(function(){
    $("#file").click()
});


// Qr code 

$(".ke??-qrcode").click(function(){
    generateQRCode($(this).data("qrhash"));
})

var qr;
(function() {
    qr = new QRious({
        element: document.getElementById('qr-code'),
        size: 200,
        value: 'Vit app'
    });
})();


function generateQRCode(qrtext) {
    qr.set({
        foreground: 'black',
        size: 200,
        value: qrtext
    });
}

// Modifier un etudiant
function ShowEtudiant(id){
    fetch("/xeux/read_etudiant/"+id).then(function(response){
        response.json().then(function(data){
            console.log(data); 
            $("#matricule").val(data.matricule);
            $("#nom").val(data.nom);
            $("#prenoms").val(data.prenoms);
            $("#id_carte").val(data.card_id);
            $("#filiere").val(data.filiere_id);
            $("#niveau").val(data.niveau);
            $("#id").val(data.id);
            
        });
    });
}
function deleteEtudiant(id){
    

      Swal.fire({
        title: 'Etes vous s??re ?',
        text: "Vous ne pourriez plus revenir en arri??re  !",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Oui, effectuer la suppression!'
      }).then((result) => {
        if (result.isConfirmed) {
            fetch("/xeux/delete_etudiant/"+id).then(function(response){
                Swal.fire(
                    'Supprim?? !',
                    'L\'enregistrement a bien ??t??  Supprim?? .',
                    'success'
                  )
            });
          
        }
      })
    
}


function deleteFiliere(id){
    Swal.fire({
      title: 'Etes vous s??re ?',
      text: "Vous ne pourriez plus revenir en arri??re  !",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Oui, effectuer la suppression!'
    }).then((result) => {
      if (result.isConfirmed) {
          fetch("/xeux/delete_filiere/"+id).then(function(response){
              Swal.fire(
                  'Supprim?? !',
                  'L\'enregistrement a bien ??t??  Supprim?? .',
                  'success'
                )
          });
        
      }
    })
  
}


function deleteMatiere(id){
    Swal.fire({
      title: 'Etes vous s??re ?',
      text: "Vous ne pourriez plus revenir en arri??re  !",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Oui, effectuer la suppression!'
    }).then((result) => {
      if (result.isConfirmed) {
          fetch("/xeux/delete_matiere/"+id).then(function(response){
              Swal.fire(
                  'Supprim?? !',
                  'L\'enregistrement a bien ??t??  Supprim?? .',
                  'success'
                )
          });
        
      }
    })
  
}

// Modifier un equipement
function ShowEquipements(id){
    fetch("/xeux/read_device/"+id).then(function(response){
        response.json().then(function(data){
            console.log(data); 
            $("#denomination").val(data.denomination);
            $("#position").val(data.position);
            $("#emei").val(data.emei);
            $("#status").val(data.status);
            $("#id").val(data.id);
            
        });
    });
}
function deleteEquipement(id){
    

      Swal.fire({
        title: 'Etes vous s??re ?',
        text: "Vous ne pourriez plus revenir en arri??re  !",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Oui, effectuer la suppression!'
      }).then((result) => {
        if (result.isConfirmed) {
            fetch("/xeux/delete_device/"+id).then(function(response){
                Swal.fire(
                    'Supprim?? !',
                    'L\'enregistrement a bien ??t??  Supprim?? .',
                    'Success'
                  )
            });
          
        }
      })
    
}


function init(){
    

    Swal.fire({
      title: 'Etes vous s??re ?',
      text: "Vous ne pourriez plus revenir en arri??re  !",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Oui, effectuer la suppression!'
    }).then((result) => {
      if (result.isConfirmed) {
          fetch("/xeux/init").then(function(response){
              Swal.fire(
                  'Supprim?? !',
                  'L\'enregistrement a bien ??t??  Supprim?? .',
                  'Success'
                )
          });
        
      }
    })
  
}



$(document).ready(async function(){

    $("#dataTableEtudiants").dataTable({
        language : {
            "info": "page _PAGE_ sur _PAGES_",
        },
        'ajax' : '/etudiant/api',
        buttons: [
            'excel', 'csv'
        ]
    })

     $("#dataTablePresence").dataTable({
        destroy : true,
        responsive: true,
        buttons: [
            'excel', 'csv'
        ]
     });

        
    
})

 

$("#formPresence").on('submit',async function(e){
    e.preventDefault()

    
    data = new FormData(this)
    console.log(data.get('date_debut').split('-'))

    

    let response = await fetch('/presence',{
        method : 'POST',
        body : data
    })
    json = await response.json()

    if(response.ok){
        
        $("#dataTablePresence").DataTable().destroy()
        document.querySelector('#dataTablePresence').innerHTML = ''
        

        $("#dataTablePresence").dataTable({
           destroy : true,
           data : json.data,
           buttons: [
            'excel', 'csv'
            ],
           columns: json.columns,
       })
       
       
    } else {
        document.querySelector('#error_data').textContent = json.message
        document.querySelector('.alert-warning').style.display = 'block'
        
        setTimeout(()=>{
            document.querySelector('.alert-warning').style.display = 'none'
        }, 3000)
    }
   
   
    
})


$('#dataTablePresence')
    
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






