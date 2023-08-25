class Chatbox {
    constructor() {
       this.args = {
           openButton: document.querySelector('.chatbox__button button'),
           chatBox: document.querySelector('.chatbox__support'),
           sendButton: document.querySelector('.send__button'),
       };
       this.state = false;
       this.messages = [];
    }
 
    display() {
        const { openButton, chatBox, sendButton } = this.args;
 
        openButton.addEventListener('click', () => this.toggleState(chatBox));
        sendButton.addEventListener('click', () => this.onSendButton(chatBox));
 
        const node = chatBox.querySelector('input');
        node.addEventListener('keyup', (event) => {
            if (event.key === 'Enter') {
                this.onSendButton(chatBox);
            }
        });
    }
 
    toggleState(chatBox) {
        this.state = !this.state;
        if (this.state) {
            chatBox.classList.add('chatbox--active');
        } else {
            chatBox.classList.remove('chatbox--active');
        }
    }

    typeMessage(message, msgObj, chatBox) {
        let currentCharacterIndex = 0;
        const typingInterval = 50; // Adjust this value for typing speed
        const typingTimer = setInterval(() => {
            const partialMessage = message.substring(0, currentCharacterIndex + 1);
            msgObj.message = partialMessage;
            this.updateChatText(chatBox);

            currentCharacterIndex++;

            if (currentCharacterIndex === message.length) {
                clearInterval(typingTimer);
                this.updateChatText(chatBox);
            }
        }, typingInterval);
    }
 
    onSendButton(chatBox) {
        const textField = chatBox.querySelector('input');
        const text1 = textField.value;
        
        if (text1.trim() === "") {
            return;
        }
        
        const msg1 = { name: "User", message: text1 };
        this.messages.push(msg1);
 
        fetch($SCRIPT_ROOT + '/predict', {
            method: 'POST',
            body: JSON.stringify({ message: text1 }),
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json'
            },
        })
        .then(response => response.json())
        .then(data => {
            const msg2 = { name: "HelpR", message: '' };
            this.messages.push(msg2);

            this.typeMessage(data.answer, msg2, chatBox);

            textField.value = '';
        })
        .catch(error => {
            console.error('Error:', error);
            this.updateChatText(chatBox);
            textField.value = '';
        });
    }
 
    updateChatText(chatBox) {
        let html = '';
        this.messages.slice().reverse().forEach(item => {
            if (item.name === 'HelpR') {
                html += `<div class="messages__item messages__item--operator">${item.message}</div>`;
            } else {
                html += `<div class="messages__item messages__item--visitor">${item.message}</div>`;
            }
        });
        const chatMessage = chatBox.querySelector('.chatbox__messages');
        chatMessage.innerHTML = html;
    }
}
 
const chatbox = new Chatbox();
chatbox.display();
