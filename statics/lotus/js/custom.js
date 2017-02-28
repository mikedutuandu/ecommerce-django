jQuery(function () {
    /**
     *  @name  add user
     *  @description list view
     *  @version 1.0
     *  @options
     *    option
     *  @events
     *    event
     *  @methods
     *    init
     */
    (function ($, window, document, undefined) {
        var pluginName = "search";

        // The actual plugin constructor
        function Plugin(element, options) {
            this.element = element;
            this.options = $.extend({}, $.fn[pluginName].defaults, options);
            this.init();
        }

        Plugin.prototype = {
            init: function () {
                var that = this;
                that.search();
            },
            search: function () {
                $('.search-area ul li a.cat-item').click(function(e){
                    e.preventDefault();
                     var text = $(this).html();
                     var catId = $(this).data('cat-id');
                     $('.search-area ul li a.cat-choose span').html(text);
                     $('.search-area .filter-by-cat').val(catId);
                });

                $('.search-button').click(function (e) {
                   e.preventDefault();
                   $('.search-area form').submit();
                });

                if($('.search-area .filter-by-cat').val() != ''){
                    var catId = $('.search-area .filter-by-cat').val();
                    var text = $('.search-area a#'+catId).html();
                    $('.search-area ul li a.cat-choose span').html(text);
                }
            }
        };

        $.fn[pluginName] = function (options) {
            return this.each(function () {
                if (!$.data(this, pluginName)) {
                    $.data(this, pluginName,
                        new Plugin(this, options));
                }
            });
        };
        $.fn[pluginName].defaults = {
            propertyName: 1
        };
        $(function () {
            $('[data-' + pluginName + ']')[pluginName]();
        });

    })(jQuery, window, document);


     /**
     *  @name  add user
     *  @description list view
     *  @version 1.0
     *  @options
     *    option
     *  @events
     *    event
     *  @methods
     *    init
     */
    (function ($, window, document, undefined) {
        var pluginName = "cart";

        // The actual plugin constructor
        function Plugin(element, options) {
            this.element = element;
            this.options = $.extend({}, $.fn[pluginName].defaults, options);
            this.init();
        }

        Plugin.prototype = {
            init: function () {
                var that = this;
                that.addCart();
                that.quantity();
            },
            addCart: function () {
                $('.quantity-container a.btn-primary').click(function(e){
                    e.preventDefault();
                    $('form#add-form').submit()
                });
            },
            quantity: function(){
                $('.cart-quantity .plus i').click(function () {
                    var currentQuantity = $('.cart-quantity .qty').val();
                    $('.cart-quantity .qty').val(parseInt(currentQuantity) + 1);
                });
                $('.cart-quantity .minus i').click(function () {
                    var currentQuantity = $('.cart-quantity .qty').val();
                    if(currentQuantity >1){
                        $('.cart-quantity .qty').val(parseInt(currentQuantity) - 1);
                    }
                });
                $('.qty').keypress(function(event) {
                  if ((event.which != 46 || $(this).val().indexOf('.') != -1) && (event.which < 48 || event.which > 57)) {
                    event.preventDefault();
                  }
                });

            }



        };

        $.fn[pluginName] = function (options) {
            return this.each(function () {
                if (!$.data(this, pluginName)) {
                    $.data(this, pluginName,
                        new Plugin(this, options));
                }
            });
        };
        $.fn[pluginName].defaults = {
            propertyName: 1
        };
        $(function () {
            $('[data-' + pluginName + ']')[pluginName]();
        });

    })(jQuery, window, document);

});