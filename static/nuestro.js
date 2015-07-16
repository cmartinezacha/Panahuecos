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

	$(".checkbox").click(function(){
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

	$(".todos").click(function(){
		big_parent = $(this).parent().parent();
		$(big_parent).find("input").each(function(){
			$(this).prop("checked", true);
		});
	});

	$.datepicker.setDefaults($.datepicker.regional['es']);

	$(".imagen-up img:first-child").addClass("active");
	$(".imagen-up .button").click(function(event){
		event.stopPropagation();
		children = $(this).parent().find("img");
		amount_images = children.length;
		if (amount_images <= 1){
			return;
		}
		current = 0
		for (var i = 0; i < amount_images; i++) {
		    if ($(children[i]).hasClass("active")) {
		    	current = i;
		   		break;
			};
		};
		thisImage = $(children[current]);
		if ($(this).hasClass('prevButton')){
			if (current == 0){
				current = amount_images - 1
			}
			else{
				current = (current - 1) % amount_images
			}
		}
		else{
			current = (current + 1) % amount_images
		}
		nextImage = $(children[current]);
		// thisImage.fadeTo('slow',0.3);
		thisImage.removeClass('active');
		thisImage.hide();
		// thisImage.css('opacity',1);
		// nextImage.fadeIn('slow');
		// nextImage.css('opacity',1);
		nextImage.show();
		nextImage.addClass('active');
		
	});

	$(function () {
		$("#fecha").datepicker({
			inline : true,
			onSelect : function(date){ 
				window.location.href ='/'+date  
			}
		});
	});

});




