(function($){

var onDocReady = function(){

  console.log("Registering doc ready handler");

  var form = $('#rsvp-submit');

  form.submit(function(e){

      var data = {
        'name': $('input[name=name]').val(),
        'email': $('input[name=email]').val(),
        'count': $('input[name=count]').val(),
        'info': $('textarea[name=requests]').val()
      };

      $.ajax({
        type: 'POST',
        url: 'rsvp',
        data: data,
        dataType: 'json',
        encode: true
      }).done(function(resp){
        
        console.log(resp);

        if(resp.success){
          $('.rsvp-alert')
            .removeClass('alert-danger')
            .addClass('alert-success')
            .html(resp.message);
        } else if (!resp.success){
          $('.rsvp-alert')
            .removeClass('alert-success')
            .addClass('alert-danger')
            .html(resp.message);
        }

      });

      e.preventDefault();
      return false

  });

};

var giftSubmits = $('.gift-register .btn');

giftSubmits.click(function(e){

  var giftId = $(this).data('gift-id');
  var count = $('#gift-' + giftId + ' input[name=count]').val()

  console.log('Submitting #' + count + ' for gift id ' + giftId);

  var data = {
    'gift_id': giftId,
    'count': count
  };

  $.ajax({
    type: 'POST',
    url: 'register_gift',
    data: data,
    dataType: 'json',
    encode: true
  }).done(function(resp){
    
    console.log(resp);

    if(resp.success){
      $('#alert-' + giftId)
        .removeClass('alert-danger')
        .addClass('alert-success')
        .html(resp.message);
    } else if (!resp.success){
      $('#alert-' + giftId)
        .removeClass('alert-success')
        .addClass('alert-danger')
        .html(resp.message);
    }

  });

  e.preventDefault();
  return false;

});

$(document).ready(onDocReady);

})(window.jQuery)