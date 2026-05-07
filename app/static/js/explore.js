/* explore.js */

const users = [
  { name: "Dhruv",   coffee: "Espresso",   cafe: "March Coffee Studio" },
  { name: "Winston", coffee: "Latte",       cafe: "Telegram Coffee" },
  { name: "Hadia",   coffee: "Cold Brew",   cafe: "Howard's Groove Coffee" },
  { name: "Aarav",   coffee: "Flat White",  cafe: "Smooth Operator Coffee" },
  { name: "Sophie",  coffee: "Cappuccino",  cafe: "La Veen Coffee" },
  { name: "Priya",   coffee: "Mocha",       cafe: "Leeway Coffee" },
];

const events = [
  { name: "Latte Workshop",   venue: "Telegram Coffee",   date: "2026-05-20" },
  { name: "Cold Brew Meetup", venue: "Fremantle Markets", date: "2026-05-25" },
];

const cafes = [
  { name: "March Coffee Studio",    addr: "140 William St",           rating: 4.9, lat: -31.9520, lng: 115.8580 },
  { name: "Leeway Coffee",          addr: "712 Hay Street Mall",       rating: 4.9, lat: -31.9537, lng: 115.8577 },
  { name: "Parkside Coffee",        addr: "2 Church St",               rating: 4.8, lat: -31.9436, lng: 115.8589 },
  { name: "Smooth Operator Coffee", addr: "938 Hay St",                rating: 4.8, lat: -31.9516, lng: 115.8519 },
  { name: "Howard's Groove Coffee", addr: "22 Howard St",              rating: 4.8, lat: -31.9554, lng: 115.8574 },
  { name: "Telegram Coffee",        addr: "State Buildings, Barrack St", rating: 4.7, lat: -31.9555, lng: 115.8604 },
  { name: "La Veen Coffee",         addr: "79 King St",                rating: 4.4, lat: -31.9506, lng: 115.8557 },
  { name: "808 Specialty Coffee",   addr: "236 Lord St",               rating: 4.7, lat: -31.9464, lng: 115.8718 },
];

const coffeeOptions = ["Espresso", "Latte", "Flat White", "Cappuccino", "Cold Brew", "Mocha"];
const cafeOptions   = [...new Set(users.map(u => u.cafe))];

/* ── HELPERS ── */
function getInitials(name) {
  return name.split(" ").map(n => n[0]).join("").substring(0, 2).toUpperCase();
}

function starsHtml(r) {
  return "★".repeat(Math.floor(r)) + (r % 1 >= 0.5 ? "½" : "");
}

let toastTimer = null;
function showToast(msg) {
  const t = document.getElementById("toast");
  t.textContent = msg;
  t.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.classList.remove("show"), 2600);
}

/* ── USERS ── */
function loadUsers() {
  const el = document.getElementById("userList");
  el.innerHTML = users.map((u, i) => `
    <div class="user-card" style="animation: fadeUp 0.4s ease ${0.05 + i * 0.07}s both;"
         onclick="showToast('Opening ${u.name}\'s journal…')">
      <div class="user-initial">${getInitials(u.name)}</div>
      <div class="user-name">${u.name}</div>
      <div class="user-coffee">${u.coffee}</div>
      <span class="user-tag">${u.cafe.split(" ")[0]}</span><br>
      <button class="view-btn" onclick="event.stopPropagation(); showToast('Viewing ${u.name}\'s journal')">
        View Journal
      </button>
    </div>
  `).join("");
}

/* ── EVENTS ── */
function loadEvents() {
  const el = document.getElementById("eventList");
  el.innerHTML = events.map(e => `
    <div class="event-card" onclick="showToast('RSVP\'d to ${e.name}!')">
      <div class="event-name">${e.name}</div>
      <div class="event-venue">${e.venue}</div>
      <div class="event-date">${e.date}</div>
    </div>
  `).join("");
}

function addEvent() {
  const name  = document.getElementById("eventName").value.trim();
  const venue = document.getElementById("eventVenue").value.trim();
  const date  = document.getElementById("eventDate").value;
  if (!name || !venue || !date) { showToast("Please fill all fields ☕"); return; }
  events.unshift({ name, venue, date });
  loadEvents();
  document.getElementById("eventName").value  = "";
  document.getElementById("eventVenue").value = "";
  document.getElementById("eventDate").value  = "";
  showToast("Event created! ☕");
}

