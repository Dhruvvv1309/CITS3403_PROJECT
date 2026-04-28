const users = [
  { name: "Dhruv", bio: "Espresso lover ☕", coffee: "Espresso", cafe: "Starbucks", public: true },
  { name: "Winston", bio: "Latte addict 🥛", coffee: "Latte", cafe: "Starbucks", public: true },
  { name: "Hadia", bio: "Cold brew fan ❄️", coffee: "Cold Brew", cafe: "Local Cafe", public: true }
];

const userList = document.getElementById("userList");

// 🔹 Render users
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

          <a href="user.html?user=${user.name}" class="btn btn-primary mb-2">
            View Journal
          </a>

          <button class="btn btn-outline-dark" onclick="matchUser('${user.name}')">
            ☕ Match
          </button>
        </div>
      </div>
    `;
  });
}

// 🔹 Initial load
renderUsers(users);

// 🔍 SEARCH
document.getElementById("searchUser").addEventListener("input", function() {
  const value = this.value.toLowerCase();

  const filtered = users.filter(user =>
    user.name.toLowerCase().includes(value)
  );

  renderUsers(filtered);
});

// MATCH FILTER SYSTEM
function findMatch() {
  const type = document.getElementById("coffeeType").value;
  const cafe = document.getElementById("cafePref").value.toLowerCase();

  const results = users.filter(user =>
    (!type || user.coffee === type) &&
    (!cafe || user.cafe.toLowerCase().includes(cafe))
  );

  const container = document.getElementById("matchResults");
  container.innerHTML = "";

  if (results.length === 0) {
    container.innerHTML = `<p style="color:#7a6550;">No matches found</p>`;
    return;
  }

  results.forEach(user => {
    const matchScore = Math.floor(Math.random() * 40) + 60;

    container.innerHTML += `
      <div class="col-md-4 mb-2">
        <div class="card p-2">
          <h6>${user.name}</h6>
          <p>${user.coffee} • ${user.cafe}</p>
          <p><strong>${matchScore}% Match ☕</strong></p>
        </div>
      </div>
    `;
  });
}

//  INDIVIDUAL MATCH BUTTON
function matchUser(name) {
  const score = Math.floor(Math.random() * 40) + 60;
  alert(`You and ${name} have a ${score}% coffee match ☕`);
}