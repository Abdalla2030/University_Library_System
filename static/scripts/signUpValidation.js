const errorCon = document.getElementById('specErrorList')

function checkForm(form){
	const firstNameVal = form.first_name.value.trim()
	const lastNameVal = form.last_name.value.trim()
	const usernameVal = form.username.value.trim()
	const passwordVal = form.password.value.trim()
	const confirmPasswordVal = form.confirmPassword.value.trim()

	errorCon.innerHTML = ''
    errorCon.style.display = 'none'

	let isValid = true;

	if (firstNameVal==""){
		showError("First name can't be blank !");
		form.first_name.focus();
		isValid = false; 
	}
	else if(lastNameVal==""){
		showError("Last name can't be blank !");
		form.last_name.focus();
		isValid = false; 
	}
	else if(usernameVal==""){
		showError("Username can't be blank !");
		form.username.focus();
		isValid = false; 
	}
	else if(passwordVal==""){
		showError("Password can't be blank !");
		form.password.focus();
		isValid = false; 
	}
	else if(passwordVal.length < 8){
		showError("Password length can't be less than 8 !");
		form.password.focus();
		isValid = false; 
	}
	else if(confirmPasswordVal==""){
		showError("Confirm password can't be blank !");
		form.confirmPassword.focus();
		isValid = false; 
	}
	else if(passwordVal != confirmPasswordVal){
		showError("Passwords are not matched !");
		form.confirmPassword.focus();
		isValid = false; 
	}

	
	form.setAttribute('data-valid', isValid)
}

function showError(error){
    errorCon.style.display = 'block'
    errorCon.innerHTML = `<li>${error}</li>`
}