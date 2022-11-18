console.log("cartHelper found")

$(document).ready(function(){
    console.log("doc ready, jQuery working")

    

    $('.checkUserState').click(function(){

        // check cookie
        if (Cookies.get('user')){

            $('.add0')[0].classList.remove("hideThis")

            // found cookie, tell server to send items to person trough json
            console.log('I found ' + Cookies.get('user'))

            $.ajax({
                type:'POST',
                url: '/cartHelper/0',                    // check users then return items
                data:{
                    usrName: Cookies.get('user'),         
                    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
                },
                success: function(serverResponse){      //items
                    console.log(serverResponse)
                    
                    $('.add0')[0].classList.remove("hideThis")
                    $('.cleaner').remove();

                    for(var i = 0 ; i < serverResponse.names.length ; i++ ){
                        $('.append').append(
                           
                            '<a class="dropdown-item cleaner " ><h5><h6>'+
                            serverResponse.names[i]+'<br>Pack off '+
                            serverResponse.quantity[i]+' @ R'+
                            serverResponse.price[i]+' X '+
                            serverResponse.count[i]+'</h6></h5></a> '
                        )
                    }
                }
            }); 

        } else {
            
            // no cookie found, tell server to show sign up
            // $('.add0')[0].classList.add("hideThis")
            // $('.cleaner').remove();
            $('.add1')[0].classList.remove("hideThis")


        }
        // make cookie after sign up
        // Cookies.remove('name')
        // Cookies.set('user', 'someone')

    })

    $('.deleteItm').click(function(event){
        event.preventDefault();
        
        console.log(this.getAttribute('id'))
        console.log("ahh. . . lol")

        // $.ajax({
        //     type:'POST',
        //     url: '/cartHelper/0',                    // check users then return items
        //     data:{
        //         usrName: Cookies.get('user'),         
        //         csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
        //     },
        //     success: function(serverResponse){      //items
        //     }
        // }); 
    })

    $("#nw").click(function(event){
        event.preventDefault();
        console.log("Submitting form from new")

        $.ajax({
            type:'POST',
            url: '/nwuser',
            data:{
                usNm:$('#usN').val(),
                usPw:$('#psW').val(),
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(serverResponse){
                console.log(serverResponse)
                if(serverResponse.state){
                    console.log("You tried to make a new user and it didnt work out. . . 🤷‍♀️🤷‍♀️🤷‍♀️")
                    alert('The user name already exits, please use another name')

                }else if(serverResponse) {
                console.log("gonna make a cookie")
                    $('.add1')[0].classList.add("hideThis")
                    $('.cleaner').remove();
    
                    $('.add0')[0].classList.remove("hideThis")
                    $('.cleaner').remove();
    
                    for(var i = 0 ; i < serverResponse.names.length ; i++ ){
                        $('.append')
                        .append(
                            '<a class="dropdown-item cleaner " ><h5><h6>'+
                            serverResponse.names[i]+'<br>Pack off '+
                            serverResponse.quantity[i]+' @ R'+
                            serverResponse.price[i]+' X '+
                            serverResponse.count[i]+' </h6></h5></a>'
                        )
                    }
                    Cookies.set('user', serverResponse.user)
                }
            }
        });


    })

    $("#userForm").submit(function(event) {
        event.preventDefault();
        console.log("Submitting form")

        $.ajax({
            type:'POST',
            url: '/cartHelper/1',
            data:{
                usNm:$('#usN').val(),
                usPw:$('#psW').val(),
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(serverResponse){
                console.log("sent post")

                if(serverResponse.notfound){
                    console.log("You tried to sign in and it didnt work out. . .🤷‍♀️🤷‍♀️")
                    alert("Are you sure you exist?. . . just saying 👀")

                }else if(serverResponse) {
                    console.log("gonna make a cookie")
                    $('.add1')[0].classList.add("hideThis")
                    $('.cleaner').remove();
    
                    $('.add0')[0].classList.remove("hideThis")
                    $('.cleaner').remove();
    
                    for(var i = 0 ; i < serverResponse.names.length ; i++ ){
                        $('.append')
                        .append(
                            '<a class="dropdown-item cleaner " ><h5><h6>'+
                            serverResponse.names[i]+'<br>Pack off '+
                            serverResponse.quantity[i]+' @ R'+
                            serverResponse.price[i]+' X '+
                            serverResponse.count[i]+' </h6></h5></a>'
                        )
                    }
                    
                    Cookies.set('user', serverResponse.user)
                }
            }
        });
    });

    $('.deleteMe').click(function(event){

        Cookies.remove('user')

    })
    

    $('.addMeToCart').click(function(event){
        event.preventDefault();

        console.log(this.getAttribute('id'))

        if(Cookies.get('user')){

            $.ajax({
                type:'POST',
                url: this.getAttribute('id'),
                data:{
                    usrName: Cookies.get('user'),  
                    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
                },
                success: function(serverResponse){
                    console.log("sent post item")
                    console.log(serverResponse.state)

                }
            });
        }else{

            console.log('please log')
        }
    })


    $( "#test" ).submit(function( event ) {
        event.preventDefault();

        console.log("submit clicked")

        $.ajax({
            type:'POST',
            url: '/cartHelper',
            data:{
                here:$('#here').val(),
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(serverResponse){
                console.log("sent post")
                console.log(serverResponse.data.fuc)
                $('#returnTest').append('<li>'+serverResponse.data.fuc+'</li>')
            }
        });

      });

});