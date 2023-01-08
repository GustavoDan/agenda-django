let messages = document.querySelectorAll('.message-container span')

messages.forEach(message => {
    setTimeout(() => message.classList.add('fade-out'), 2000)
})
