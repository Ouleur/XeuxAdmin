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