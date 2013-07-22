jQuery.support.placeholder = (function(){
  var i = document.createElement('input');
  return 'placeholder' in i;
})();

if (!jQuery.support.placeholder) {
  $('[placeholder]').focus(function() {
    var input = $(this);
    if (input.val() == input.attr('placeholder')) {
      input.val('');
    }
  }).blur(function() {
    var input = $(this);
    if (input.val() == '') {
      input.val(input.attr('placeholder'));
    }
  }).blur().parents('form').submit(function() {
    $(this).find('[placeholder]').each(function() {
      var input = $(this);
      if (input.val() == input.attr('placeholder')) {
        input.val('');
      }
    })
  });
}

$(document).ready( function() {
  $('.dropdown-toggle').dropdown();
});

// Change the right-chevron to down-chevron when people click to show filters
$('.collapse').on('show', function () {
  var i = $(this).parent('.accordion-group').find('i');
  i.attr('class', 'icon-chevron-down');    
});

// Change the down-chevron to right-chevron when people click to hide filters
$('.collapse').on('hide', function () {
  var i = $(this).parent('.accordion-group').find('i');
  i.attr('class', 'icon-chevron-right');    
});