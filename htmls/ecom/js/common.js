(function($) {
    'use strict';

    // Preloader method
    function preloader() {
        var host = $('#preloader');
        var bars = [];
        //create 3 bars
        for (var i = 0; i < 3; i++) {
            var bar = $('<div class="bar"></div>');
            bars.push(bar);
            host.append(bar);
        }
        //Animate bar method
        var barAnimation = function(index) {
            setTimeout(function() {
                setInterval(function() {
                    if (bars[index].hasClass('active')) {
                        bars[index].removeClass('active');
                    } else {
                        bars[index].addClass('active');
                    }
                }, 700);
            }, (index === 0) ? 50 : index * 150 + 50);
        };

        host.prop('class', 'preloader animate');

        setTimeout(function() {
            host.prop('class', 'preloader start animate');
        }, 300);
        setTimeout(function() {
            host.prop('class', 'preloader start complete');
        }, 1100);
        setTimeout(function() {
            for (var b = 0; b < bars.length; b++) {
                barAnimation(b);
            }
        }, 1100);
    }

    // Start preloader
    preloader();

    // MasonryiInitialization
    function masonryUnitOne() {
        var $conmas = $('#unit-one');
        $conmas.imagesLoaded(function() {
            $conmas.masonry({
                columnWidth: ".js-wrap-products",
                itemSelector: '.js-wrap-products',
                percentPosition: true,
                singleMode: false,
                isResizable: true,
                isAnimated: true,
                animationOptions: {
                    queue: false,
                    duration: 500
                }
            });
        });
    }

    // Automaticity subtraction unit width search bar
    function autoWidthHeader() {
        var col_size_search = $("#col-size-search");
        var col_size_buy = $("#col-size-buy");
        var col_size_logo = $("#col-size-logo");
        if ($(window).width() > 1200) {
            col_size_search.width($(".box-1675").width() - col_size_buy.width() - col_size_logo.width() - 4);
            col_size_search.after(col_size_buy.detach());
        } else if ($(window).width() <= 1200) {
            col_size_logo.after(col_size_buy.detach());
        }
    }

    // Positioning block search
    function offsetSearch() {
        var box_search_popup = $("#box-search-popup");
        var col_size_search = $("#col-size-search");
        if ($(window).width() >= 1200) {
            box_search_popup.width(col_size_search.width());
            box_search_popup.offset({ left: col_size_search.offset().left, top: col_size_search.offset().top });
        } else if ($(window).width() < 1200) {
            box_search_popup.width("90%");
            box_search_popup.offset({ left: $("body").width() * 0.035, top: col_size_search.offset().top });
        }
    }

    // Format number
    function formatNumber(num) {
        var number = num + "";
        number = new Array(4 - number.length % 3).join("U") + number;
        return number.replace(/([0-9U]{3})/g, "$1 ").replace(/U/g, "");
    }

    // Get url parametr for tabs Start
    function getUrlParameter(sParam) {
        var sPageURL = decodeURIComponent(window.location.search.substring(1)),
            sURLVariables = sPageURL.split('&'),
            sParameterName,
            i;
        for (i = 0; i < sURLVariables.length; i++) {
            sParameterName = sURLVariables[i].split('=');
            if (sParameterName[0] === sParam) {
                return sParameterName[1] === undefined ? true : sParameterName[1];
            }
        }
    }

    $(document).ready(function() {

        // Hiding blocks when clicked
        $(".delete-cart-product", '#main-blocks-cart').on("click", function() {
            $(this).parent(".block-cart").fadeOut();
            return false;
        });

        $(".delete-cart-product", '#main-blocks-cart-mob').on("click", function() {
            $(this).parent(".block-cart").fadeOut();
            return false;
        });

        $(".js-delete-cart").on("click", function() {
            $(this).parents(".block-personal-wish").fadeOut();
            return false;
        });

        $(".main-wishlist .block-cart table .delete-cart-product").on("click", function() {
            $(this).parents(".block-cart").fadeOut();
            return false;
        });

        $("#js-close-one").on("click", function() {
            $(this).parents("#table-compare").find("td:nth-child(2)").fadeOut();
            return false;
        });

        $("#js-close-two").on("click", function() {
            $(this).parents("#table-compare").find("td:nth-child(3)").fadeOut();
            return false;
        });

        $("#js-close-three").on("click", function() {
            $(this).parents("#table-compare").find("td:nth-child(4)").fadeOut();
            return false;
        });
        $("#js-close-discont").on("click", function() {
            $(".main-discont").fadeOut();
        });
        // Hiding blocks when clicked End

        // Initialization Waves Start
        Waves.attach('.button-small, .button-middle, .button-lardge, .button-info-lardge', ['waves-circle', 'waves-float']);
        Waves.init();

        // Faq Accordion Start
        $(".faq_list").accordion({
            active: false,
            collapsible: true,
            heightStyle: "content"
        });

        // The appearance of the block on the page off with a delay Start
        $("#main-discont").delay(2000).fadeIn();

    });

    $(window).on('load', function() {

        //Hide preloader
        $("#loader").fadeOut();

        // Events in page "My account" Start
        $("#js-edit-profile").on("click", function() {
            $("#account-setting").tabs("option", "active", 0);
            return false;
        });

        $("#js-change-password").on("click", function() {
            $(".js-show-pass").toggleClass("active");
            $(this).hide();
        });

        $("#account-setting").tabs({ "active": getUrlParameter('active_tab') });

        $("#forgot-pass").on("click", function() {
            $("#sign_in_form").css("display", "none");
            $("#forgot_pass_form").css("display", "block");
            return false;
        });

        $("#back-log-in").on("click", function() {
            $("#sign_in_form").css("display", "block");
            $("#forgot_pass_form").css("display", "none");
        });

        $("#js-open-thank").on("click", function() {
            $("#thank_registr").css("display", "block");
        });

        $("#close-account-box").on("click", function() {
            $("#main-account").fadeOut();
            $("body").css("position", "inherit");
            $("#thank_registr").css("display", "none");
        });

        $("#js-account, #js-account-mob").on("click", function() {
            $("body").css("position", "fixed");
            $("#main-account").fadeIn();
            $("#js-open-thank").on("click", function() {
                $("#thank_registr").css("display", "block");
            });
            return false;
        });
        // Events in page "My account" End

        // Initializing Carousel Slider Arrows Start
        var owl = $("#owl-carousel");
        owl.owlCarousel({
            navigation: true,
            navigationText: ['<i class="fa fa-angle-left" aria-hidden="true"></i>', '<i class="fa fa-angle-right" aria-hidden="true"></i>'],
            items: 8,
            itemsDesktop: [1700, 4],
            itemsDesktopSmall: [1200, 4],
            itemsTablet: [992, 3],
            itemsMobile: false,
            addClassActive: true,
            afterInit: function() {
                $(".active").eq(1).addClass('active-border');
                $(".active").eq(8).addClass('active-border-right');
            },
            afterMove: function() {
                //add transform for 2nd active slide
                $(".owl-item").removeClass('active-border');
                $(".owl-item").removeClass('active-border-right');
                $(".active").eq(1).addClass('active-border');
                $(".active").eq(8).addClass('active-border-right');
            }
        });
        // Initializing Carousel Slider Arrows End

        // Filter Results Searched Start
        $("#filter").on("keyup", function() {
            var countWatch = 5;
            // Retrieve the input field text and reset the count to zero
            var filter = $(this).val(),
                countSearch = 0;
            // Loop through the comment list
            var results_search_ul = $("#results-search ul");
            var wrap_see_all_results = $("#wrap-see-all-results");
            for (var i = 0, len = results_search_ul.children(".item").length; i < len; i++) {
                results_search_ul.children(".item").eq(i).hide().removeClass("activebackg bgcolorsearch");
                // If the list item does not contain the text phrase fade it out
                if (results_search_ul.children(".item").eq(i).text().search(new RegExp(filter, "i")) > 0) {
                    results_search_ul.children(".item").eq(i).show().addClass("activebackg");
                    results_search_ul.css("display", "block");
                    countSearch++;
                    // Show the list item if the phrase matches and increase the count by 1
                } else {
                    results_search_ul.children(".item").eq(i).hide().removeClass("activebackg bgcolorsearch");
                }
                if (countSearch > countWatch) {
                    results_search_ul.children(".item").eq(i).hide();
                    wrap_see_all_results.css("display", "block");
                } else {
                    wrap_see_all_results.css("display", "none");
                }
                $(".activebackg:even").addClass("bgcolorsearch");
            }

            // Update the count
            var numberItems = countSearch;
            $("#filter-count").text(countSearch + " ").append("<p>Results Searched</p");
        });
        // Filter Results Searched End

        // Initializing function Start
        autoWidthHeader();
        offsetSearch();
        masonryUnitOne();
        // Initializing function Start

        // Initializing JqueryUI plugins Start
        $("#accordion_cart_product_mob").accordion({
            heightStyle: "content"
        });
        var spinner = $("#spinner").spinner({
            min: 1,
            value: 1
        });
        var cart_name_prodct = $(".box-counter-cart input").spinner({
            min: 1,
            value: 1
        });

        // Tabs Product Start
        $("#tabs_cart_product").tabs();
        // Tabs Product End

        // Tabs Popup Account Start
        $("#tabs_account").tabs();
        // Tabs Popup Account End

        // Initializing JqueryUI plugins End

        // ---------------------------------------------------------------
        var mnu_toggle = $('#mnu-toggle ul li a');
        mnu_toggle.on("click", function() {
            var checkElement = $(this).next();
            checkElement.stop().animate({ 'height': 'toggle' }, 500).parent().toggleClass('active');
            if (checkElement.is('ul')) {
                return false;
            }
        });

        $("#js-mnu_container, menu_item").on("click", function() {
            $(".sandwich").toggleClass("active");
        });
        // ---------------------------------------------------------------

        // -------------------------------------------------------------
        var main_mnu_toggle = $('#js-main-menu-mob');
        for (var i = 0, len = main_mnu_toggle.children("li").length; i < len; i++) {
            if (main_mnu_toggle.children("li").eq(i).children().is("ul")) {
                main_mnu_toggle.children("li").eq(i).children("a").append('<i class="fa fa-angle-down" aria-hidden="true"></i>');
                main_mnu_toggle.children("li").eq(i).children("a").on("click", function() {
                    main_mnu_toggle.children("li").eq(i).next().slideToggle('slow');
                    return false;
                });
            }
        }
        // -------------------------------------------------------------

        // ---------------------------------------------------------------
        $("#js-mnu_container").on("click", function() {
            var mnu_popup_mob = $("#mnu-popup-mob");
            if (mnu_popup_mob.hasClass("active")) {
                mnu_popup_mob.toggleClass("active").fadeOut();
            } else {
                mnu_popup_mob.toggleClass("active").fadeIn();
            }
        });
        // -------------------------------------------------------------

        // Select Search Start
        var cat_select_search = $('#cat-select-menu, #cat-select-search');
        var elements, numberOfOptions, $styledSelect, list, li_list, join_list, $list, $listItems;
        for (var k = 0, klen = cat_select_search.length; k < klen; k++) {
            elements = cat_select_search.eq(k);
            numberOfOptions = cat_select_search.eq(k).children('option').length;
            elements.addClass('select-hidden');
            elements.wrap('<div class="select"></div>');
            elements.after('<div class="box-allcategories"></div>');
            $(".wrap-allcat").append('<i class="fa fa-angle-down" aria-hidden="true"></i>');
            $styledSelect = elements.next('div.box-allcategories');
            $styledSelect.text(elements.children('option').eq(0).text());

            list = [];
            li_list = [];
            list.push('<ul class="select-options">');
            for (i = 0; i < numberOfOptions; i++) {
                li_list.push('<li rel="' + elements.children('option').eq(i).val() + '">' + elements.children('option').eq(i).text() + '</li>');
            }
            list.push(li_list.join(''), '</ul>');

            join_list = list.join('');
            $styledSelect.after(join_list);

            $list = $styledSelect.next('.select-options');

            $styledSelect.on("click", function(e) {
                if ($('.select-options').is(':visible')) {
                    e.stopPropagation();
                    $styledSelect.text($(this).text()).removeClass('active');
                    elements.val($(this).attr('rel'));
                    $('.select-options').hide();
                } else {
                    e.stopPropagation();
                    for (var j = 0, l = $('div.box-allcategories.active').length; j < l; j++) {
                        $('div.box-allcategories.active').eq(j).removeClass('active').next('ul.select-options').hide();
                    }
                    $(this).toggleClass('active').next('ul.select-options').toggle();
                } //end if
            });

            $listItems = $list.children('li');
            $listItems.on("click", function(e) {
                e.stopPropagation();
                $('div.box-allcategories.active').text($(this).text()).removeClass('active');
                elements.val($(this).attr('rel'));
                $('.select-options').hide();
            });
            $(document).on("click", function() {
                $styledSelect.removeClass('active');
                $('.select-options').hide();
            });
        }

        // Select Search End

        // Select Town Start
        var select_town = $('#select-town');
        var div_steptwo_active = $('div.select-step-two.active');
        for (k = 0, klen = select_town.length; k < klen; k++) {

            elements = select_town.eq(k);
            numberOfOptions = select_town.eq(k).children('option').length;
            elements.addClass('select-hidden');
            elements.wrap('<div class="select"></div>');
            elements.after('<div class="select-step-two"></div>');
            $(".wrap-allcat").append('<i class="fa fa-angle-down" aria-hidden="true"></i>');
            $styledSelect = elements.next('div.select-step-two');
            $styledSelect.text(elements.children('option').eq(0).text());

            list = [];
            li_list = [];
            list.push('<ul class="select-options">');
            for (i = 0; i < numberOfOptions; i++) {
                li_list.push('<li rel="' + elements.children('option').eq(i).val() + '">' + elements.children('option').eq(i).text() + '</li>');
            }
            list.push(li_list.join(''), '</ul>');

            join_list = list.join('');
            $styledSelect.after(join_list);

            $list = $styledSelect.next('.select-options');

            $styledSelect.on("click", function(e) {
                if ($('.select-options').is(':visible')) {
                    e.stopPropagation();
                    $styledSelect.text($(this).text()).removeClass('active');
                    elements.val($(this).attr('rel'));
                    $('.select-options').hide();
                } else {
                    e.stopPropagation();

                    for (var j = 0, l = div_steptwo_active.length; j < l; j++) {
                        div_steptwo_active.eq(j).removeClass('active').next('ul.select-options').hide();
                    }
                    $(this).toggleClass('active').next('ul.select-options').toggle();
                } //end if
            });

            $listItems = $list.children('li');
            $listItems.on("click", function(e) {
                e.stopPropagation();
                div_steptwo_active.text($(this).text()).removeClass('active');
                elements.val($(this).attr('rel'));
                $('.select-options').hide();
            });
            $(document).on("click", function() {
                $styledSelect.removeClass('active');
                $('.select-options').hide();
            });
        }

        // Select Town End

        // filtering the input field
        $('#min-custom-size, #max-custom-size').on("keypress", function(event) {
            var key, keyChar;
            if (!event) {
                event = window.event;
            }
            if (event.keyCode) key = event.keyCode;
            else if (event.which) key = event.which;
            if (key === null || key === 0 || key === 8 || key === 13 || key === 9 || key === 46 || key === 37 || key === 39) return true;
            keyChar = String.fromCharCode(key);
            if (!/\d/.test(keyChar)) return false;
        });
        $("#clear-searh-mob").on("click", function() {
            $(this).parent().find("#input-search-mob").val("");
        });
        $("#clear-searh").on("click", function() {
            $("#live-search .input-search").val("");
            $("#results-search ul").css("display", "none");
        });
        $("#box-search").on("click", function() {
            $("#wrap-allcat").appendTo("#live-search fieldset");
            $("#main-search-popup").fadeIn();
            $("#filter").focus();
        });
        $("#close-popup-search").on("click", function() {
            $("#box-search").after($(".wrap-allcat"));
            $("#main-search-popup").fadeOut();
            return false;
        });

        // Masonry Mob Footer Start
        var $item_foot_mob = $('#js-footer-item');
        $item_foot_mob.imagesLoaded(function() {
            $item_foot_mob.masonry({
                columnWidth: ".footer-wrap-mob",
                itemSelector: '.footer-wrap-mob',
                percentPosition: true,
                singleMode: false,
                isResizable: true,
                isAnimated: true,
                animationOptions: {
                    queue: false,
                    duration: 500
                }
            });
        });
        // Masonry Mob Footer End

        // Logic Range Slider Min Start
        var min_custom_size = $("#min-custom-size");
        var max_custom_size = $("#max-custom-size");
        $("#slider-range").slider({
            range: true,
            min: 0,
            max: 6000,
            values: [0, 999]
        }).bind({
            slide: function(event, ui) {

                min_custom_size.val(formatNumber(ui.values[0]));
                max_custom_size.val(formatNumber(ui.values[1]));
            }
        });
        min_custom_size.val($("#slider-range").slider("values", 0));
        max_custom_size.val($("#slider-range").slider("values", 1));
        $("#resize-curs input").change(function() {
            $("#slider-range").slider("values", [min_custom_size.val(), max_custom_size.val()]);
        });
        // Logic Range Slider Min End

        var el = $('#nav_list_first div a');
        el.on("click", function() {
            var checkElement = $(this).next();
            checkElement.stop().animate({ 'height': 'toggle' }, 500).parent().toggleClass('active');
            if (checkElement.is('div')) {
                return false;
            }
        });
        // --------------------------------------------------------------------------------------

        // Using preview images Start
        $(".preview-img-mini-product").on("click", function() {
            var preview_img_mini_product = $(this).parents("#block-img-product").find('.preview-img-mini-product');
            for (var i = 0, len = preview_img_mini_product.length; i < len; i++) {
                if (preview_img_mini_product.eq(i).hasClass('preview-product-active')) {
                    preview_img_mini_product.eq(i).removeClass('preview-product-active');
                }
            }
            $(this).addClass('preview-product-active');
            $("img", this).parents("#block-img-product").find("#full-img-product img").attr("src", $(this).data('full-img'));
        });

        // --------------------------------------------------------------------------------------
        $(".preview-img-mini").on("click", function() {
            var preview_img_mini = $(this).parents(".box-preview-img").find('.preview-img-mini');
            for (var i = 0, len = preview_img_mini.length; i < len; i++) {
                if (preview_img_mini.eq(i).hasClass('preview-active')) {
                    preview_img_mini.eq(i).removeClass('preview-active');
                }
            }
            $(this).addClass('preview-active');
            $("img", this).parents(".js-change-img").find(".box-img-products img").attr("src", $(this).data('medium-img'));
        });
        // Using preview images End

        // Hiding elements by clicking outside the box Start
        $(document).on("mouseup", function(e) {
            var div = $('#sort-box-sample ul, #js-sort-sample');
            if (!div.is(e.target) && div.has(e.target).length === 0) {
                $('#sort-box-sample').css({
                    "borderRadius": "3px"
                });
                $("#sort-box-sample ul").removeClass("active").fadeOut();
                $("#js-sort-sample").removeClass("sort-arrow-up");
            }
        });
        // Hiding elements by clicking outside the box End

        // Changing the display of products Start
        $('#js-stract-sample').on("click", function() {
            var self = $(this);
            var stract_box_sample = $("#stract-box-sample");
            var js_stract_sample = $("#js-stract-sample");
            if (stract_box_sample.children('ul').hasClass("active")) {
                stract_box_sample.css({
                    "borderRadius": "3px"
                });
                stract_box_sample.children('ul').removeClass("active").fadeOut();
                js_stract_sample.removeClass("stract-arrow-up");
            } else {
                stract_box_sample.css({
                    "borderRadius": "3px 3px 0px 0px"
                });
                stract_box_sample.children('ul').addClass("active").fadeIn();
                js_stract_sample.addClass("stract-arrow-up");
            }
            $("#stract-list li").on("click", function() {
                stract_box_sample.children('ul').removeClass("active").fadeOut();
                js_stract_sample.removeClass("stract-arrow-up");
                stract_box_sample.css({
                    "borderRadius": "3px"
                });

                var currentSrtact = $(this).data("stract");
                $(this).removeClass("active");
                $(this).siblings().addClass("active");
                self.find(".js-active-stract").removeClass("stract-one stract-two stract-three stract-four");
                self.find(".js-active-stract").addClass(currentSrtact);
            });

        });
        // --------------------------------------------------------------------------------------
        $('#js-sort-sample').on("click", function() {
            var self = $(this);
            var sort_box_sample = $('#sort-box-sample');
            if (sort_box_sample.children('ul').hasClass("active")) {
                sort_box_sample.css({
                    "borderRadius": "3px"
                });
                sort_box_sample.children('ul').removeClass("active").fadeOut();
                $("#js-sort-sample").removeClass("sort-arrow-up");
            } else {
                sort_box_sample.css({
                    "borderRadius": "3px 3px 0px 0px"
                });
                sort_box_sample.children('ul').addClass("active").fadeIn();
                $("#js-sort-sample").addClass("sort-arrow-up");
            }
            $("#sort-list li").on("click", function() {
                sort_box_sample.children('ul').removeClass("active").fadeOut();
                $("#js-sort-sample").removeClass("sort-arrow-up");
                sort_box_sample.css({
                    "borderRadius": "3px"
                });
                var currentSort = $(this).data("sort");
                var sortText = $(this).text();
                $(this).removeClass("active");
                $(this).siblings().addClass("active");
                self.find(".js-active-sort").removeClass("sort-one sort-two sort-three sort-four");
                self.find(".js-active-sort").addClass(currentSort);
                self.find(".js-active-sort").text(sortText);
            });
        });
        $("#stract-list li[data-stract='stract-one']").on("click", function() {
            $(".block-products").removeClass("active");
            $("#unit-one").addClass("active");
        });
        $("#stract-list li[data-stract='stract-two']").on("click", function() {
            $(".block-products").removeClass("active");
            $("#unit-two").addClass("active");
        });
        $("#stract-list li[data-stract='stract-three']").on("click", function() {
            $(".block-products").removeClass("active");
            $("#unit-three").addClass("active");
        });
        $("#stract-list li[data-stract='stract-four']").on("click", function() {
            $(".block-products").removeClass("active");
            $("#unit-four").addClass("active");
        });
        $(document).on("mouseup", function(e) {
            var div = $('#stract-box-sample ul, #js-stract-sample');
            if (!div.is(e.target) && div.has(e.target).length === 0) {
                $('#stract-box-sample').css({
                    "borderRadius": "3px"
                });
                $("#stract-box-sample ul").removeClass("active").fadeOut();
                $("#js-stract-sample").removeClass("stract-arrow-up");
            }
        });
        // Changing the display of products End

        $('#top-left .level-two, #top-right .level-two').on("click", function() {
            $("#top-left li ul").fadeOut();
            $(this).parent().children("ul").fadeIn();
        });
        // Hiding elements by clicking outside the box Start
        $(document).on("mouseup", function(e) {
            var div = $('#top-left li ul, #top-right li ul');
            if (!div.is(e.target) && div.has(e.target).length === 0) {
                div.hide();
            }
        });

        // --------------------------------------------------------------------------------------

        $(document).on("mouseup", function(e) {
            var div = $('#wrap-allcat ul, .box-allcategories, #box-discont');
            if (!div.is(e.target) && div.has(e.target).length === 0) {
                $("#wrap-allcat ul").removeClass("active").fadeOut();
                $("#main-discont").fadeOut();
            }
        });

        //Chrome Smooth Scroll
        try {
            $.browserSelector();
            if ($("html").hasClass("chrome")) {
                $.smoothScroll();
            }
        } catch (err) {

        }

        $("img, a").on("dragstart", function(event) {
            event.preventDefault();
        });

    });

    $(window).resize(function() {
        // Reinitialization functions Start
        autoWidthHeader();
        offsetSearch();
        masonryUnitOne();
        $("#box-search").on("click", function() {
            $("body").css("position", "fixed");
            offsetSearch();
            $("#main-search-popup").fadeIn();
        });
    });


})(jQuery);
