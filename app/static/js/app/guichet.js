url = $("#container_cont").data('url').split("||");

// TICKET_VIEW
$("body").delegate('.ticket_view','click',function(){
    $("#numero-t").html($(this).data("id").split(":")[1]);
    $("#numero-t").attr("data-id",$(this).data("id").split(":")[0]);
    // $("#sidebarToggleTop").click()
});

$("body").delegate('.item-action','click',function(){
    $("#sidebarToggleTop").click()
});


// SUIVANT
$(".suivant").on('click',function(){
    fetch(url[1]+"/next_ticket"+"/"+$("#nb-ticket").attr("data-id")).then(function(response){
        response.json().then(function(data){
            $("#numero-t").html(data.ticket[0].servstr+""+data.ticket[0].numero);
            $("#numero-t").attr("data-id",data.ticket[0].id);
        });
        
    });
})

// APPEL
$(".appel").on('click',function(){
    fetch(url[1]+"/call_ticket/"+$("#numero-t").attr("data-id")+"/"+$("#nb-ticket").attr("data-id")).then(function(response){});
    // $("#numero-t").html($(this).data("id").split(":")[1]);
})

// RAPPEL
$(".rappel").on('click',function(){
    fetch(url[1]+"/recall_ticket/"+$("#numero-t").attr("data-id")+"/"+$("#nb-ticket").attr("data-id")).then(function(response){});
    $("#numero-t").html($(this).data("id").split(":")[1]);
})

// TRANSFERT
$(".transfert").on('click',function(){
    fetch(url[1]+"/transfert_ticket/"+$("#numero-t").attr("data-id")).then(function(response){});
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

function tickets_list(){
    url_code = window.location.pathname.split('/');
    const eventSource = new EventSource(url[0]+"/.well-known/mercure?topic=https://example.com/tickets/"+url_code[3]+"/"+url_code[4]);
    eventSource.onmessage = ({ data }) => {
        console.log(JSON.parse(data));
        var ticket =JSON.parse(data)
        tic= '<div class="ticket-item col-12">';
        tic+= '<div class="row">';
        tic+= '<div class="item-info col-8">N '+ticket.servstr+''+ticket.numero+'</div>';
        tic+= '<div class="item-action_min col-4"><i class="fas fa-eye fa-2x text-gray-300 ticket_view" data-id="'+ticket.id+':'+ticket.servstr+''+ticket.numero+'"></i></div>';
        tic+= '<div class="item-action col-4"><i class="fas fa-eye fa-2x text-gray-300 ticket_view" data-id="'+ticket.id+':'+ticket.servstr+''+ticket.numero+'"></i></div>';
        tic+= '</div>';
        tic+= '</div>';
        $("#ticket-list").append(tic);
    };
}

tickets_list();