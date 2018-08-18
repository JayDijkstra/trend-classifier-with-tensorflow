$(document).ready(function(){
  updateCountDown();
  $('.message').change(updateCountDown);
  $('.message').keyup(updateCountDown);


  function readUrl(input){
    if(input.files && input.files[0]){
      var reader = new FileReader();

      reader.onload = function(e){
        $('#blah').attr('src', e.target.result);
      }

      reader.readAsDataURL(input.files[0]);
    }else {
      $('#blah').hide()
    }
  }

  $("#imgInp").change(function(){
    readUrl(this);
  })

  function updateCountDown() {
    //Create a function for minimal 140 characters.
    var remCharacters = 140 - $('.message').val().length;
    $('.countdown').text(remCharacters + ' characters remaining.');
  }
})
