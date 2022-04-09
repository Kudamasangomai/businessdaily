   from paynow import Paynow

   
    paynow = Paynow(
    '13395', 
    '9c3c1ded-6b1d-4081-abfe-2c2033cf18f6',
    #'13396',
    #'af269a2d-c734-4a6a-aa2a-c96aa73fb4d3'
    'http://google.com', 
    'http://google.com'
    )
    payment = paynow.create_payment('Order', 'test@example.com')
    payment.add('Payment for stuff', 1)
    response = paynow.send_mobile(payment, '0777777777', 'ecocash')
    if(response.success):
        poll_url = response.poll_url
        print("Poll Url: ", poll_url)
        status = paynow.check_transaction_status(poll_url)
        time.sleep(30)
        print("Payment Status: ", status.status)