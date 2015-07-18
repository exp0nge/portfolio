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

var cardHtml = function(rowBool, cover_image_url, release_day, title , series_ID, current_episode, stream_site){
  var mainBody = '<div class="card small hoverable"> \
            <div class="card-image"> \
                <img src="' + cover_image_url +'"  width="300" height="250"> \
                <span class="card-title grey-text text-lighten-4">' + release_day + '</span> \
            </div> \
            <div class="card-content"> \
                <p class="truncate">' + title + '</p> \
            </div> \
             <!-- Dropdown Structure --> \
            <div class="card-action"> \
          <button class="waves-effect waves-light btn right ep-done left" \
          series-id="' + series_ID + '">#<strong id="ep-number-' + series_ID + '"> \
      '+ current_episode + '</strong><i class="material-icons left">done</i></button> \
            </div></div>';

    var menuOptions = '<div class="col s3" id="'+ series_ID +'-div">' +
        '<a class="waves-effect waves-light dropdown-button btn teal" data-activates="'+ series_ID + '_options">' +
        '<i class="material-icons gray">settings</i></a>';

    if (stream_site  === ''){
      menuOptions += '<a href="/tracker/watch_episode/' + series_ID + '" class="waves-effect btn-flat modal-trigger gray disabled right"><i class="material-icons">play_arrow</i></a>';
    }else{
        menuOptions += '<a href="/tracker/watch_episode/' + series_ID + '" class="waves-effect btn modal-trigger red right"><i class="material-icons">play_arrow</i></a>';
    }
    menuOptions += ' <!-- Dropdown Structure for Settings -->' +
        '<ul id="' + series_ID + '_options" class="dropdown-content">' +
    '<li><a class="material-icons update-form" pk="' + series_ID + '" title="' + series_ID + '">edit</a></li> ' +
    '<li><a href="#!" class="material-icons">share</a></li>' +
    '<li class="divider"></li>' +
    '<li><a class="material-icons series-delete red" series-id="' + series_ID +'">delete</a></li></ul>';

    return menuOptions + mainBody + '</div>';
};
$.ajax({
  url: '/tracker/get_series_as_json/',
  type: 'GET',
  data: {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
  dataType: 'json',
  success: function(response){
    // clear deck
    $("#series-deck").html('');
      var rowBool = true;
      var columnCount = 0;
      var fullHtml = '';
    for (var key in response){
      if(response.hasOwnProperty(key)){
        if (rowBool){
            fullHtml += '<div class="row">';
            rowBool = false;
        }
        var series = response[key];
        fullHtml += cardHtml(rowBool, series.cover_image_url, series.release_day, series.title , series.id,
            series.current_episode, series.stream_site);
        columnCount++;
        if(columnCount === 4) {
            fullHtml += '</div>';
            columnCount = 0;
            rowBool = true;
            $('#series-deck').append(fullHtml);
            fullHtml = '';
        }

      }
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
  $('#add-series-button').hide();
  $("#preloader-form").show();
  $.ajax({
    url: '/tracker/add/',
    type: 'POST',
    data: form.serialize(),
    success: function(response){
      if (response.includes('"errorlist"')){
        $('#add-series-button').show();
        $("#preloader-form").hide();
        response = response.replace('release_day', '');
        response = response.replace('tag', '');
        response = response.replace('title', '');
        $('#error-message').html('<div class="card-panel red">' + response + '</div>');
        $('#add_series_modal').animate({ scrollTop: 0 }, 'slow');
      }
      else {
        $('#add-form').trigger('reset');
        $("#preloader-form").hide();
        $("#add_series_modal").closeModal();
        Materialize.toast('<span>' + response + ' added.</span>', 4000);
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

$('.update-form').on('click', function(e) {
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
            $('#update-button').hide()
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


