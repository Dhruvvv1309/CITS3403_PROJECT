let loggedIn = false;

function addComment() {
  if (!loggedIn) {
    alert("Please login to comment");
    return;
  }

  const text = document.getElementById("commentInput").value;

  document.getElementById("commentsList").innerHTML += `
    <p>${text}</p>
  `;
}