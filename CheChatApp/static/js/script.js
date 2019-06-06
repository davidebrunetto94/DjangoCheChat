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

    var addFriend = document.getElementById('addFriend')

    var newChatA = document.querySelector('#newChatA') // new chat ahref
    var chatA = document.querySelector('#chatA'); // list chat href
    var newChatGroupA = document.querySelector('#newChatGroupA'); // new chat group ahref
    var addressBookA = document.getElementById('addressBookA')  //address book href
    var addFriendA = document.querySelector('#addFriendA a') //add friend href

    var done = document.getElementById('done');
    var somethingBad = document.getElementById('somethingBad');

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
        done.classList.remove('is-hidden')
        done.innerHTML = message
    }

    // Bad box (chatlist)
    function bad(message) {
        somethingBad.classList.remove('is-hidden');
        somethingBad.innerHTML = message;
    }

    //New chat
    newChatA.addEventListener("click", function (event) {
        event.preventDefault()
        resetView()
        chatListColumnTitle.innerHTML = "New chat";
        newChat.classList.remove('is-hidden');
    });

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

    //View chats
    chatA.addEventListener("click", function (event) {
        event.preventDefault()
        resetView()
        chatListColumnTitle.innerHTML = "Your chats"
        realChatList.classList.remove('is-hidden');
    });

    //New chat group
    newChatGroupA.addEventListener("click", function (event) {
        event.preventDefault()
        resetView();
        newChatGroup.classList.remove('is-hidden');
        chatListColumnTitle.innerHTML = "New group chat"
    });

    document.querySelector('#startGroupChat').addEventListener("click", function () {
        var users = document.querySelectorAll('.checkUser:checked');
        var title = document.getElementById('groupChatTitle').value;

        // Create new chat
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

    // Address book
    addressBookA.addEventListener("click", function (event) {
        event.preventDefault();
        resetView();

        chatListColumnTitle.innerHTML = "Your friends"

        document.getElementById('addFriendA').classList.remove('is-hidden')

        addressBook.classList.remove('is-hidden')
    });

    addFriendA.addEventListener("click", function (event) {
        event.preventDefault();
        resetView();

        chatListColumnTitle.innerHTML = "Add an user"

        addFriend.classList.remove('is-hidden')
    });
});