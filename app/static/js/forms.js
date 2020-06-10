
        function checkForm(){
         var error=false; //to znaczy, że danych nie brakuje
         var errorText=""; //komunikat z błędem
         var contactName = document.getElementById("contactName");
         var contactEmail = document.getElementById("contactEmail"); 
		 var contactInfo = document.getElementById("contactInfo");
          if (contactName.value == ""){
			$("#errorName").removeClass('d-none');
			$("#contactName").addClass('is-invalid').removeClass('is-valid');
            error=true;
          } 
		  else{
			 $("#errorName").addClass('d-none');
			 $("#contactName").addClass('is-valid').removeClass('is-invalid');			 
		  }
          if(contactEmail.value == ""){
            $("#errorMail").removeClass('d-none');
			$("#contactEmail").addClass('is-invalid').removeClass('is-valid');
			errorText+="Podanie Emaila jest wymagane!";
            error=true;
          } else
          {
            var email = contactEmail.value;
            var regex = /^[a-zA-Z0-9._-]+@([a-zA-Z0-9.-]+\.)+[a-zA-Z0-9.-]{2,4}$/;
          if(regex.test(email)==false)
          {
			$("#errorMail").removeClass('d-none');
			$("#contactEmail").addClass('is-invalid').removeClass('is-valid');
			errorText+="Wprowadzono błędny Email!";
            error=true;
          }
		   else{
			 $("#contactEmail").removeClass('is-invalid').addClass('is-valid');
			 $("#errorMail").addClass('d-none');
		   }
          }
		  if(contactInfo.value == ""){
            $("#errorInfo").removeClass('d-none');
			$("#contactInfo").addClass('is-invalid').removeClass('is-valid');
            error=true;
          }
		  else{
			 $("#errorInfo").addClass('d-none');
			 $("#contactInfo").addClass('is-valid').removeClass('is-invalid');			 
		  }
          if (!error)return true; 
          else{
			document.getElementById("errorMail").innerHTML = errorText;
            return false;
          }  
		  
        }

		function checkName(){
         var contactName = document.getElementById("contactName");
          if (contactName.value == ""){
			$("#errorName").removeClass('d-none');
			$("#contactName").addClass('is-invalid').removeClass('is-valid');
          } 
		  else{
			 $("#errorName").addClass('d-none');
			 $("#contactName").addClass('is-valid').removeClass('is-invalid');			 
		  }  
        }
		
        function checkEmail(){
         var errorText=""; //komunikat z błędem
         var contactEmail = document.getElementById("contactEmail"); 
		 var error=false;
          if(contactEmail.value == ""){
            $("#errorMail").removeClass('d-none');
			$("#contactEmail").addClass('is-invalid').removeClass('is-valid');
			errorText+="Podanie Emaila jest wymagane!";
            error=true;
          } else
          {
            var email = contactEmail.value;
            var regex = /^[a-zA-Z0-9._-]+@([a-zA-Z0-9.-]+\.)+[a-zA-Z0-9.-]{2,4}$/;
          if(regex.test(email)==false)
          {
			$("#errorMail").removeClass('d-none');
			$("#contactEmail").addClass('is-invalid').removeClass('is-valid');
			errorText+="Wprowadzono błędny Email!";
            error=true;
          }
		   else{
			 $("#contactEmail").removeClass('is-invalid').addClass('is-valid');
			 $("#errorMail").addClass('d-none');
		   }
          }
          if (error){
			document.getElementById("errorMail").innerHTML = errorText; 
		  }
        }
		
				function checkInfo(){
         var contactInfo = document.getElementById("contactInfo");
          if (contactInfo.value == ""){
			$("#errorInfo").removeClass('d-none');
			$("#contactInfo").addClass('is-invalid').removeClass('is-valid');
          } 
		  else{
			 $("#errorInfo").addClass('d-none');
			 $("#contactInfo").addClass('is-valid').removeClass('is-invalid');			 
		  }  
        }
		
	