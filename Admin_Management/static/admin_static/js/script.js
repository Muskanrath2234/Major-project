const roomName = JSON.parse(document.getElementById('room-name').textContent);
const user = JSON.parse(document.getElementById('user').textContent);
const conversation = document.getElementById("conversation");
const sendButton = document.getElementById("send");
const inputField = document.getElementById("comment");

// WebSocket protocol setup
const protocol = window.location.protocol === "https:" ? "wss://" : "ws://";
const chatSocket = new WebSocket(protocol + window.location.host + "/ws/chat/" + roomName + "/");

// Fetch chat history from the server
function fetchChatHistory() {
    fetch(`/chat/history/${roomName}/`)
        .then(response => response.json())
        .then(data => {
            data.messages.forEach(messageData => {
                displayMessage(messageData);
            });
        })
        .catch(error => {
            console.error('Error fetching chat history:', error);
        });
}

function displayMessage(data) {
    const message_type = data.what_is_it;
    let message;

    if (message_type === "text") {
        message = data.message;
    } else if (message_type === "image") {
        message = `<img width="200" height="200" src="${data.message}">`;
    } else if (message_type === "audio") {
        message = `<audio style="width:250px;" controls><source src="${data.message}" type="audio/mpeg">Your browser does not support the audio element.</audio>`;
    } else if (message_type === "video") {
        message = `<video width="320" height="240" controls><source src="${data.message}" type="video/mp4">Your browser does not support the video tag.</video>`;
    }

    const messageHtml = user === data.user
        ? `<div class="row message-body">
              <div class="col-sm-12 message-main-sender">
                  <div class="sender">
                      <div class="message-text">${message}</div>
                      <span class="message-time pull-right">${data.created_date}</span>
                  </div>
              </div>
          </div>`
        : `<div class="row message-body">
              <div class="col-sm-12 message-main-receiver">
                  <div class="receiver">
                      <div class="message-text">${message}</div>
                      <span class="message-time pull-right">${data.created_date}</span>
                  </div>
              </div>
          </div>`;

    conversation.innerHTML += messageHtml;
    conversation.scrollTop = conversation.scrollHeight;
}

document.getElementById("hiddeninput").addEventListener("change", handleFileSelect, false);

function handleFileSelect(event) {
    var fileInput = document.getElementById("hiddeninput");
    var file = fileInput.files[0];

    if (!file) {
        console.error("No file selected.");
        return;
    }

    getBase64(file, file.type);
}

function getBase64(file, fileType) {
    var type = fileType.split("/")[0];
    var reader = new FileReader();

    reader.readAsDataURL(file);

    reader.onload = function() {
        chatSocket.send(JSON.stringify({
            "what_is_it": type,
            "message": reader.result
        }));
    };

    reader.onerror = function(error) {
        console.error('Error: ', error);
    };
}

const startStop = document.getElementById("record");
let isRecord = false;
let mediaRecorder;
let dataArray = [];
let stream;

startStop.onclick = () => {
    if (isRecord) {
        stopRecord();
        startStop.style = "";
        isRecord = false;
    } else {
        startRecord();
        startStop.style = "color: red";
        isRecord = true;
    }
};

function startRecord() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(streamObj => {
            stream = streamObj;
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();
            dataArray = [];

            mediaRecorder.ondataavailable = function (e) {
                dataArray.push(e.data);
            };

            mediaRecorder.onstop = function (e) {
                let audioData = new Blob(dataArray, { 'type': 'audio/mp3' });
                dataArray = [];
                getBase64(audioData, audioData.type);

                stream.getTracks().forEach(track => {
                    if (track.readyState === 'live' && track.kind === 'audio') {
                        track.stop();
                    }
                });
            };
        })
        .catch(err => {
            console.error('The following error occurred: ' + err);
        });
}

function stopRecord() {
    mediaRecorder.stop();
}

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    displayMessage(data);
};

chatSocket.onclose = function(e) {
    console.error("Socket unexpectedly closed.");
};

