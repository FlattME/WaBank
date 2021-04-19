$('.collapse').collapse()

$('#myCollapsible').collapse({
    toggle: false
})

$('#collapseThree').on('click', function (event) {
    $("#collapseThree").removeClass("active");
    $this.addClass("active");
    nav.removeClass("active");
    nav_toggle.removeClass("active");
  })