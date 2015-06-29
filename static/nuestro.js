$(function($){
	$.datepicker.regional['es'] = {
		closeText: 'Cerrar',
		prevText: '<Ant',
		nextText: 'Sig>',
		currentText: 'Hoy',
		monthNames: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
		monthNamesShort: ['Ene','Feb','Mar','Abr', 'May','Jun','Jul','Ago','Sep', 'Oct','Nov','Dic'],
		dayNames: ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'],
		dayNamesShort: ['Dom','Lun','Mar','Mié','Juv','Vie','Sáb'],
		dayNamesMin: ['Do','Lu','Ma','Mi','Ju','Vi','Sá'],
		weekHeader: 'Sm',
		dateFormat: 'dd-mm-yy',
		firstDay: 1,
		isRTL: false,
		showMonthAfterYear: false,
		yearSuffix: ''
	};
	$.datepicker.setDefaults($.datepicker.regional['es']);
});

$(function () {
	$("#fecha").datepicker({
		inline : true,
		onSelect : function(date){ 
			window.location.href ='/'+date  
		}
	});

});

// $(function() {
//    $('#nav li a').click(function() {
//       $('#nav li').removeClass();
//       $($(this).attr('href')).addClass('active');
//    });
// });

// $(".navbar-nav li").on("click", function() {
//    $(".navbar-nav li").removeClass("active");
//    $(this).addClass("active");
//  });
// $('.navbar-nav li a').click(function(e) {
//   var $this = $(this);
//   if (!$this.hasClass('active')) {
//     $this.addClass('active');
//   }
//   e.preventDefault();
// });
