const user_id = "current_user_id";  // მომხმარებლის ID აიღე საიტზე
const socket = new WebSocket(`ws://localhost:8000/ws/notifications/`);

socket.onopen = function(event) {
    console.log("WebSocket is open now.");
};

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log("Received notification: ", data.message);
    // შეიძლება ახლებური შეტყობინება გამოჩნდეს მომხმარებლის ინტერფეისში
};

socket.onclose = function(event) {
    console.log("WebSocket closed.");
};
