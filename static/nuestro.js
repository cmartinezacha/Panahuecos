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
	$(".solo").click(function(event){
		event.stopPropagation();
		big_parent = $(this).parent().parent();

		$(big_parent).find("input").each(function(){
			$(this).prop("checked",false);
		});
		label = $(this).siblings().get();
		checkbox = $(label).find("input");
		checkbox.prop("checked",true);
	});

	$(".checkbox").click(function(event){
		checkbox = $(this).find("input")[0];
		if(checkbox.checked == false){
			checkbox.checked = true;
		} else{
			checkbox.checked = false;
		}
	});

	$(".input-checkbox").click(function(event){
		event.stopPropagation();
		if(this.checked == false){
			this.checked = true;
		} else{
			this.checked = false;
		}
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




