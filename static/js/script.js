(function($){

var onDocReady = function(){

  console.log("Registering doc ready handler");

  var form = $('#rsvp-submit');



  form.submit(function(e){

      var data = {
        'name': $('input[name=name]').val(),
        'email': $('input[name=email]').val(),
        'count': $('input[name=count]').val(),
        'requests': $('input[name=requests]').val()
      };

      $.ajax({
        type: 'POST',
        url: 'rsvp',
        data: data,
        dataType: 'json',
        encode: true
      }).done(function(resp){
        
        console.log(resp);

        location.hash = '#';
        window.scrollTo(0,0);

        if(resp.success){
          $('.alert')
            .removeClass('alert-danger')
            .addClass('alert-success')
            .html(resp.message);
        } else if (!resp.success){
          $('.alert')
            .removeClass('alert-success')
            .addClass('alert-danger')
            .html(resp.message);
        }

      });

      e.preventDefault();
      return false

  });

};

$(document).ready(onDocReady);

})(window.jQuery)