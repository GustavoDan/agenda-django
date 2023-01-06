let messages = document.querySelectorAll('.message-container span')

messages.forEach(async message => {
    setTimeout(() => message.classList.add('fade-out'), 2000)
})