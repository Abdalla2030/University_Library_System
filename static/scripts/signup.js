const signupForm = document.getElementById('signupForm')
const firstName = document.getElementById('id_first_name')
const lastName = document.getElementById('id_last_name')
const username = document.getElementById('id_username')
const password = document.getElementById('id_password')
const confirmPassword = document.getElementById('id_confirmPassword')

const csrf = document.getElementsByName('csrfmiddlewaretoken')

const url = ''

const errorsUL = document.getElementById('specErrorList')

signupForm.addEventListener('submit', event => {
    event.preventDefault()

    isValidForm = signupForm.getAttribute('data-valid')
    if (isValidForm == 'false' || isValidForm == false) {
        return
    }

    errorsUL.innerHTML = ''
    errorsUL.style.display = 'none'

    const formData = new FormData()
    formData.append('csrfmiddlewaretoken', csrf[0].value)
    formData.append('first_name', firstName.value)
    formData.append('last_name', lastName.value)
    formData.append('username', username.value)
    formData.append('password', password.value)
    formData.append('confirmPassword', confirmPassword.value)


    $.ajax({
        type: 'POST',
        url: url,
        enctype: 'multipart/form-data',
        data: formData,
        success: response => {
            clearForm()
            document.location.pathname = response
        },
        error: response => {
            let errors = JSON.parse(response.responseText)['errors'][0]
            handelErrors(errors)
        },
        cache: false,
        contentType: false,
        processData: false
    })
})

function clearForm(){
    firstName.value = ''
    lastName.value = ''
    username.value = ''
    password.value = ''
    confirmPassword.value = ''
}

function handelErrors(errorsList){
    errorsUL.style.display = 'block'
    errorsList.forEach(err => {
        errorsUL.innerHTML += `<li>${err}</li>`
    })
}