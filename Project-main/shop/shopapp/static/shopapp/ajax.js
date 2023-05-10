$.ajaxSetup({ 
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                     if (cookie.substring(0, name.length + 1) == (name + '=')) {
                         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                         break;
                     }
                 }
             }
             return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     }
});

$(document).ready(function(){
	$(".addProduct").each(function(index, element) {
		$(element).submit(function(e){
			e.preventDefault();
			$.ajax({
				url: $("#catalogUrl").val(),
				type:"post",
				data: {
					"category":$(this).val(),
					"productId":$(element).find(".button").val(),
					"productAmount":$(element).find(".amount__number").val()
				},
				success: function(response){
					alert('Done')
				}
			});
		})
	});
});

$(document).ready(function(){
	$(".deleteProduct").each(function(index, element){
		$(element).submit(function(e){
			e.preventDefault();
			$.ajax({
				url: $("#basket").val(),
				type:"post",
				data: {
					"category":$(this).val(),
					"productId":$(element).find(".button").val()
				},
				success: function(response){
					element.closest('.card').remove()
				}
			});
		})
	});
});

const plusButtons = document.querySelectorAll('.amount__plus')
const minusButtons = document.querySelectorAll('.amount__minus')

function increase(e) {
	e.preventDefault()
	let number = e.currentTarget.previousElementSibling
	number.textContent = Number(number.textContent) + 1
	let i = number.getAttribute('value')
	number.setAttribute('value', Number(i) + 1)
}

function decrease(e) {
	e.preventDefault()
	let number = e.currentTarget.nextElementSibling
	if (number.textContent != 1) {
		number.textContent = Number(number.textContent) - 1
		let i = number.getAttribute('value')
		number.setAttribute('value', Number(i) - 1)
	}
}

plusButtons.forEach(element => {
	element.addEventListener('click', increase)
});

minusButtons.forEach(element => {
	element.addEventListener('click', decrease)
});