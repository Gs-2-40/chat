// 1. После логина НИЧЕГО сохранять не нужно. Браузер сделал это сам.

// 2. Запрос делается как обычно
async function fetchMessages() {
    // Браузер сам прикрепит куку "access_token" к этому запросу
    const response = await fetch("/api/messages");
    if (response.status === 401) {
        window.location.href = "/auth";
    }
    const data = await response.json();
}

// Отправка
socket.send(JSON.stringify({ action: "send_msg", to_id: 5, text: "Хей!" }));

// Получение
socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log(data.text);
};