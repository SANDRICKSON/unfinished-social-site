const post_id = "current_post_id";  // ამოიღეთ პოსტ ID
const socket = new WebSocket(`ws://localhost:8000/ws/comments/${post_id}/`);

socket.onopen = function(event) {
    console.log("WebSocket is open now.");
};

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if (data.type === 'comment') {
        // განაახლეთ UI ახალი კომენტარით
        const comment = data.comment;
        document.getElementById("comments-section").innerHTML += `
            <div class="comment">
                <p>${comment.user.username}: ${comment.content}</p>
            </div>`;
    }
    if (data.type === 'reply') {
        // განაახლეთ UI ახალი პასუხით
        const reply = data.reply;
        document.getElementById("replies-section").innerHTML += `
            <div class="reply">
                <p>${reply.user.username}: ${reply.content}</p>
            </div>`;
    }
};

socket.onclose = function(event) {
    console.log("WebSocket closed.");
};

// Comment submission
document.getElementById("comment-form").addEventListener("submit", function(event) {
    event.preventDefault();
    const content = document.getElementById("comment-input").value;
    socket.send(JSON.stringify({
        'action': 'comment',
        'content': content
    }));
});

// Reply submission
document.getElementById("reply-form").addEventListener("submit", function(event) {
    event.preventDefault();
    const content = document.getElementById("reply-input").value;
    const comment_id = document.getElementById("comment-id").value;
    socket.send(JSON.stringify({
        'action': 'reply',
        'content': content,
        'comment_id': comment_id
    }));
});
