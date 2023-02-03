// $(document).ready(function () {
//
//     $(".btn-primary").on('click', function () {
//         var review = $('#review_text').val();
//         var parentId = $('#parent_id').val();
//         console.log(parentId);
//
//         console.log('done');
//         $.ajax({
//             url: "/products/add-product-review",
//             type: "post",
//             data: {
//                 product_review: review,
//                 product_id: "gg",
//                 parent_id: parentId,
//                 csrfmiddlewaretoken: "{{csrf_token}}"
//             },
//             dataType: 'json',
//             beforeSend: function () {
//                 $("#send_review_btn").addClass('disabled').text('در حال ارسال');
//             },
//             success: function (res) {
//                 if (res.bool === true) {
//                     $('#review_text').val('');
//                     // Append Element
//                     var _html = '<div class="card mb-2 animate__animated animate__bounce">\
//                                     <div class="card-body">\
//                                          <p>' + review + '</p>\
//                                          <p>\
//                                         <a href="#">{{request.user}}</a>\
//                                          </p>\
//                                     </div>\
//                                 </div>';
//                     $("review_" + parentId).append(_html);
//
//                     var prevCount = $("#review_count").text();
//                     $("#review_count").text("نظرات" + (parseInt(prevCount) + 1));
//                 }
//                 $("#send_review_btn").removeClass('disabled').text('در حال ارسال');
//             }
//         });
//     });
// });
function ShowSweet(title, icon, text, show_cancel_button, btn_color, btn_text) {
    Swal.fire({
        title: title,
        text: text,
        icon: icon,
        showCancelButton: show_cancel_button,
        confirmButtonColor: btn_color,
        confirmButtonText: btn_text
    })
}

//
// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let i = 0; i < cookies.length; i++) {
//             const cookie = cookies[i].trim();
//             // Does this cookie string begin with the name we want?
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }
//
// const csrftoken = getCookie('csrftoken');
//
// // const csrftoken = Cookies.get('csrftoken');
//
// function sendProductReview(productId) {
//     var review = $('#review_text').val();
//     var parentId = $('#parent_id').val();
//     console.log(parentId);
//     console.log(productId);
//     console.log('done');
//     $.ajax({
//         url: "/products/add-product-review",
//         type: "post",
//         data: {
//             product_review: review,
//             product_id: productId,
//             parent_id: parentId,
//             csrfmiddlewaretoken: "{{csrf_token}}"
//         },
//         dataType: 'json',
//         beforeSend: function () {
//             $("#send_review_btn").addClass('disabled').text('در حال ارسال');
//         },
//         success: function (res) {
//             if (res.bool === true) {
//                 $('#review_text').val('');
//                 // Append Element
//                 var _html = '<div class="card mb-2 animate__animated animate__bounce">\
//                         <div class="card-body">\
//                             <p>' + _comment + '</p>\
//                             <p>\
//                                 <a href="#">{{request.user}}</a>\
//                             </p>\
//                         </div>\
//                     </div>';
//                 $(".comment-wrapper-" + _answerid).append(_html);
//
//                 var prevCount = $("#review_count").text();
//                 $("#review_count").text("نظرات" + (parseInt(prevCount) + 1));
//             }
//             $("#send_review_btn").removeClass('disabled').text('در حال ارسال');
//         }
//     });

// });

// $.get('/products/add-product-review', {
//     product_review: review,
//     product_id: productId,
//     parent_id: parentId
// })
// .then(res => {
//     $('#reviews_area').html(res);
//     $('#review_text').val('');
//     $('#parent_id').val('');
//     console.log('done2')
//
//     if (parentId !== null && parentId !== '') {
//         console.log('sing')
//         document.getElementById('single_review_box_' + parentId).scrollIntoView({behavior: "smooth"});
//     } else {
//         document.getElementById('reviews_area').scrollIntoView({behavior: "smooth"});
//         console.log('mul')
//     }
// });
// }


function fillParentId(parentId) {
    $('#parent_id').val(parentId);
    document.getElementById('review_form').scrollIntoView({behavior: "smooth"});
}

function filterProducts() {
    const filterPrice = $('#sl2').val();
    const start_price = filterPrice.split(',')[0];
    const end_price = filterPrice.split(',')[1];
    $('#start_price').val(start_price);
    $('#end_price').val(end_price);
    $('#filter_form').submit();
}

function fillPage(page) {
    $('#page').val(page);
    $('#filter_form').submit();
}

function showLargeImage(imageSrc) {
    // // $('#main_image').attr('src', imageSrc);
    // $('#show_large_image_modal').attr('href', imageSrc);
    // $('#show_large_image_modal').attr('href', imageSrc);
}

function addProductToOrder(productId) {
    const productCount = $('#product-count').val();
    $.get('/order/add-to-order?product_id=' + productId + '&count=' + productCount).then(res => {
        Swal.fire({
            title: 'اعلان',
            text: res.text,
            icon: res.icon,
            showCancelButton: false,
            confirmButtonColor: '#3085d6',
            confirmButtonText: res.confirm_button_text
        }).then((result) => {
            if (result.isConfirmed && res.status === 'not_auth') {
                window.location.href = '/login';
            }
        });
    });
}

function removeOrderDetail(detailId) {
    $.get('/user/remove-order-detail?detail_id=' + detailId).then(res => {
        if (res.status === 'success') {
            $('#order-detail-content').html(res.body);
        }
    });
}


// detail id => order detail id
// state => increase , decrease
function changeOrderDetailCount(detailId, state) {
    $.get('/user/change-order-detail?detail_id=' + detailId + '&state=' + state).then(res => {
        if (res.status === 'success') {
            $('#order-detail-content').html(res.body);
        }
    });
}

$('.carousel[data-type="multi"] .item').each(function () {
    var next = $(this).next();
    if (!next.length) {
        next = $(this).siblings(':first');
    }
    next.children(':first-child').clone().appendTo($(this));

    for (var i = 0; i < 3; i++) {
        next = next.next();
        if (!next.length) {
            next = $(this).siblings(':first');
        }

        next.children(':first-child').clone().appendTo($(this));
    }
});
