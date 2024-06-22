$(document).ready(function() {
    $('.cart-row-left-item-right-count').change(function() {
            var amount_not_filter = $(this).val();
            amount = parseInt(amount_not_filter.replace(/[^0-9]/g, ''));

            if (isNaN(amount) == true) {
                amount = 1;
            }

            $(this).val(amount)

            var cartRow = $(this).closest('.cart-row');
            var cart_pk = cartRow.find('.cart-row-left-item-left-name').attr('id');

            $.ajax({
                url: '/accounts/cart_change/',
                type: 'GET',
                data: {
                    'amount': amount,
                    'cart_pk': cart_pk,
                },
                success: function(response) {
                    $('#all_products_price').text(response.all_products_price + " ₽")
                    $('#all_products_sale').text("- " + response.all_products_sale + " ₽")
                    $('#all_products_price_discounted').text(response.all_products_price_discounted + " ₽")
                    cartRow.find('#total_price_not_sale').text(response.total_price_not_sale + " ₽")
                    cartRow.find('#total_price_sale').text(response.total_price_sale + " ₽")
                },
            });
    });
});