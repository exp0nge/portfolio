$(document).ready(function(){
  
$("#preloader-form").hide();  
$("#progress").hide();
$('#menu-up').show();
  
var loc = window.location.pathname;
var dir = loc.substring(0, loc.lastIndexOf('/'));
if (dir === '/tracker/watch_episode'){
  $('#floaty-side-nav').append('<li><a href="/tracker/" class="waves-effect waves-circle waves-light btn-floating blue" id="home"><i class="material-icons">home</i></a></li>');
  $('#menu-up').hide();
  
}
  
$('.ep-done').on("click", function(){
  var pk = $(this).attr("series-id");
  
  $.ajax({
    url: "/tracker/watched/" + pk,
    type: "GET",
    data: {pk: pk},
    success: function(response){
      $("#ep-number-" + pk).html(response)
    }
  });
});


$('.series-delete').on("click", function(){
  var pk = $(this).attr("series-id");
  
  $.ajax({
    url: "/tracker/delete/" + pk,
    type: "GET",
    data: {pk: pk},
    success: function(response){
      $("#" + pk + "-div").empty();
      Materialize.toast('<span>' + response + ' deleted.</span>', 4000);
    }
  });
});


var form = $('#add-form');
form.submit(function(e){
  e.preventDefault();
  $("#preloader-form").show();
  $.ajax({
    url: '/tracker/add/',
    type: 'POST',
    data: form.serialize(),
    success: function(response){
      $('#add-form').trigger('reset');
      $("#preloader-form").hide();
      $("#add_series_modal").closeModal();
      Materialize.toast('<span>' + response + ' added.</span>', 4000);
    },
    error: function(response){
      $("#preloader-form").hide();
      alert("Title and release day is required!");
    }
    
  });
  return false;
  
});


$('#favorite_link').on('click', function(e) {
    e.preventDefault();
    var site_url = $('#stream_site_id').val();
    if (site_url.length > 7 && site_url.includes("http://")){
      $.ajax({
        url: '/tracker/favorite_site/?site=' + site_url,
        type: 'POST',
        data: {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
        success: function(response){
          $('#add_fav_link').html('done')
        },
        error: function(response){
          alert(response);
          console.log(response);
        }
      });
    }
    else{
      alert('Site url should include "http://"')
    }
    
});


});


