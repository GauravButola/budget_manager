$(document).ready(function(){
	//Hide erros, on click.
	$(".error, .success").on("click", function(){
		$(this).fadeOut();
	});

	//Show report
	$(".showmore").on("click", function(){
		$(".reports").slideToggle();
	});

	//print repotr
	$(".print").on("click", function(){
		window.print();
	});

});
