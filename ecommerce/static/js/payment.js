$(document).ready(function () {
    

    $('.paywithrazorpay').click(function (e) { 
        e.preventDefault();

        var fname    =$("[name='fname']").val();
        var lname    =$("[name='lname']").val();
        var email   =$("[name='email']").val();
        var pno      =$("[name='pno']").val();
        var address    =$("[name='address']").val();
        var city     =$("[name='city']").val();
        var state    =$("[name='state']").val();
        var pin       =     $("[name='pin']").val();


        if (fname == '' ||lname == '' ||email == '' ||pno == '' ||address == '' ||city == '' ||state == '' ||pin=='')
        {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'ALL FIELDS ARE MANDETORY TO FILL',
                
              })
            return false;
        }
        else{

            var totalprice=$('[name="totalprice"]').val();
            
            var options = {
                "key": "rzp_test_C6v2hwG7iqkEkx", // Enter the Key ID generated from the Dashboard
                "amount": 1*100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                "currency": "INR",
                "name": "Acme Corp", //your business name
                "description": "Test Transaction",
                // "image": "https://example.com/your_logo",
                //"order_id": "order_9A33XWu170gUtm", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                "handler": function (response){
                    alert(response.razorpay_payment_id);

            var data={
                        fname  :fname  , 
                        lname:lname  ,  
                        email :email  , 
                        pno    :pno    ,
                        address:address,
                       city   :city   ,
                        state  :state  ,
                        pin    :pin  ,
                        totalprice:totalprice,
                        paymentmode:'Razorpay',
                        payid:response.razorpay_payment_id ,
                        csrfmiddlewaretoken:"{{csrf_token}}",


                        
                    };
                    console.log(data);


                    $.ajax({
                        method: "POST",
                        url: '/place-order',
                        data: data ,
                        
                        
                        success: function (responsec) {
                          
                           
                          Swal.fire({
                            title: 'Order Placed',
                            text: "Check out the order and its status",
                            icon: 'success',
                            showCancelButton: true,
                            confirmButtonColor: '#3085d6',
                            cancelButtonColor: '#d33',
                            confirmButtonText: 'Yes, View orders'
                          }).then((result) => {
                            if (result.isConfirmed) {
                              window.location.href="/your-orders"
                            }
                          })
                          
                                                        
                                
                              
                        }
                    });
                    console.log('ok');
                    
                },
                "prefill": {
                    "name": fname+''+lname, //your customer's name
                    "email": email,
                    "contact": pno
                },
                
                "theme": {
                    "color": "#3399cc"
                }
            };
            var rzp1 = new Razorpay(options);
            rzp1.on('payment.failed', function (response){
                    alert(response.error.code);
                    alert(response.error.description);
                    alert(response.error.source);
                    alert(response.error.step);
                    alert(response.error.reason);
                    alert(response.error.metadata.order_id);
                    alert(response.error.metadata.payment_id);
            }); 
    
            rzp1.open();

        }

        


        
    });

});