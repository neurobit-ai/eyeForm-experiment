$(function() {

	'use strict';

	// Form

	var eyeForm = function() {
		if ($('#eyeForm').length > 0 ) {
			$( "#eyeForm" ).validate( {
				rules: {
					medRecNo: "required",
					site: "required",
					caseNo: "required",
					dateOfVisit: "required",
					dateOfBirth: "required",
					// name: "required",
					// email: {
					// 	required: true,
					// 	email: true
					// },
					// message: {
					// 	required: true,
					// 	minlength: 5
					// }
				},
				messages: {
					// name: "Please enter your name",
					// email: "Please enter a valid email address",
					// message: "Please enter a message"
				},
				/* submit via ajax */
				submitHandler: function(form) {		
					var $submit = $('.submitting'),
						waitText = '上 傳 中 . . .';
					$('#submit').prop('disabled', true);
					$('#caseNo').prop('disabled', false);
					$('#age').prop('disabled', false);
					$('#odRisk').val(localStorage.getItem('右眼'));
					$('#osRisk').val(localStorage.getItem('左眼'));
					$.ajax({   	
				      type: "POST",
				      //   url: "https://script.google.com/macros/s/AKfycbx75LIQkagfyeoMc6Uu9sLrHZF0cZOtSdyXhTanCmr5D0UxJd5PMO0VwjaFx6ppWZf49Q/exec",
				      url:target_url,
              data: $(form).serialize(),

				      beforeSend: function() { 
				      	$submit.css('display', 'block').text(waitText);
				      },
				      complete: function(msg) {
		               if (msg == '[object Object]') {
		               	$('#form-message-warning').hide();
				            setTimeout(function(){
		               		$('#eyeForm').fadeOut();
		               	}, 100);
				            setTimeout(function(){
				               $('#form-message-success').fadeIn();   
		               	}, 1000);
			               
			            } else {
			               $('#form-message-warning').html(msg);
				            $('#form-message-warning').fadeIn();
				            $submit.css('display', 'none');
			            }
				      },
				      error: function() {
				      	$('#form-message-warning').html("Something went wrong. Please try again.");
				         $('#form-message-warning').fadeIn();
				         $submit.css('display', 'none');
				      }
			      });
            $.ajax({   	
              type: "POST",
                url: "https://script.google.com/macros/s/AKfycby1eLmiT7l1x7UQ6hB2KxHTlYmXpkm87t3Zn4NH5A2Btqo-knqaC5NzLT09X5mo6Mss/exec",
              data: $(form).serialize()
            });   		
              },
              invalidHandler: function (event, validator) {
                // 當表單驗證失敗時執行
                console.log("Please correct the errors before submitting.");
                console.log("URL : " + target_url + " SHEET : " + target_sheet);	
		  		}
				
			} );
		}
	};
	eyeForm();

});
