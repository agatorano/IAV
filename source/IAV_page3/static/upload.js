var main = function(){
  

  $('#id_z_score').tipsy({gravity: 's'});
  $('#id_screens').tipsy({gravity: 's'});
  $('#flu_protein').tipsy({gravity: 'w'});
  $('#id_word_search').tipsy({gravity: 'n'});
  $('#id_docfile_iav').tipsy({gravity: 'w'});

  //dropdow for front page
  $(".dropdown_2 dt a").on('click', function () {
      $(".dropdown_2 dd ul").slideToggle('fast');
  });

  $(".dropdown_2 dd ul li a").on('click', function () {
      $(".dropdown_2 dd ul").hide();
  });

  function getSelectedValue(id) {
       return $("#" + id).find("dt a span.value").html();
  }

  $(document).bind('click', function (e) {
      var $clicked = $(e.target);
      if (!$clicked.parents().hasClass("dropdown_2")) $(".dropdown_2 dd ul").hide();
  });


  $('.mutliSelect_2 input[type="checkbox"]').on('click', function () {
    
      var title = $(this).closest('.mutliSelect_2').find('input[type="checkbox"]').val(),
          title = $(this).val() + ",";
    
      if ($(this).is(':checked')) {
          var html = '<span title="' + title + '">' + title + '</span>';
          $('.multiSel_2').append(html);
          $(".hida").hide();
      } 
      else {
          $('span[title="' + title + '"]').remove();
          var ret = $(".hida");
          $('.dropdown_2 dt a').append(ret);
          
      }
  });

  //dropdown IAV
  $(".dropdown dt a").on('click', function () {
      $(".dropdown dd ul").slideToggle('fast');
  });

  $(".dropdown dd ul li a").on('click', function () {
      $(".dropdown dd ul").hide();
  });

  function getSelectedValue(id) {
       return $("#" + id).find("dt a span.value").html();
  }

  $(document).bind('click', function (e) {
      var $clicked = $(e.target);
      if (!$clicked.parents().hasClass("dropdown")) $(".dropdown dd ul").hide();
  });


  $('.mutliSelect input[type="checkbox"]').on('click', function () {
    
      var title = $(this).closest('.mutliSelect').find('input[type="checkbox"]').val(),
          title = $(this).val() + ",";
    
      if ($(this).is(':checked')) {
          var html = '<span title="' + title + '">' + title + '</span>';
          $('.multiSel').append(html);
          $(".hida").hide();
      } 
      else {
          $('span[title="' + title + '"]').remove();
          var ret = $(".hida");
          $('.dropdown dt a').append(ret);
          
      }
  });

  $('.spinner .btn:first-of-type').on('click', function() {
    $('.spinner input').val( parseInt($('.spinner input').val(), 10) + 1);
  });
  $('.spinner .btn:last-of-type').on('click', function() {
    $('.spinner input').val( parseInt($('.spinner input').val(), 10) - 1);
  });

  $('li').click(function(){
    var current = $('li.active');
    var next = $(this);
    current.removeClass('active');
    next.addClass('active');
  });

  
};
$(document).ready(main)
