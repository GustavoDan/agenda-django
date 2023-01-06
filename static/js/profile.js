const help = document.querySelector('.register-help')
const original_values = {}
const inputs = document.querySelectorAll('input')
inputs.forEach(input => original_values[input.name] = input.value)

function toggle(event){
    const label = event.target
    const name = label.getAttribute('for').replace('id_', '')
    const input = document.querySelector(`[name=${name}]`)

    input.readOnly = !input.readOnly
    label.classList.toggle('input-action-enabled')

    if (input.readOnly) {
        label.innerText = 'Editar'
        input.value = original_values[input.name]
    }
    else {
        label.innerText = 'Cancelar'
    }
}
