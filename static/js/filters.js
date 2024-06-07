$(document).ready(function() {
    $('.product-list-main-filters-checkbox-genre').change(function() {
        updateProducts();
    });

    $('.product-list-main-filters-price').change(function() {
        updateProducts();
    });

    $('.product-list-main-filters-checkbox-source').change(function() {
        $('.product-list-main-filters-checkbox-source:checked').not(this).prop('checked', false);
        updateProducts();
    });

    function updateProducts() {
        var selected_genres = [];
        var selected_source = $('input[name="source"]:checked').val();

        var minPrice = $('input[name="min_price"]').val();
        var maxPrice = $('input[name="max_price"]').val();

        minPrice = minPrice.replace(/[^0-9]/g, '');
        maxPrice = maxPrice.replace(/[^0-9]/g, '');

        if (isNaN(minPrice) == true) {
            minPrice = 0;
        }

        if (isNaN(maxPrice) == true || maxPrice < minPrice) {
            maxPrice = minPrice;
        }

        $('input[name="min_price"]').val(minPrice);
        $('input[name="max_price"]').val(maxPrice);

        // Получаем текущий URL
        var currentUrl = window.location.href;

        var urlObject = new URL(currentUrl);

        // Извлекаем слаг категории из URL
        var pathSegments = urlObject.pathname.split('/');
        var categorySlug = pathSegments[2];

        $('input[name="genre"]:checked').each(function() {
            selected_genres.push($(this).val());
        });

        $.ajax({
            url: '/catalog/dynamic-filters/',
            type: 'GET',
            data: {
                'genres[]': selected_genres,
                'source': selected_source,
                'category_slug': categorySlug,
                'min_price': minPrice,
                'max_price': maxPrice,
            },
            success: function(response) {
                // Обновляем содержимое страницы с помощью полученных данных
                var productsHtml = '';
                if (response.products.length == 0) {
                    productsHtml += `
                    <div class="no-items-ajax">
                        <p class="no-items-text">Не найдено ни одного товара, доступного для заказа</p>
                    </div>
                    `
                }
                else {
                    response.products.forEach(function(product) {
                        productsHtml += `
                            <div class="product-list-main-row-products-grid-item">
                                <a href="${product.absolute_url}">
                                    <img class="product-list-main-row-products-grid-item-img" src="${product.image}" alt="Logo">
                                    <a class="product-list-main-row-products-grid-item-name" href="${product.absolute_url}">${product.name}</a>`;

                        if (product.discount) {
                            productsHtml += `
                                    <div class="prices">
                                        <p class="product-list-main-row-products-grid-item-price-sale">${product.price} ₽</p>
                                        <p class="product-list-main-row-products-grid-item-price-through">${product.price_discount} ₽</p>
                                    </div>`;
                        } else {
                            productsHtml += `
                                    <p class="product-list-main-row-products-grid-item-price">${product.price} ₽</p>`;
                        }

                        productsHtml += `
                                    <a class="product-list-main-row-products-grid-item-btn" href="#">В корзину</a>
                                </a>
                            </div>`;
                    });
                }
                $('.product-list-main-row-products-grid').html(productsHtml);
            }
        });
    }
});