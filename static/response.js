function sendResponse(answer) {
  fetch('/send-sms', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ response: answer })
  })
  .then(response => response.json())
  .then(data => {
    if (data.redirect) {
      window.location.href = data.redirect;
    } else {
      alert("Something went wrong.");
    }
  })
  .catch(err => {
    console.error(err);
    alert("Error sending response.");
  });
}
