$(document).ready(function(){
  
$("#preloader-form").hide();  
$("#progress").hide();
$('#menu-up').show();

$('.dropdown-sites').dropdown({
    inDuration: 300,
    outDuration: 225,
    constrain_width: true, // Does not change width of dropdown to that of the activator
    hover: false, // Activate on hover
    gutter: 0, // Spacing from edge
    belowOrigin: true // Displays dropdown below the button
  }
);

    var cardHtml = function (cover_image_url, release_day, title, series_ID, current_episode, stream_site) {
        var mainBody = '<div series-id="' + series_ID + '"><button class="waves-effect waves-light btn ep-done  deep-orange lighten-1" series-id="' + series_ID + '">#' +
            '<strong id="ep-number-' + series_ID + '">' + current_episode + '</strong><i class="material-icons left">done</i></button>' +
            '<span>midnight</span>' +
            '<a href="/tracker/watch_episode/' + series_ID + '" class="waves-effect waves-light btn ep-done  deep-orange lighten-1 right" series-id="' + series_ID + '">' +
            '<i class="material-icons">play_arrow</i></a></div>' +
            '<li class="collection-item avatar" series-id="' + series_ID + '">' +
            ' <img src="' + cover_image_url + '" alt="" class="circle">' +
            '<span class="title">' + title + '</span>' +
            '<p>' + release_day + '</p>' +
            '<div class="secondary-content"><a class="waves-effect waves-light dropdown-button btn-flat" ' +
            'data-activates="' + series_ID + '_options"><i class="material-icons gray">settings</i></a></li>';

        var settingsOptions = '<!-- Dropdown Structure -->' +
        '<ul id="' + series_ID + '_options" class="dropdown-content">' +
            '<li><a class="material-icons update-form" pk="' + series_ID + '" title="' + title + '">edit</a></li>' +
            '<li><a href="#" class="material-icons">share</a></li> <li class="divider"></li> ' +
            '<li><a class="material-icons series-delete red" series-id="' + series_ID + '">delete</a></li></ul>';
        return mainBody + settingsOptions;
};
    var altBool = true;
$.ajax({
  url: '/tracker/get_series_as_json/',
  type: 'GET',
  data: {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
  dataType: 'json',
  success: function(response){
      $('#series-deck').html('<ul class="collection" id="card-list"></ul>');
      $('#series-deck2').html('<ul class="collection" id="card-list2"></ul>');
    for (var key in response){
      if(response.hasOwnProperty(key)){
        var series = response[key];
          var fullHtml = cardHtml(series.cover_image_url, series.release_day, series.title, series.id,
              series.current_episode, series.stream_site);
          if (altBool) {
              $('#card-list').append(fullHtml);
              altBool = false;
          } else {
              $('#card-list2').append(fullHtml);
              altBool = true;
        }
      }
    }
      // initialize
      $('.dropdown-button').dropdown();

  },
  error: function(response){
    console.log(response);
  }

  });

$('#add_series_button').on('click', function() {
  $('.dropdown-sites').dropdown({belowOrigin: true});
    // Get favorite websites and load into dropdown
    $.ajax({
      url: '/tracker/get_favorite_sites/',
      type: 'GET',
      success: function(response){
        $.each(response, function(index, value){
          $('#fav-sites-dropdown').append('<li class="fav-item"><a href="#!">' + value + '</a></li>');
        });
        $('.fav-item').on('click', function() {
           $('#stream_site_id').val($(this).html().replace('<a href="#!">', '').replace('</a>', '')); 
        });
      },
      error: function(response){
        alert(response);
        console.log(response);
      }
    });
    // Tag suggestions
    var tag_list = ['anime', 'tv series', 'manga'];
    $('.dropdown-tag').dropdown({belowOrigin: true});
    for(var i = 0; i < tag_list.length; i++){
      $('#tags-dropdown').append('<li><a class="tag-item" href="#!">' + tag_list[i] + '</a></li>');
    }
    $('.tag-item').on('click', function(e) {
        e.preventDefault();
        $('.dropdown-tag').focus();
        $('.dropdown-tag').val($(this).html());
    });
    
});
     

var loc = window.location.pathname;
var dir = loc.substring(0, loc.lastIndexOf('/'));
if (dir === '/tracker/watch_episode'){
  $('#floaty-side-nav').append('<li><a href="/tracker/" class="waves-effect waves-circle waves-light btn-floating blue" id="home"><i class="material-icons">home</i></a></li>');
  $('#menu-up').hide();
  
}

var reloadCard = function(PK){
  var pkDiv = '#' + PK + '-div';
  $.ajax({
    url: '/tracker/',
    success: function(response){
      $(pkDiv).html($(response).find(pkDiv).html());
      
      $('.dropdown-button').dropdown();
      $('.collapsible').collapsible();
      $('.tooltipped').tooltip();
    
    },
    error: function(response){
      console.log(response);
    }
  });
};

    $(document.body).on("click", '.ep-done', function () {
        var pk = $(this).attr("series-id");

        $.ajax({
            url: "/tracker/watched/" + pk,
            type: "GET",
            data: {pk: pk},
            success: function (response) {
                $("#ep-number-" + pk).html(response)
            }
        });
});


    $(document.body).on("click", '.series-delete', function () {
  var pk = $(this).attr("series-id");
  
  $.ajax({
    url: "/tracker/delete/" + pk,
    type: "GET",
    data: {pk: pk},
    success: function(response){
        $('div[series-id=' + pk + ']').remove();
        $('li[series-id=' + pk + ']').remove();
      Materialize.toast('<span>' + response + ' deleted.</span>', 4000);
    }
  });
});


var form = $('#add-form');
form.submit(function(e){
  e.preventDefault();
  $('#add-series-button').hide();
  $("#preloader-form").show();
  $.ajax({
      dataType: 'json',
    url: '/tracker/add/',
    type: 'POST',
    data: form.serialize(),
    success: function(response){
        if (response[0] == 'error') {
            console.log(response);
        $('#add-series-button').show();
        $("#preloader-form").hide();
            var errorDict = {'release_day': 'Day', 'tag': 'Tag', 'title': 'Title'};
            for (var i = 0; i < response.errors.length; i++) {
                $('#error-message').append('<li class="collection-item">' + errorDict[response.errors[i]] + ' is required.</li>');
            }
        $('#add_series_modal').animate({ scrollTop: 0 }, 'slow');
      }
      else {
        $('#add-form').trigger('reset');
        $("#preloader-form").hide();
        $("#add_series_modal").closeModal();
            var series = response[0];
            $('#card-list').append(cardHtml(series.cover_image_url, series.release_day, series.title, series.id,
                series.current_episode, series.stream_site));
            Materialize.toast('<span>' + series.title + ' added.</span>', 4000);
      }
    },
    error: function(response){
      $("#preloader-form").hide();
      $('#add-series-button').show();
      console.log(response);
      alert("Something went wrong.");
    }
    
  });
});

    $(document.body).on('click', '.update-form', function (e) {
    e.preventDefault();
    var updateSeriesPK = $(this).attr('pk');
    var title = $(this).attr('title');
    $.get('/tracker/update/' + updateSeriesPK, function(data){
      $('#update-series-modal-content').html(data);
      $('select').material_select();
      $('#update-button').html('<i class="material-icons">check</i>');
      $('#update-series-modal').openModal();
      $('input').focus();
      $('#update-series-form').on('submit', function(e) {
            e.preventDefault();
          $('#update-button').hide();
            $.ajax({
              url: '/tracker/update/' + updateSeriesPK,
              type: 'POST',
              data: $('#update-series-form').serialize(),
              success: function(response){
                if(response.includes('collection-item')){
                  $('#update-button').show();
                  $('#error-div').html($(response).find('.collection').html());
                }
                else{
                  $('#update-series-modal').closeModal();
                  reloadCard(updateSeriesPK);
                  Materialize.toast('<span>' + title + ' updated.</span>', 4000);
                }
              },
              error: function(response){
                $('#update-button').show();
                alert('Error');
              }
            });
        });
      
    });
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