/* ── MATCH ── */
function updateMatchOptions() {
  const type = document.getElementById("matchType").value;
  const sel  = document.getElementById("matchValue");
  const opts = type === "coffee" ? coffeeOptions : cafeOptions;
  sel.innerHTML = opts.map(o => `<option value="${o}">${o}</option>`).join("");
  closeMatch();
}

function findMatch() {
  const type    = document.getElementById("matchType").value;
  const val     = document.getElementById("matchValue").value;
  const key     = type === "coffee" ? "coffee" : "cafe";
  const matches = users.filter(u => u[key] === val);

  if (!matches.length) {
    showToast("No matches yet — keep logging! ☕");
    return;
  }

  const pick = matches[Math.floor(Math.random() * matches.length)];
  document.getElementById("matchAvatar").textContent = getInitials(pick.name);
  document.getElementById("matchName").textContent   = pick.name;
  document.getElementById("matchMsg").textContent    =
    type === "coffee"
      ? `You both love ${val}! Time for a coffee date ☕`
      : `You both visit ${val}! Say hello next time 👋`;

  const res = document.getElementById("matchResult");
  res.classList.remove("hidden");
  /* re-trigger animation */
  res.style.animation = "none";
  res.offsetHeight;
  res.style.animation = "";
}

function closeMatch() {
  document.getElementById("matchResult").classList.add("hidden");
}

/* ── DISCOUNTS ── */
function toggleDiscounts(btn) {
  const list = document.getElementById("discountList");
  const open = list.classList.toggle("open");
  list.classList.toggle("hidden", false);   // ensure visible once toggled
  btn.textContent = open ? "🔥 Hide Discounts" : "🔥 View Discounts";
}

/* ── MAP ── */
let mapInstance = null;
const markers = [];

function buildMap() {
  mapInstance = L.map("leaflet-map", {
    center: [-31.9520, 115.8580],
    zoom: 15,
  });

  /* Light/neutral tile that matches the cream palette */
  L.tileLayer("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png", {
    attribution: "&copy; <a href='https://carto.com/'>CARTO</a>",
    maxZoom: 19,
  }).addTo(mapInstance);

  function makeIcon(active) {
    return L.divIcon({
      className: "",
      html: `<div style="
        width:${active ? 18 : 14}px; height:${active ? 18 : 14}px;
        background:${active ? "#c8852e" : "#8a5020"};
        border:2px solid ${active ? "#fff" : "rgba(255,255,255,0.7)"};
        border-radius:50%;
        box-shadow:0 2px 6px rgba(0,0,0,0.3);
      "></div>`,
      iconSize: [active ? 18 : 14, active ? 18 : 14],
      iconAnchor: [active ? 9 : 7, active ? 9 : 7],
    });
  }

  cafes.forEach((cafe, i) => {
    const marker = L.marker([cafe.lat, cafe.lng], { icon: makeIcon(false) })
      .addTo(mapInstance)
      .bindPopup(`
        <div style="font-family:inherit; font-size:13px; min-width:140px; color:#2b1710;">
          <strong style="font-family:'Lora',serif;">${cafe.name}</strong><br>
          <span style="font-size:11px;color:#7a5030;">${cafe.addr}</span><br>
          <span style="color:#c8852e;">${starsHtml(cafe.rating)} ${cafe.rating}</span>
        </div>
      `)
      .on("click", () => setActiveMarker(i));
    markers.push({ marker, makeIcon });
  });

  buildCafeList();
}

function setActiveMarker(idx) {
  const cafe = cafes[idx];
  mapInstance.setView([cafe.lat, cafe.lng], 16, { animate: true });
  markers[idx].marker.openPopup();

  document.querySelectorAll(".cafe-item").forEach((el, i) => {
    el.classList.toggle("active", i === idx);
  });
}

function buildCafeList() {
  const el = document.getElementById("cafeListItems");
  el.innerHTML = cafes.map((c, i) => `
    <div class="cafe-item" onclick="setActiveMarker(${i})">
      <div class="cafe-item-name">${c.name}</div>
      <div class="cafe-item-addr">${c.addr}</div>
      <div>
        <span class="cafe-stars">${starsHtml(c.rating)}</span>
        <span class="cafe-rating-num">${c.rating}</span>
      </div>
    </div>
  `).join("");
}

/* ── INIT ── */
updateMatchOptions();   // populate match dropdown on load
loadUsers();
loadEvents();
buildMap();