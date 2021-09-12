const addBookForm = document.getElementById('bookForm')
const ispnInput = document.getElementById('id_ISPN')
const nameInput = document.getElementById('id_name')
const authorInput = document.getElementById('id_author')
const dateInput = document.getElementById('id_publicationDate')
const imgInput = document.getElementById('id_image')

const csrf = document.getElementsByName('csrfmiddlewaretoken')

const url = ''

const errorsUL = document.getElementById('specErrorList')


addBookForm.addEventListener('submit', event => {
    event.preventDefault()
    
    console.log(errorsUL)

    errorsUL.innerHTML = ''
    errorsUL.style.display = 'none'

    const formData = new FormData()
    formData.append('csrfmiddlewaretoken', csrf[0].value)
    formData.append('ISPN', ispnInput.value)
    formData.append('name', nameInput.value)
    formData.append('author', authorInput.value)
    formData.append('publicationDate', dateInput.value)
    formData.append('image', imgInput.files[0])


    $.ajax({
        type: 'POST',
        url: url,
        enctype: 'multipart/form-data',
        data: formData,
        success: response => {
            clearForm()
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
    ispnInput.value = ''
    nameInput.value = ''
    authorInput.value = ''
    dateInput.value = ''
    imgInput.value = ''
}

function handelErrors(errorsList){
    errorsUL.style.display = 'block'
    errorsList.forEach(err => {
        console.log(err)
        errorsUL.innerHTML += `<li>${err}</li>`
    })
}