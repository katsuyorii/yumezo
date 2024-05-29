$(document).ready(function() {
    $('.product-detail-stars-forever-link, .product-detail-stars-forever-link-red').click(function(event) {
        event.preventDefault(); 

        var link = $(this); 

        $.ajax({
            url: link.attr('href'),
            type: 'GET',
            success: function(response) {
                link.css('color', response.button_color); 
                link.text(response.button_text)
                $('#forever').attr('src', response.new_img);
            },
        });
    });
});
