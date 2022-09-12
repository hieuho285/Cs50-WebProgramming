document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector('#current-user')) {
        document.querySelector('#user-profile').addEventListener('click', () => profile_page(document.querySelector('#current-user').value));
        document.querySelector('#following-posts').addEventListener('click', () => following_page(document.querySelector('#current-user').value));

    }

    if (document.querySelector('#new-post-submit') !== null) {
        document.querySelector('#new-post-submit').disabled = true;
        document.querySelector('#new-post-body').onkeyup = undisable_submit_button;
        document.querySelector('#new-post').onsubmit = new_post;
    }

    load_default();

});


function following_page(user) {
    document.querySelector('#all-post-page').style.display = 'none';
    document.querySelector('#following-page').style.display = 'block';
    document.querySelector('#user-post').style.display = 'none';
    document.querySelector('#profile').style.display = 'none';

    document.querySelector('#following-page').innerHTML = '';

    fetch(`/following/${user}`)
    .then(response => response.json())
    .then(posts => {
        console.log(posts);
        posts.forEach(post => {
            post_details(post, user);
        })
        if (document.querySelector('#following-page').innerHTML === '') {
            const message = document.createElement('h1');
            message.innerHTML = "You are not following anybody";
            document.querySelector('#following-page').append(message);
        }
    })

    


}

function load_default() {

    document.querySelector('#all-post-page').style.display = 'block';
    document.querySelector('#following-page').style.display = 'none';
    document.querySelector('#user-post').style.display = 'none';
    document.querySelector('#profile').style.display = 'none';


    fetch('/showallpost')
    .then(response => response.json())
    .then(posts => {
        console.log(posts);

        pagination();

        posts.forEach(post => {
            if (document.querySelector('#current-user')) {
                post_details(post, document.querySelector('#current-user').value);
            } else {
                post_details(post, '');  
            }
        });
        
    });        
     
}

function pagination() {
    const nav = document.createElement('nav');

    const pagination = document.createElement('ul');
    pagination.classList.add('pagination');
    nav.append(pagination);

    const items = document.createElement('li');
    items.classList.add('page-item');
    pagination.append(items);

    const links = document.createElement('a');
    links.classList.add('page-link');
    links.innerHTML = "1";
    links.href = "#";

    items.append(links);  

    if (document.querySelector('#all-post-page').style.display === 'block') {
        document.querySelector('#all-post-page').append(nav);
    } else if (document.querySelector('#profile').style.display === 'block') {
        document.querySelector('#profile').append(nav);
    }

}

function profile_page(user) {
    
    document.querySelector('#all-post-page').style.display = 'none';
    document.querySelector('#following-page').style.display = 'none';
    document.querySelector('#profile').style.display = 'block';
    document.querySelector('#user-post').style.display = 'block';

    document.querySelector('#all-post-page').innerHTML = '';
    document.querySelector('#follow-button').innerHTML = '';
    document.querySelector('#user-post').innerHTML = '';
    
    fetch(`/follow/${user}`)
    .then(response => response.json())
    .then(result => {
        
        console.log(result);
        document.querySelector("#follower").innerHTML = result.follower;
        document.querySelector("#following").innerHTML = result.following;
    });

    fetch(`/showprofile/${user}`)
    .then(response => response.json())
    .then(posts => {
        console.log(posts); 
               
        posts.forEach(post => {
            post_details(post, user);                        
        });    
        
        document.querySelector('#user-post').append(document.createElement('hr'));
    });

    if (document.querySelector('#current-user').value !== user) {
        const button = document.createElement('button');
        button.classList.add('btn', 'btn-success', 'btn-rounded', 'text-white', 'text-uppercase', 'font-14');
        button.id = "button-value";
        fetch(`/follow/${user}`)
        .then(response => response.json())
        .then(result => {
            console.log(result);
            button.innerHTML = result.follow;
        });

        document.querySelector('#follow-button').append(button);

        document.querySelector('#follow-button').onclick = function () {
            update_follow(user, button.innerHTML);
        }
    } 

}

function update_follow(user, button) {
    fetch(`/updatefollow/${user}`)
    .then(response => response.json())
    .then(result => {
        console.log(result);
        document.querySelector("#follower").innerHTML = result.follower;
        document.querySelector("#following").innerHTML = result.following;
        if (button === "Follow") {
            document.querySelector('#button-value').innerHTML = "Unfollow";
        } else {
            document.querySelector('#button-value').innerHTML = "Follow";
        }
    });
}

function post_details(post, user) {
    

    

    const border = document.createElement('div');
    border.classList.add('row', 'border', 'rounded', 'mr-3', 'ml-3', 'mb-3');
                
    const name = document.createElement('a');
    name.classList.add('mt-2', 'ml-3', 'col', "user" + post.creator);
    name.href = '#';
    name.innerHTML = post.creator;

    const timestamp = document.createElement('small');
    timestamp.classList.add('ml-3');
    timestamp.innerHTML = post.timestamp;

    const like = document.createElement('button');
    like.classList.add('ml-4', 'mt-1', 'btn', 'btn-primary', 'btn-sm', 'position-relative', 'like-button');
    like.dataset.likeId = post.id;

    const likeValue = document.createElement('text');
    
    likeValue.innerHTML = "Like";
    
    likeValue.dataset.textId = post.id;

    const badge = document.createElement('span');
    badge.classList.add('position-absolute', 'top-0', 'start-100', 'translate-middle', 'badge', 'rounded-pill', 'bg-danger', 'likes');
    badge.innerHTML = post.likes;
    badge.dataset.badgeId = post.id;
    like.append(likeValue, badge);

    const content = document.createElement('input');
    content.classList.add('form-control', 'mt-2', 'mr-4', 'ml-4');
    content.setAttribute('readonly', true);
    content.value = post.body;

    border.append(name, timestamp, content, like);

    if (document.querySelector('#all-post-page').style.display === 'block') {
        document.querySelector('#all-post-page').append(border);
    } else if (document.querySelector('#user-post').style.display === 'block') {
        document.querySelector('#user-post').append(border);
    } else if (document.querySelector('#following-page').style.display === 'block') {
        document.querySelector('#following-page').append(border);
    }
    ;
    

    document.querySelectorAll('.like-button').forEach((button) => {
        button.onclick = function() {
            update_like(button.dataset.likeId, user);
        }
    });

    document.querySelectorAll(`.user${post.creator}`).forEach((button) => {
        button.onclick = function() {
            profile_page(post.creator)
        }
    });
}

function update_like(id, user) {

    if (user === '') {
        location.href = "/login"
    }
    else {
        fetch(`/updatelike/${id}`)
        .then(response => response.json())
        .then(result => {
            console.log(result);

            document.querySelector(`[data-badge-id="${id}"]`).innerHTML = result.likes;

        })
    }

};

function undisable_submit_button() {
    if (document.querySelector('#new-post-body').value.length > 0) {
        document.querySelector('#new-post-submit').disabled = false;
    } else {
        document.querySelector('#new-post-submit').disabled = true;
    }
}

function new_post() {
    fetch('/newpost', {
        method: 'POST',
        body: JSON.stringify({
            body: document.querySelector('#new-post-body').value,
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
    });
    window.location.reload();
    return false;
}


