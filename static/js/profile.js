const setLabelPosition = (label) => label.style.right = `-${label.clientWidth + 10}px`

const original_values = {}
const help = document.querySelector('.register-help')
const inputs = document.querySelectorAll('input')
const labels = document.querySelectorAll("label")

inputs.forEach(input => original_values[input.name] = input.value)
labels.forEach(setLabelPosition)

function toggle(event) {
    const label = event.target
    const name = label.getAttribute('for').replace('id_', '')
    const input = document.querySelector(`[name=${name}]`)

    input.readOnly = !input.readOnly
    input.value = original_values[input.name]

    label.innerText = input.readOnly ? 'Editar' : 'Cancelar'
    setLabelPosition(label)
}
