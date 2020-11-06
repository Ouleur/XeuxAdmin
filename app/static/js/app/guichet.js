// TICKET_VIEW
$(".ticket_view").on('click',function(){
    $("#numero-t").html($(this).data("id").split(":")[1]);
    $("#numero-t").attr("data-id",$(this).data("id").split(":")[0]);
    // $("#sidebarToggleTop").click()
});


// SUIVANT
$(".suivant").on('click',function(){
    fetch("/next_ticket"+"/"+$("#nb-ticket").attr("data-id")).then(function(response){
        response.json().then(function(data){
            $("#numero-t").html(data.ticket[0].servstr+""+data.ticket[0].numero);
            $("#numero-t").attr("data-id",data.ticket[0].id);
        });
        
    });
})

// APPEL
$(".appel").on('click',function(){
    fetch("/call_ticket/"+$("#numero-t").attr("data-id")+"/"+$("#nb-ticket").attr("data-id")).then(function(response){});
    // $("#numero-t").html($(this).data("id").split(":")[1]);
})

// RAPPEL
$(".rappel").on('click',function(){
    fetch("/recall_ticket/"+$("#numero-t").attr("data-id")+"/"+$("#nb-ticket").attr("data-id")).then(function(response){});
    $("#numero-t").html($(this).data("id").split(":")[1]);
})

// TRANSFERT
$(".transfert").on('click',function(){
    fetch("/transfert_ticket/"+$("#numero-t").attr("data-id")).then(function(response){});
    $("#numero-t").html($(this).data("id").split(":")[1]);
})

// DEBUTER
$(".debuter").on('click',function(){
    $("#numero-t").html($(this).data("id").split(":")[1]);
})

// FERMER
$(".fermer").on('click',function(){
    $("#numero-t").html($(this).data("id").split(":")[1]);
})

//Resize
function quarter() {
    window.resizeTo(
      window.screen.availWidth / 2,
      window.screen.availHeight / 2
    );
  }

quarter();