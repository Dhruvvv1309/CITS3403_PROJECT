/* explore.js */

/* ═══════════════════════════════════════
   MATCH
═══════════════════════════════════════ */

const coffeeOptions = ["Espresso", "Latte", "Flat White", "Cappuccino", "Cold Brew", "Mocha"];
const cafeOptions   = ["March Coffee Studio", "Telegram Coffee", "Howard's Groove Coffee",
                       "Smooth Operator Coffee", "La Veen Coffee", "Leeway Coffee"];

function updateMatchOptions() {
  const type = document.getElementById("matchType").value;
  const sel  = document.getElementById("matchValue");
  const opts = type === "coffee" ? coffeeOptions : cafeOptions;
  sel.innerHTML = opts.map(o => `<option value="${o}">${o}</option>`).join("");
  closeMatch();
}

function findMatch() {
  const type = document.getElementById("matchType").value;
  const val  = document.getElementById("matchValue").value;

  document.getElementById("matchAvatar").textContent = val[0].toUpperCase();
  document.getElementById("matchName").textContent   = val;
  document.getElementById("matchMsg").textContent    =
    type === "coffee"
      ? `Someone nearby loves ${val} too ☕`
      : `Someone else hangs out at ${val}! 👋`;

  const res = document.getElementById("matchResult");
  res.classList.remove("hidden");
  res.style.animation = "none";
  res.offsetHeight;
  res.style.animation = "";
}

function closeMatch() {
  document.getElementById("matchResult").classList.add("hidden");
}

/* ═══════════════════════════════════════
   DISCOUNTS
═══════════════════════════════════════ */

function toggleDiscounts(btn) {
  const list = document.getElementById("discountList");
  const open = list.classList.toggle("open");
  btn.textContent = open ? "🔥 Hide Discounts" : "🔥 View Discounts";
}

/* ═══════════════════════════════════════
   EVENTS
═══════════════════════════════════════ */

let events = [
  { name: "Latte Workshop",   venue: "Telegram Coffee",   date: "2026-05-20" },
  { name: "Cold Brew Meetup", venue: "Fremantle Markets", date: "2026-05-25" },
];

function loadEvents() {
  const el = document.getElementById("eventList");
  el.innerHTML = events.map(e => `
    <div class="event-card">
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

  if (!name || !venue || !date) {
    showToast("Please fill all fields ☕");
    return;
  }

  events.unshift({ name, venue, date });
  loadEvents();

  document.getElementById("eventName").value  = "";
  document.getElementById("eventVenue").value = "";
  document.getElementById("eventDate").value  = "";
  showToast("Event created!");
}

/* ═══════════════════════════════════════
   PERTH CBD MAP
═══════════════════════════════════════ */

const cafes = [
  { name: "March Coffee Studio",    addr: "140 William St",             rating: 4.9, lat: -31.9520, lng: 115.8580 },
  { name: "Leeway Coffee",          addr: "712 Hay Street Mall",         rating: 4.9, lat: -31.9537, lng: 115.8577 },
  { name: "Parkside Coffee",        addr: "2 Church St",                 rating: 4.8, lat: -31.9436, lng: 115.8589 },
  { name: "Smooth Operator Coffee", addr: "938 Hay St",                  rating: 4.8, lat: -31.9516, lng: 115.8519 },
  { name: "Howard's Groove Coffee", addr: "22 Howard St",                rating: 4.8, lat: -31.9554, lng: 115.8574 },
  { name: "Telegram Coffee",        addr: "State Buildings, Barrack St", rating: 4.7, lat: -31.9555, lng: 115.8604 },
  { name: "La Veen Coffee",         addr: "79 King St",                  rating: 4.4, lat: -31.9506, lng: 115.8557 },
  { name: "808 Specialty Coffee",   addr: "236 Lord St",                 rating: 4.7, lat: -31.9464, lng: 115.8718 },
];

let mapInstance = null;
const markers   = [];

function starsHtml(r) {
  return "★".repeat(Math.floor(r)) + (r % 1 >= 0.5 ? "½" : "");
}

function buildMap() {
  mapInstance = L.map("leaflet-map", {
    center: [-31.9520, 115.8580],
    zoom: 15,
  });

  L.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", {
    attribution: "&copy; <a href='https://carto.com/'>CARTO</a>",
    maxZoom: 19,
  }).addTo(mapInstance);

  function makeIcon(active) {
    const size = active ? 18 : 14;
    return L.divIcon({
      className: "",
      html: `<div style="
        width:${size}px; height:${size}px;
        background:${active ? "#C47F3C" : "#8a5020"};
        border:2px solid ${active ? "#F2EDE4" : "rgba(242,237,228,0.6)"};
        border-radius:50%;
        box-shadow:0 2px 6px rgba(0,0,0,0.5);
      "></div>`,
      iconSize: [size, size],
      iconAnchor: [size / 2, size / 2],
    });
  }

  cafes.forEach((cafe, i) => {
    const marker = L.marker([cafe.lat, cafe.lng], { icon: makeIcon(false) })
      .addTo(mapInstance)
      .bindPopup(`
        <div style="font-family:'DM Sans',sans-serif;font-size:13px;min-width:145px;color:#2b1710;">
          <strong>${cafe.name}</strong><br>
          <span style="font-size:11px;color:#7a5030;">${cafe.addr}</span><br>
          <span style="color:#C47F3C;">${starsHtml(cafe.rating)} ${cafe.rating}</span>
        </div>
      `)
      .on("click", () => setActiveMarker(i));
    markers.push(marker);
  });

  buildCafeList();
}

function setActiveMarker(idx) {
  mapInstance.setView([cafes[idx].lat, cafes[idx].lng], 16, { animate: true });
  markers[idx].openPopup();
  document.querySelectorAll(".cafe-item").forEach((el, i) => {
    el.classList.toggle("active", i === idx);
  });
}

function buildCafeList() {
  document.getElementById("cafeListItems").innerHTML = cafes.map((c, i) => `
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

/* ═══════════════════════════════════════
   TOAST
═══════════════════════════════════════ */

let toastTimer = null;
function showToast(msg) {
  const t = document.getElementById("toast");
  t.textContent = msg;
  t.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.classList.remove("show"), 2600);
}

/* ═══════════════════════════════════════
   INIT
═══════════════════════════════════════ */

updateMatchOptions();
loadEvents();
buildMap();