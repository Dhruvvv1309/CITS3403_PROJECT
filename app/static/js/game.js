const COFFEES = [
  {
    id: "espresso",
    name: "Espresso",
    emoji: "☕",
    ingredients: ["espresso"],
    desc: "Pure, concentrated coffee shot. The base of almost every coffee drink. Originated in Italy in the early 1900s.",
  },
  {
    id: "americano",
    name: "Americano",
    emoji: "🫖",
    ingredients: ["espresso", "hot_water"],
    desc: "Espresso diluted with hot water. Smooth and strong. Popular with those who want a longer black coffee.",
  },
  {
    id: "flat_white",
    name: "Flat White",
    emoji: "🥛",
    ingredients: ["espresso", "steamed_milk"],
    desc: "Espresso with velvety steamed milk. Less foam than a latte. Born in Australia and New Zealand!",
  },
  {
    id: "cappuccino",
    name: "Cappuccino",
    emoji: "☁️",
    ingredients: ["espresso", "steamed_milk", "milk_foam"],
    desc: "Equal parts espresso, steamed milk, and thick foam. A classic Italian morning staple.",
  },
  {
    id: "mocha",
    name: "Mocha",
    emoji: "🍫",
    ingredients: ["espresso", "steamed_milk", "chocolate"],
    desc: "Espresso meets chocolate meets milk. Rich, sweet, and indulgent. A coffee lover's dessert.",
  },
  {
    id: "iced_latte",
    name: "Iced Latte",
    emoji: "🧋",
    ingredients: ["espresso", "cold_milk", "ice"],
    desc: "Espresso poured over ice and cold milk. Refreshing and smooth. Perfect for warm days.",
  },
  {
    id: "vienna",
    name: "Vienna Coffee",
    emoji: "🍦",
    ingredients: ["espresso", "whipped_cream"],
    desc: "Strong espresso topped with whipped cream. A Viennese classic — rich and indulgent.",
  },
  {
    id: "hot_chocolate",
    name: "Hot Chocolate",
    emoji: "🍵",
    ingredients: ["hot_water", "chocolate", "steamed_milk"],
    desc: "No coffee here! Just warm chocolate and steamed milk. A comforting non-coffee classic.",
  },
];

let selectedIngredients = [];
let discovered = JSON.parse(localStorage.getItem("cuplog_discovered") || "[]");

const mixZone = document.getElementById("mixZone");
const resultPanel = document.getElementById("resultPanel");
const resultName = document.getElementById("resultName");
const resultDesc = document.getElementById("resultDesc");
const resultEmoji = document.getElementById("resultEmoji");
const resultRecipe = document.getElementById("resultRecipe");
const collectionGrid = document.getElementById("collectionGrid");

document.querySelectorAll(".ingredient").forEach((el) => {
  el.addEventListener("click", () => {
    const id = el.dataset.id;
    if (selectedIngredients.includes(id)) {
      selectedIngredients = selectedIngredients.filter((i) => i !== id);
      el.classList.remove("selected");
    } else {
      selectedIngredients.push(id);
      el.classList.add("selected");
    }
    renderMixZone();
  });
});

function renderMixZone() {
  if (selectedIngredients.length === 0) {
    mixZone.innerHTML = `<p class="mix-hint">Click ingredients to add them here</p>`;
    return;
  }
  mixZone.innerHTML = selectedIngredients
    .map((id) => {
      const el = document.querySelector(`.ingredient[data-id="${id}"]`);
      return `<span class="mix-tag">${el.textContent}</span>`;
    })
    .join("");
}

document.getElementById("brewBtn").addEventListener("click", () => {
  if (selectedIngredients.length === 0) return;

  const sorted = [...selectedIngredients].sort();
  const match = COFFEES.find(
    (c) => JSON.stringify([...c.ingredients].sort()) === JSON.stringify(sorted)
  );

  resultPanel.classList.add("show");

  if (match) {
    resultEmoji.textContent = match.emoji;
    resultName.textContent = match.name;
    resultDesc.textContent = match.desc;
    resultRecipe.textContent = `Recipe: ${match.ingredients.join(" + ")}`;
    resultPanel.querySelector(".result-card").classList.remove("fail");
    resultPanel.querySelector(".result-card").classList.add("success");

    if (!discovered.includes(match.id)) {
      discovered.push(match.id);
      localStorage.setItem("cuplog_discovered", JSON.stringify(discovered));
    }
    renderCollection();
  } else {
    resultEmoji.textContent = "❓";
    resultName.textContent = "Unknown Mix!";
    resultDesc.textContent = "Hmm, that combination doesn't make a known coffee. Try adjusting your ingredients!";
    resultRecipe.textContent = "";
    resultPanel.querySelector(".result-card").classList.remove("success");
    resultPanel.querySelector(".result-card").classList.add("fail");
  }
});

document.getElementById("clearBtn").addEventListener("click", () => {
  selectedIngredients = [];
  document.querySelectorAll(".ingredient").forEach((el) => el.classList.remove("selected"));
  renderMixZone();
  resultPanel.classList.remove("show");
});

function renderCollection() {
  collectionGrid.innerHTML = COFFEES.map((c) => {
    const found = discovered.includes(c.id);
    return `<div class="collection-item ${found ? "found" : "locked"}">
      <span>${found ? c.emoji : "🔒"}</span>
      <p>${found ? c.name : "???"}</p>
    </div>`;
  }).join("");
}

renderCollection();