
$(".agence").on("change",function(){
    fetch("/change_service/"+$(this).val()).then(function(response){
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
    $("#update_form").attr("action","/update_offre/"+data[0])
})

var offre_id=0;
// Delete Offre
$(".delete_item").on('click',function(){
    offre_id = $(this).data("id");
});

$(".delete_valide").on("click", function(){
    fetch("/del_offre/"+offre_id).then(function(response){
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
    fetch("/achat_offre/"+payement).then(function(response){
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
    fetch("/annuler_offre/"+achat_id).then(function(response){
        location.reload(); 
    });
});


// accept achat
var achat_id = 0;

$(".valid_item").on('click',function(){
    achat_id = $(this).data("id");
});

$(".valid_valide").on("click", function(){
    fetch("/valider_offre/"+achat_id).then(function(response){
        location.reload(); 
    });
});


var btncopy = document.querySelector('.js-copy');
if(btncopy) {
    btncopy.addEventListener('click', docopy);
}

function docopy() {
    // Cible de l'élément qui doit être copié
    var target = this.dataset.target;
    var fromElement = document.querySelector(target);
    if(!fromElement) return;

    // Sélection des caractères concernés
    var range = document.createRange();
    var selection = window.getSelection();
    range.selectNode(fromElement);
    selection.removeAllRanges();
    selection.addRange(range);

    try {
        // Exécution de la commande de copie
        var result = document.execCommand('copy');
        if (result) {
            // La copie a réussi
            this.setAttribute("title","Lien copié !");
            
        }
    }
    catch(err) {
        // Une erreur est surevnue lors de la tentative de copie
        alert(err);
    }

    // Fin de l'opération
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