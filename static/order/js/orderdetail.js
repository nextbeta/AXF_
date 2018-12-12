$(function () {
    $('.orderdetail').width(innerWidth)

    $('#pay').click(function () {
        var identifier = $(this).attr('identifier')
        $.get('/axf/pay/', {'identifier':identifier}, function (response) {
            console.log(response)
            if (response.status){
                window.open(response.alipay_url, target='_self')
            }
        })
    })
})