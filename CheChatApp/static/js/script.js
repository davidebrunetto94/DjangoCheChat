document.addEventListener('DOMContentLoaded', () => {
    // Json load
    function loadJSON(path, method = 'GET', params = null) {
        return new Promise(function (resolve, reject) {
            var xobj = new XMLHttpRequest();
            xobj.open(method, path, true);

            if (method == 'POST') {
                xobj.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
            } else {
                xobj.overrideMimeType("application/json");
            }

            xobj.onreadystatechange = function () {
                if (xobj.readyState == 4 && xobj.status == "200") {
                    resolve(xobj.responseText);
                }
            };
            xobj.send(params);
        });
    }

    var chatListColumnTitle = document.querySelector('#chatListColumnTitle')
    var realChatList = document.querySelector('#realChatList')

    var newChat = document.querySelector('#newChat')
    var newChatGroup = document.getElementById('newChatGroup')

    var addressBook = document.getElementById('addressBook')
    var addressList = document.getElementById('addressList')

    var addFriend = document.getElementById('addFriend')
    var addFriendButton = document.getElementById('addFriendButton')

    var newChatA = document.querySelector('#newChatA') // new chat ahref
    var chatA = document.querySelector('#chatA'); // list chat href
    var newChatGroupA = document.querySelector('#newChatGroupA'); // new chat group ahref
    var addressBookA = document.getElementById('addressBookA')  //address book href
    var addFriendA = document.querySelector('#addFriendA a') //add friend href

    var done = document.getElementById('done');
    var somethingBad = document.getElementById('somethingBad');

    var chatTitle = document.getElementById('chatTitle')
    var changeTitle = document.getElementById('changeTitle')

    var chatList = document.getElementById('chatList')
    var chatMessages = document.getElementById('chatMessages')
    var deleteChatA = document.getElementById('deleteChatA')

    var newMessageInput = document.getElementById('newMessageInput')

    var addFriendToChat = document.getElementById('addFriendToChat');
    var addFriendToChatA = document.getElementById('addFriendToChatA');
    var addChatFriendButton = document.getElementById('addChatFriendButton')

    // Reset all view
    function resetView() {
        realChatList.classList.add('is-hidden');

        newChat.classList.add('is-hidden');

        newChatGroup.classList.add('is-hidden');

        done.classList.add('is-hidden')
        somethingBad.classList.add('is-hidden');

        addressBook.classList.add('is-hidden');
        document.getElementById('addFriendA').classList.add('is-hidden');

        addFriend.classList.add('is-hidden')

        addFriendToChat.classList.add('is-hidden');
    }

    // Success box (chatlist)
    function success(message) {
        somethingBad.classList.add('is-hidden')
        done.classList.remove('is-hidden')
        done.innerHTML = message
    }

    // Bad box (chatlist)
    function bad(message) {
        done.classList.add('is-hidden')
        somethingBad.classList.remove('is-hidden');
        somethingBad.innerHTML = message;
    }

    // New chat
    newChatA.addEventListener("click", function (event) {
        event.preventDefault()
        resetView()
        chatListColumnTitle.innerHTML = "New chat";
        newChat.classList.remove('is-hidden');

        loadFriendsSingleChat();
    });

    // Load friends single chat
    function loadFriendsSingleChat() {
        document.getElementById('selectUserToChat').innerHTML = "<option>Select user</option>";

        loadJSON('account/contacts/').then(async function (response) {
            response = JSON.parse(response);

            for (let userId of response.contacts) {
                await loadJSON('users/get/' + userId).then(function (response) {
                    response = JSON.parse(response)

                    document.getElementById('selectUserToChat').innerHTML += '<option value="' + userId + '"> ' + response.username + ' </option>'
                });
            }
        });
    }

    // Start chat button listener
    document.querySelector('#startChat').addEventListener("click", function () {
        var e = document.getElementById("selectUserToChat");
        var userId = e.options[e.selectedIndex].value;

        loadJSON('chat/new').then(function (response) {
            response = JSON.parse(response)

            if (response.state == 'successful') {
                loadJSON('chat/add/participant/' + userId + '/' + response.id).then(function (response) {
                    response = JSON.parse(response)

                    if (response.state == 'successful') {
                        success(response.state);
                    } else {
                        bad(response.state);
                    }
                });
            } else {
                bad(response.state);
            }
        });
    });

    /* Chat group */
    // Create chat group click listener
    newChatGroupA.addEventListener("click", function (event) {
        event.preventDefault()
        resetView();
        newChatGroup.classList.remove('is-hidden');
        chatListColumnTitle.innerHTML = "New group chat"

        loadFriendsGroupChat();
    });

    // Create a new group chat
    document.querySelector('#startGroupChat').addEventListener("click", function () {
        var users = document.querySelectorAll('.checkUser:checked');
        var title = document.getElementById('groupChatTitle').value;

        loadJSON('chat/new/' + title).then(async function (response) {
            response = JSON.parse(response)

            if (response.state == 'successful') {
                for (let userId of users) {
                    // Add all the selected user to the chat
                    await loadJSON('chat/add/participant/' + userId.value + '/' + response.id).then(function (response) {
                        response = JSON.parse(response)

                        if (response.state == 'successful') {
                            success(response.state);
                            title = ""
                        } else {
                            bad(response.state);
                        }
                    });
                }
            } else {
                bad(response.state);
            }
        });

        document.getElementById('groupChatTitle').value = ""
    });

    // Load friends group chat
    function loadFriendsGroupChat() {
        document.getElementById('checkAddFriends').innerHTML = "";

        loadJSON('account/contacts/').then(async function (response) {
            response = JSON.parse(response);

            for (let userId of response.contacts) {
                await loadJSON('users/get/' + userId).then(function (response) {
                    response = JSON.parse(response)

                    document.getElementById('checkAddFriends').innerHTML += `
                <label class="checkbox">
                    <input type="checkbox" class="checkUser" value="` + userId + `"> ` + response.username + `
                </label>`;
                });
            }
        });
    }

    /* Address book */
    // Address book click listener
    addressBookA.addEventListener("click", function (event) {
        event.preventDefault();
        resetView();

        chatListColumnTitle.innerHTML = "Your friends"

        document.getElementById('addFriendA').classList.remove('is-hidden')

        addressBook.classList.remove('is-hidden')

        updateAdressBook()
    });

    // Update address list on adressbook
    async function updateAdressBook() {
        addressList.innerHTML = ""
        await loadJSON('account/contacts/').then(async function (response) {
            response = JSON.parse(response)

            for (let userId of response.contacts) {
                await loadJSON('users/get/' + userId).then(function (response) {
                    response = JSON.parse(response)

                    addressList.innerHTML += `
                <li>
                    <div class="columns">
                        <div class="column is-2">
                            <figure class="image is-48x48">
                                <img src="` + response.thumbnail + `" alt="avatar" class="is-rounded">
                            </figure>
                        </div>
                        <div class="column">
                            <div class="content">
                                <div class="user-info">
                                    <h3 class="is-size-6"> ` + response.username + `</h3>
                                    <span class="has-text-grey-light is-size-7">
                                        <a class="deleteFriend" data-id="` + userId + `" href="">
                                            <i class="fas fa-user-minus"></i>
                                        </a>
                                    </span>
                                </div>
                                <p class="has-text-grey-light">Last access: ` + response.lastlogin + `</p>
                            </div>
                        </div>
                    </div>
                </li>`;

                });
            }
        });

        deleteFriendListener();
    }

    // Add friends listener
    addFriendA.addEventListener("click", function (event) {
        event.preventDefault();
        resetView();

        chatListColumnTitle.innerHTML = "Add an user"

        addFriend.classList.remove('is-hidden')
    });

    // Add friends button listener
    addFriendButton.addEventListener("click", function (event) {
        event.preventDefault();

        username = document.getElementById('friendName').value;

        loadJSON('users/get/id/' + username).then(function (response) {
            response = JSON.parse(response)

            if (response.state == 'successful') {
                loadJSON('account/contacts/add/' + response.id).then(function (response) {
                    response = JSON.parse(response)

                    if (response.state == 'successful') {
                        success(response.state)
                    } else {
                        bad(response.state)
                    }
                });
            } else {
                bad(response.state)
            }
        });

        document.getElementById('friendName').value = ""
    });

    // Create delete friend listener
    function deleteFriendListener() {
        var classes = document.querySelectorAll('.deleteFriend');

        Array.from(classes).forEach(function (element) {
            element.addEventListener("click", function (event) {
                event.preventDefault();

                userId = element.dataset.id;

                loadJSON('account/contacts/delete/' + userId).then(function (response) {
                    response = JSON.parse(response)

                    if (response.state == 'successful') {
                        success(response.state);
                        updateAdressBook();
                    } else {
                        bad(response.state);
                    }
                });
            });
        });
    }

    /** Change title */
    // Title click listener 
    chatTitle.addEventListener('click', function (event) {
        event.preventDefault();
        chatTitle.querySelector('span').classList.add('is-hidden');
        chatTitle.querySelector('div').classList.remove('is-hidden');
    });

    // Confirm button title listener
    changeTitle.addEventListener('click', function (event) {
        event.preventDefault();

        chatId = chatTitle.dataset.id;
        newTitle = chatTitle.querySelector('div input').value;

        loadJSON('chat/change/title/' + chatId + '/' + newTitle).then(function (response) {
            chatTitle.querySelector('span').classList.remove('is-hidden');
            chatTitle.querySelector('div').classList.add('is-hidden');
            chatTitle.querySelector('div input').value = "";
            updateChatList();
            updateTitle(chatId)
        });

        event.stopPropagation()
    });

    /* Chats */
    // View chats
    chatA.addEventListener("click", function (event) {
        event.preventDefault()
        resetView()
        chatListColumnTitle.innerHTML = "Your chats"
        realChatList.classList.remove('is-hidden');
        updateChatList();
    });

    // Remove user from participiants
    deleteChatA.addEventListener('click', function (event) {
        event.preventDefault();

        loadJSON('chat/delete/participant/' + chatTitle.dataset.id).then(async function (response) {
            response = JSON.parse(response)
            document.querySelector('#noChats .title').innerHTML = "You're out!"
            document.getElementById('noChats').classList.remove('is-hidden');
            document.querySelector('.send').classList.add('is-hidden');
            document.querySelector('.messages').classList.add('is-hidden');
            document.querySelector('.level').classList.add('is-hidden');

            updateChatList();
        });
    });

    /* Chat list */
    async function updateChatList() {
        //Get user chat
        await loadJSON('user/chat/').then(async function (response) {
            response = JSON.parse(response)
            chatList.innerHTML = "";

            if (response.chat == undefined) {
                return;
            }

            // Get info about all chat
            for (let id of response.chat) {
                await loadJSON('chat/info/' + id.id).then(async function (response) {
                    response = JSON.parse(response)
                    var title = response.title;
                    var isGroup = response.isGroup;

                    // Get last message
                    await loadJSON('chat/get/last/' + id.id).then(async function (response) {
                        response = JSON.parse(response)

                        var lastMessage = response.message;
                        var timestamp = new Date(response.message.timestamp);
                        var thumbnail = ""

                        if (isNaN(timestamp)) {
                            timestamp = new Date();
                        }

                        if (lastMessage.length == 0) {
                            lastMessage = "No messages";
                        } else {
                            lastMessage = lastMessage.text;
                        }

                        if (isGroup == "false") {
                            // The username of the other user should be shown if it's not a group chat
                            await loadJSON('user/get/current').then(async function (response) {
                                userId = JSON.parse(response).id;

                                await loadJSON('chat/get/participants/' + id.id).then(async function (response) {
                                    for (let user of JSON.parse(response).participants) {
                                        if (userId != user.id) {
                                            await loadJSON('users/get/' + user.id).then(async function (response) {
                                                title = user.username;
                                                thumbnail = JSON.parse(response).thumbnail;
                                            });
                                        }
                                    }
                                });
                            });
                        }

                        chatList.innerHTML += `
                    <li>
                        <a href="" class="chatListA" data-id="` + id.id + `">
                            <div class="columns">
                                <div class="column is-2` + ((isGroup == "true") ? ` is-hidden`  : ``)  + `">
                                    <figure class="imageis-square">
                                        <img src="` + thumbnail + `" alt="avatar" class="is-rounded">
                                    </figure>
                                </div>
                                <div class="column">
                                    <div class="content">
                                        <div class="user-info">
                                            <h3 class="is-size-6">` + title + `</h3>
                                            <span class="has-text-grey-light is-size-7">` + timestamp.toLocaleDateString("default", { day: '2-digit', month: "short" }) + `</span>
                                        </div>
                                        <p class="has-text-grey-light">` + lastMessage + `</p>
                                    </div>
                                </div>
                            </div>
                        </a>
                    </li>
                        `;
                        openChatListener()
                    });
                });
            }
        });
    }
    updateChatList();

    // Create open chat listener
    function openChatListener() {
        var classes = document.querySelectorAll('.chatListA');

        Array.from(classes).forEach(function (element) {
            element.addEventListener("click", function (event) {
                event.preventDefault();

                chatId = element.dataset.id;

                updateChatMessages(chatId);
                updateTitle(chatId);

                document.getElementById('noChats').classList.add('is-hidden');
                document.querySelector('.send').classList.remove('is-hidden');
                document.querySelector('.messages').classList.remove('is-hidden');
                document.querySelector('.level').classList.remove('is-hidden');
            });
        });
    }

    //Update chat messages
    function updateChatMessages(chatId) {
        chatMessages.innerHTML = "";

        loadJSON('chat/messages/' + chatId).then(async function (response) {
            response = JSON.parse(response)
            messages = response.messages;

            await loadJSON('user/get/current').then(async function (response) {
                var userId = JSON.parse(response).id;

                for (let chat of messages) {
                    await loadJSON('users/get/' + chat.sender).then(async function (response) {
                        response = JSON.parse(response);

                        isUser = ((userId == chat.sender) ? 'class="my-message"' : '');
                        chatMessages.innerHTML += `
            <li ` + isUser + `>
                <figure class="image is-32x32">
                    <img src="` + response.thumbnail + `" alt="avatar" class="is-rounded">
                </figure>
                <div class="content">
                    <div class="message">
                        <div class="bubble">
                            <p>` + chat.text + `</p>
                        </div>
                    </div>
                    <span class="has-text-grey-light">` + (new Date(chat.timestamp)).toLocaleTimeString("default", { hour: "2-digit", minute: "2-digit" }) + `</span>
                </div>
            </li>`;
                    });
                }

                // Scroll to the last message
                document.querySelector('.messages').scrollTop = document.querySelector('.messages').scrollHeight;
            });
        });

        newMessageInput.setAttribute('data-id', chatId);
        chatTitle.setAttribute('data-id', chatId);
    }

    // Send message input
    newMessageInput.addEventListener("keypress", function (e) {
        var key = e.which || e.keyCode || 0;

        // On enter press
        if (key === 13) {
            var chatId = newMessageInput.dataset.id;

            loadJSON('chat/add/message/', 'POST', 'id=' + chatId + '&message_body=' + encodeURI(newMessageInput.value)).then(async function (response) {
                updateChatMessages(chatId);
                updateChatList();
                newMessageInput.value = ''
            });
        }
    });

    // Update chat title
    function updateTitle(id) {
        loadJSON('chat/info/' + id).then(function (response) {
            response = JSON.parse(response)
            var title = response.title;
            var isGroup = response.isGroup;

            if (isGroup == "false") {
                // The username of the other user should be shown if it's not a group chat
                loadJSON('user/get/current').then(async function (response) {
                    userId = JSON.parse(response).id;

                    await loadJSON('chat/get/participants/' + id).then(async function (response) {
                        for (let user of JSON.parse(response).participants) {
                            if (userId != user.id) {
                                await loadJSON('users/get/' + user.id).then(async function (response) {
                                    response = JSON.parse(response)
                                    var title = response.username;
                                    var lastOnline = response.lastlogin;
                                    var thumbnail = response.thumbnail

                                    //Change chat title
                                    chatTitle.querySelector('span').innerHTML = title;
                                    document.getElementById('thumbnailChat').classList.remove('is-hidden');

                                    document.getElementById('lastOnline').innerHTML = 'Last online: ' + lastOnline;
                                    document.getElementById('thumbnailChat').src = thumbnail;
                                });
                            }
                        }
                    });
                });
            } else {
                document.getElementById('thumbnailChat').classList.add('is-hidden');
                chatTitle.querySelector('span').innerHTML = title;

                // Participants list

                loadJSON('chat/get/participants/' + id).then(async function (response) {
                    participants = JSON.parse(response).participants;

                    participantsList = []

                    Object.keys(participants).forEach(k => {
                        participantsList.push(participants[k].username);
                    });

                    document.getElementById('lastOnline').innerHTML =  participantsList.join(", ");
                });
            }
        });
    }

    // Add friend to chat listener ahref
    addFriendToChatA.addEventListener('click', function (event) {
        event.preventDefault();
        resetView();

        addFriendToChat.classList.remove('is-hidden');
    });

    // Add friend to chat listener button
    addChatFriendButton.addEventListener('click', function () {
        var username = document.getElementById('friendNameChat').value;

        loadJSON('users/get/id/' + username).then(function (response) {
            userId = JSON.parse(response).id;

            loadJSON('chat/add/participant/' + userId + '/' + chatTitle.dataset.id).then(function (response) {
                response = JSON.parse(response);

                if (response.state == 'successful') {
                    success('Friend added!');
                    updateTitle(chatTitle.dataset.id)
                    document.getElementById('friendNameChat').value = ''
                } else {
                    bad(response.state)
                }
            });
        });

    });
});