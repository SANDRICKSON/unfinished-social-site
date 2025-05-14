const post_id = "current_post_id";  // ამოიღეთ პოსტ ID

const socket = new WebSocket(`ws://localhost:8000/ws/likes/${post_id}/`);

socket.onopen = function(event) {
    console.log("WebSocket is open now.");
};

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    document.getElementById("like-count").innerText = `Likes: ${data.like_count}`;
};

socket.onclose = function(event) {
    console.log("WebSocket closed.");
};

// Like Button Click
document.getElementById("like-button").addEventListener("click", function() {
    socket.send(JSON.stringify({
        'action': 'like'  // or 'unlike'
    }));
});
