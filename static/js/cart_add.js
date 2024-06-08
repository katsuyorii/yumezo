$(document).ready(function() {
    $('.main-hits-row-card-btn, .product-list-main-row-products-grid-item-btn, .product-detail-main-right-btn').click(function(event) {
        event.preventDefault();

        var link = $(this);

        $.ajax({
            url: link.attr('href'),
            type: 'GET', 
            success: function(response) {
                link.css('background-color', response.button_color);
                link.text(response.button_text)
            },
            error: function(xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    });
});
