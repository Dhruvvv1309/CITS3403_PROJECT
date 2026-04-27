const users = [
  { name: "Dhruv", bio: "Espresso lover ☕", public: true },
  { name: "Winston", bio: "Latte addict 🥛", public: true },
  { name: "Hadia", bio: "Cold brew fan ❄️", public: true }
];

const userList = document.getElementById("userList");

// Render users
function renderUsers(list) {
  userList.innerHTML = "";

  const visibleUsers = list.filter(user => user.public);

  if (visibleUsers.length === 0) {
    userList.innerHTML = `<p style="color:#7a6550;">No users found</p>`;
    return;
  }

  visibleUsers.forEach(user => {
    userList.innerHTML += `
      <div class="col-md-4 mb-3">
        <div class="card p-3">
          <h5>${user.name}</h5>
          <p>${user.bio}</p>

          <a href="user.html?user=${user.name}" class="btn btn-primary">
            View Journal
          </a>
        </div>
      </div>
    `;
  });
}

// Initial load
renderUsers(users);

// SEARCH
document.getElementById("searchUser").addEventListener("input", function() {
  const value = this.value.toLowerCase();

  const filtered = users.filter(user =>
    user.name.toLowerCase().includes(value)
  );

  renderUsers(filtered);
});