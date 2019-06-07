document.addEventListener('DOMContentLoaded', () => {
    // Json load
    function loadJSON(path) {
        return new Promise(function (resolve, reject) {
            var xobj = new XMLHttpRequest();
            xobj.overrideMimeType("application/json");
            xobj.open('GET', path, true);
            xobj.onreadystatechange = function () {
                if (xobj.readyState == 4 && xobj.status == "200") {
                    resolve(xobj.responseText);
                }
            };
            xobj.send(null);
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

            for (let userId in response.contacts) {
                userId = response.contacts[userId]

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

    /* Chats */
    // View chats
    chatA.addEventListener("click", function (event) {
        event.preventDefault()
        resetView()
        chatListColumnTitle.innerHTML = "Your chats"
        realChatList.classList.remove('is-hidden');
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

            for (let userId in response.contacts) {
                userId = response.contacts[userId]

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

            for (let userId in response.contacts) {
                userId = response.contacts[userId]

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

                loadJSON('account/contacts/remove/' + userId).then(function (response) {
                    if (response.state == 'successful') {
                        success(response.state)
                    } else {
                        bad(response.state)
                    }
                });
            });
        });
    }

    /** Change title */
    /* Title click listener */
    chatTitle.addEventListener('click', function(event) {
        event.preventDefault();
        chatTitle.querySelector('span').classList.add('is-hidden');
        chatTitle.querySelector('div').classList.remove('is-hidden');
    });

    /* Confirm button title listener */
    changeTitle.addEventListener('click', function (event) {
        event.preventDefault();

        chatId = chatTitle.dataset.id;
        newTitle = chatTitle.querySelector('div input').value;

        loadJSON('chat/change/title/' + chatId + '/' + newTitle).then(function (response) {
            chatTitle.querySelector('span').classList.remove('is-hidden');
            chatTitle.querySelector('div').classList.add('is-hidden');
            chatTitle.querySelector('div input').value = "";    
        });

        event.stopPropagation()
    });
});