inputField.focus();

inputField.onkeyup = function(e) {
    if (e.keyCode === 13) {
        sendButton.click();
    }
};

sendButton.onclick = function(e) {
    const message = inputField.value;
    chatSocket.send(JSON.stringify({
        "what_is_it": "text",
        "message": message
    }));
    inputField.value = '';
};

$(function(){
    $(".heading-compose").click(function() {
        $(".side-two").css({
            "left": "0"
        });
    });

    $(".newMessage-back").click(function() {
        $(".side-two").css({
            "left": "-100%"
        });
    });
});

function toggleDropdown() {
    var dropdown = document.getElementById("dropdownMenu");
    if (dropdown.style.display === "none" || dropdown.style.display === "") {
        dropdown.style.display = "block";
    } else {
        dropdown.style.display = "none";
    }
}

window.onclick = function(event) {
    if (!event.target.matches('.fa-ellipsis-v')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.style.display === "block") {
                openDropdown.style.display = "none";
            }
        }
    }
};

document.addEventListener('DOMContentLoaded', function() {
    fetchChatHistory();  // Fetch and display chat history on page load

    const searchText = document.getElementById('searchText');
    const noUserFound = document.getElementById('noUserFound');
    
    searchText.addEventListener('input', function() {
        const filter = searchText.value.toLowerCase();
        const rows = document.querySelectorAll('.sideBar-body');
        let matchFound = false;

        rows.forEach(row => {
            const nameElement = row.querySelector('.sideBar-name .name-meta');
            if (nameElement && nameElement.innerText.toLowerCase().includes(filter)) {
                row.style.display = '';
                row.parentNode.prepend(row);
                matchFound = true;
            } else {
                row.style.display = 'none';
            }
        });

        if (matchFound) {
            noUserFound.style.display = 'none';
        } else {
            noUserFound.style.display = 'block';
        }
    });
})

document.addEventListener('DOMContentLoaded', function() {
    const deleteChatLink = document.getElementById('delete-chat');
    if (deleteChatLink) {
        deleteChatLink.addEventListener('click', function(event) {
            event.preventDefault(); // Default action ko rokte hain

            // Confirmation pop-up
            const userConfirmed = confirm("Are you sure you want to delete this chat? This action cannot be undone.");

            if (userConfirmed) {
                const roomId = deleteChatLink.getAttribute('data-room-id'); // room ID ko fetch karte hain

                // Fetch API ke through GET request
                fetch(`/chat/room/${roomId}/delete/`, {
                    method: 'GET',
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'Chat deleted') {
                        alert('Chat has been deleted.');
                        window.location.href = "{% url 'index' %}"; // Redirect to index or another page
                    } else {
                        alert('Failed to delete chat.');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred while deleting the chat.');
                });
            }
        });
    }
});
document.getElementById('contact-info-link').addEventListener('click', function(event) {
    event.preventDefault();

    // AJAX call to fetch the profile data
    fetch('/profile/{{ room.id }}/')
        .then(response => response.json())
        .then(data => {
            // Data ko modal me inject karna
            document.getElementById('profile-username').textContent = data.username + "'s Profile";
            document.getElementById('profile-email').textContent = "Email: " + data.email;
            document.getElementById('profile-contact-number').textContent = "Contact Number: " + data.contact_number;
            document.getElementById('profile-address').textContent = "Address: " + data.address;
            document.getElementById('profile-age').textContent = "Age: " + data.age;
            document.getElementById('profile-img').src = data.profile_img_url;

            // Modal ko show karna
            document.getElementById('profile-modal').style.display = 'block';
        });
});

// Close button functionality
document.querySelector('.close-btn').addEventListener('click', function() {
    document.getElementById('profile-modal').style.display = 'none';
});

// Close modal on outside click
window.addEventListener('click', function(event) {
    if (event.target == document.getElementById('profile-modal')) {
        document.getElementById('profile-modal').style.display = 'none';
    }
});
