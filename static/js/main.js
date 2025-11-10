// KiyaGreen Main JavaScript

$(document).ready(function() {
    // Smooth scrolling for anchor links
    $('a[href^="#"]').on('click', function(event) {
        var target = $(this.getAttribute('href'));
        if (target.length) {
            event.preventDefault();
            $('html, body').stop().animate({
                scrollTop: target.offset().top - 70
            }, 1000);
        }
    });

    // Product search functionality
    $('#product-search').on('keyup', function() {
        var searchText = $(this).val().toLowerCase();
        $('.product-card').each(function() {
            var productName = $(this).find('.card-title').text().toLowerCase();
            var productDesc = $(this).find('.card-text').text().toLowerCase();

            if (productName.includes(searchText) || productDesc.includes(searchText)) {
                $(this).parent().show();
            } else {
                $(this).parent().hide();
            }
        });
    });

    // Category filter
    $('.category-filter').on('click', function(e) {
        e.preventDefault();
        $('.category-filter').removeClass('active');
        $(this).addClass('active');

        var categoryId = $(this).data('category');

        if (categoryId === 'all') {
            $('.product-card').parent().show();
        } else {
            $('.product-card').each(function() {
                var productCategory = $(this).data('category');
                if (productCategory == categoryId) {
                    $(this).parent().show();
                } else {
                    $(this).parent().hide();
                }
            });
        }
    });

    // RFQ Modal - Populate product info
    $('.rfq-modal-trigger').on('click', function() {
        var productId = $(this).data('product-id');
        var productName = $(this).data('product-name');

        $('#rfq-product-id').val(productId);
        $('#rfq-product-name').val(productName);

        // If product name field is readonly, show it to user
        if ($('#product-display').length) {
            $('#product-display').text(productName);
        }
    });

    // Form validation
    $('form').on('submit', function(e) {
        var isValid = true;
        var form = $(this);

        form.find('input[required], textarea[required], select[required]').each(function() {
            if ($(this).val() === '') {
                isValid = false;
                $(this).addClass('is-invalid');
            } else {
                $(this).removeClass('is-invalid');
            }
        });

        // Email validation
        var emailField = form.find('input[type="email"]');
        if (emailField.length) {
            var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(emailField.val())) {
                isValid = false;
                emailField.addClass('is-invalid');
            }
        }

        if (!isValid) {
            e.preventDefault();
            alert('Please fill in all required fields correctly.');
        }
    });

    // Clear validation on input
    $('input, textarea, select').on('input change', function() {
        $(this).removeClass('is-invalid');
    });

    // Product quantity controls
    $('.qty-minus').on('click', function() {
        var input = $(this).siblings('.qty-input');
        var val = parseInt(input.val());
        if (val > 1) {
            input.val(val - 1);
        }
    });

    $('.qty-plus').on('click', function() {
        var input = $(this).siblings('.qty-input');
        var val = parseInt(input.val());
        input.val(val + 1);
    });

    // Image gallery for product detail
    $('.gallery-thumbnail').on('click', function() {
        var newSrc = $(this).attr('src');
        $('#main-product-image').attr('src', newSrc);
        $('.gallery-thumbnail').removeClass('active');
        $(this).addClass('active');
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        $('.alert').fadeOut('slow', function() {
            $(this).remove();
        });
    }, 5000);

    // Navbar scroll effect
    $(window).scroll(function() {
        if ($(this).scrollTop() > 50) {
            $('.navbar').addClass('shadow');
        } else {
            $('.navbar').removeClass('shadow');
        }
    });

    // Animate elements on scroll
    function animateOnScroll() {
        $('.fade-in-up').each(function() {
            var elementTop = $(this).offset().top;
            var elementBottom = elementTop + $(this).outerHeight();
            var viewportTop = $(window).scrollTop();
            var viewportBottom = viewportTop + $(window).height();

            if (elementBottom > viewportTop && elementTop < viewportBottom) {
                $(this).addClass('visible');
            }
        });
    }

    $(window).on('scroll resize', animateOnScroll);
    animateOnScroll(); // Initial check

    // Product autocomplete in RFQ form
    if ($('#product-autocomplete').length) {
        $('#product-autocomplete').on('input', function() {
            var query = $(this).val();
            if (query.length >= 2) {
                $.ajax({
                    url: '/products/search/',
                    data: { q: query },
                    success: function(data) {
                        var resultsHtml = '';
                        data.forEach(function(product) {
                            resultsHtml += '<div class="autocomplete-item" data-id="' + product.id + '">' + product.name + '</div>';
                        });
                        $('#autocomplete-results').html(resultsHtml).show();
                    }
                });
            } else {
                $('#autocomplete-results').hide();
            }
        });

        // Handle autocomplete selection
        $(document).on('click', '.autocomplete-item', function() {
            var productId = $(this).data('id');
            var productName = $(this).text();
            $('#product-autocomplete').val(productName);
            $('#selected-product-id').val(productId);
            $('#autocomplete-results').hide();
        });

        // Hide autocomplete when clicking outside
        $(document).on('click', function(e) {
            if (!$(e.target).closest('#product-autocomplete').length) {
                $('#autocomplete-results').hide();
            }
        });
    }

    // Print functionality for quotes
    $('.print-quote').on('click', function() {
        window.print();
    });

    // Tooltip initialization (Bootstrap 5)
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Console log for debugging
    console.log('KiyaGreen JavaScript loaded successfully!');
});
