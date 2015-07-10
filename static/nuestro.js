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
		yearSuffix: '',
		beforeShowDay: $.datepicker.noWeekends
	};
	$(".solo").click(function(){
	big_parent = $(this).parent().parent();

	$(big_parent).find("input").each(function(){
		console.log(this);
		$(this).prop("checked",false);
	});
	label = $(this).siblings().get();
	checkbox = $(label).find("input");
	checkbox.prop("checked",true);
	console.log(big_parent);
	});

	$.datepicker.setDefaults($.datepicker.regional['es']);

	// $('.editar').click(function(e){
 //    e.stopPropagation();
 //    $('#myModal3').modal("show");
 //  		});

});

$(function () {
	$("#fecha").datepicker({
		inline : true,
		onSelect : function(date){ 
			window.location.href ='/'+date  
		}
	});
});




