const COFFEES = [
  {
    id: "espresso",
    name: "Espresso",
    emoji: "☕",
    ingredients: ["espresso"],
    desc: "Pure, concentrated coffee shot. The base of almost every coffee drink.",
    history: "Espresso was invented in Italy in the early 1900s by Luigi Bezzera. It became the foundation of modern coffee culture worldwide. Today it is the most consumed coffee in Europe.",
    who: "Enjoyed by coffee purists, professionals, and Italians after every meal.",
    famous: "Italy — especially Naples, Rome and Milan.",
    tip: "Just use Espresso alone!",
  },
  {
    id: "americano",
    name: "Americano",
    emoji: "🫖",
    ingredients: ["espresso", "hot_water"],
    desc: "Espresso diluted with hot water. Smooth and strong.",
    history: "The Americano was created during World War II when American soldiers in Italy diluted espresso with hot water to mimic the drip coffee back home. It quickly became popular worldwide.",
    who: "Popular with Americans and people who prefer a milder, longer coffee.",
    famous: "United States and widely across Europe and Australia.",
    tip: "Combine Espresso + Hot Water!",
  },
  {
    id: "flat_white",
    name: "Flat White",
    emoji: "🥛",
    ingredients: ["espresso", "steamed_milk"],
    desc: "Espresso with velvety steamed milk. Less foam than a latte.",
    history: "The Flat White originated in Australia and New Zealand in the 1980s. There is still a friendly debate between the two countries about who invented it first. It gained global popularity after Starbucks added it to their menu in 2015.",
    who: "Popular with Australians, New Zealanders and specialty coffee lovers.",
    famous: "Australia and New Zealand — especially Sydney, Melbourne and Auckland.",
    tip: "Combine Espresso + Steamed Milk!",
  },
  {
    id: "cappuccino",
    name: "Cappuccino",
    emoji: "☁️",
    ingredients: ["espresso", "steamed_milk", "milk_foam"],
    desc: "Equal parts espresso, steamed milk, and thick foam.",
    history: "The Cappuccino gets its name from the Capuchin friars in Italy, whose brown robes resembled the colour of the drink. It became a morning staple in Italian culture and spread globally after World War II.",
    who: "Loved by Italians in the morning and coffee enthusiasts worldwide.",
    famous: "Italy — Rome, Florence and Venice are famous for their cappuccinos.",
    tip: "Combine Espresso + Steamed Milk + Milk Foam!",
  },
  {
    id: "latte",
    name: "Caffè Latte",
    emoji: "☕",
    ingredients: ["espresso", "steamed_milk", "sugar"],
    desc: "A smooth espresso with lots of steamed milk and a touch of sweetness.",
    history: "Caffe Latte means coffee and milk in Italian. It became popular in American coffee shops in the 1980s and 1990s. Today it is one of the most ordered drinks in cafes worldwide.",
    who: "Popular with casual coffee drinkers, students and office workers.",
    famous: "United States — Seattle is considered the birthplace of modern latte culture.",
    tip: "Combine Espresso + Steamed Milk + Sugar!",
  },
  {
    id: "mocha",
    name: "Mocha",
    emoji: "🍫",
    ingredients: ["espresso", "steamed_milk", "chocolate"],
    desc: "Espresso meets chocolate meets milk. Rich, sweet and indulgent.",
    history: "The Mocha is named after the port city of Mocha in Yemen, which was historically famous for exporting coffee with a natural chocolatey flavour. The modern mocha with added chocolate became popular in American coffee shops in the 1990s.",
    who: "Loved by those with a sweet tooth and people who enjoy dessert-like drinks.",
    famous: "United States and globally — a favourite in Starbucks and coffee chains worldwide.",
    tip: "Combine Espresso + Steamed Milk + Chocolate!",
  },
  {
    id: "iced_latte",
    name: "Iced Latte",
    emoji: "🧋",
    ingredients: ["espresso", "cold_milk", "ice"],
    desc: "Espresso poured over ice and cold milk. Refreshing and smooth.",
    history: "Iced coffee drinks became popular in the United States during the 1990s. The iced latte became a summer staple in coffee chains and is now consumed year-round globally.",
    who: "Popular with younger generations and those in warm climates.",
    famous: "United States, South Korea and Southeast Asia are famous for creative iced lattes.",
    tip: "Combine Espresso + Cold Milk + Ice!",
  },
  {
    id: "vienna",
    name: "Vienna Coffee",
    emoji: "🍦",
    ingredients: ["espresso", "whipped_cream"],
    desc: "Strong espresso topped with whipped cream. A Viennese classic.",
    history: "Vienna Coffee has been a staple of Viennese coffee house culture since the 17th century. The coffee houses of Vienna were famous gathering places for artists, philosophers and intellectuals. UNESCO recognised Viennese coffee house culture as an Intangible Cultural Heritage.",
    who: "Enjoyed by coffee lovers who appreciate rich, indulgent drinks.",
    famous: "Austria — Vienna's coffee houses are world-famous landmarks.",
    tip: "Combine Espresso + Whipped Cream!",
  },
  {
    id: "cold_brew",
    name: "Cold Brew",
    emoji: "🧃",
    ingredients: ["cold_brew", "ice"],
    desc: "Coffee steeped in cold water for hours. Smooth, rich and low acidity.",
    history: "Cold brew coffee has roots in Japan where it was known as Kyoto-style coffee. It became a mainstream trend in the United States around 2015 and has since become one of the fastest-growing coffee categories globally.",
    who: "Popular with health-conscious coffee drinkers and those sensitive to acidity.",
    famous: "United States and Japan — Tokyo and New York are cold brew capitals.",
    tip: "Combine Cold Brew + Ice!",
  },
  {
    id: "affogato",
    name: "Affogato",
    emoji: "🍨",
    ingredients: ["espresso", "ice_cream"],
    desc: "Hot espresso poured over vanilla ice cream. A dessert and coffee in one.",
    history: "Affogato means drowned in Italian. This simple dessert-coffee hybrid originated in Italy and is traditionally served after dinner. It became popular internationally in the 2000s as a trendy cafe dessert.",
    who: "Loved by dessert lovers and people who enjoy creative coffee experiences.",
    famous: "Italy — and now popular in specialty cafes across the world.",
    tip: "Combine Espresso + Ice Cream!",
  },
  {
    id: "irish_coffee",
    name: "Irish Coffee",
    emoji: "🥃",
    ingredients: ["espresso", "whiskey", "whipped_cream"],
    desc: "Coffee with Irish whiskey and whipped cream. A warming classic.",
    history: "Irish Coffee was invented in 1943 by Joe Sheridan at Foynes Airport in Ireland to warm up cold American passengers. It was introduced to the United States in San Francisco in 1952 and became an iconic cocktail-coffee hybrid.",
    who: "Popular with adults looking for a warming evening drink.",
    famous: "Ireland — Limerick and Dublin. Also famous in San Francisco, USA.",
    tip: "Combine Espresso + Whiskey + Whipped Cream!",
  },
  {
    id: "vietnamese",
    name: "Vietnamese Coffee",
    emoji: "🥤",
    ingredients: ["espresso", "condensed_milk", "ice"],
    desc: "Strong coffee with sweet condensed milk over ice. Bold and creamy.",
    history: "Vietnamese coffee culture developed in the 19th century under French colonial influence. Since fresh milk was scarce, condensed milk became the standard. Ca phe sua da became an iconic part of Vietnamese street food culture.",
    who: "Popular in Vietnam and among Southeast Asian coffee lovers worldwide.",
    famous: "Vietnam — Hanoi and Ho Chi Minh City are famous for their street coffee culture.",
    tip: "Combine Espresso + Condensed Milk + Ice!",
  },
  {
    id: "matcha_latte",
    name: "Matcha Latte",
    emoji: "🍵",
    ingredients: ["matcha", "steamed_milk", "sugar"],
    desc: "Earthy green tea powder blended with steamed milk. Creamy, smooth and naturally sweet.",
    history: "Matcha has been used in Japanese tea ceremonies for over 800 years. The matcha latte became a global trend in the 2010s as cafes in Australia, the US and UK started serving it as a coffee alternative.",
    who: "Popular with health-conscious people, tea lovers and those avoiding caffeine.",
    famous: "Japan — Kyoto is the home of matcha. Also huge in Melbourne, London and New York.",
    tip: "Combine Matcha Powder + Steamed Milk + Sugar!",
  },
  {
    id: "hot_chocolate",
    name: "Hot Chocolate",
    emoji: "🍫",
    ingredients: ["hot_water", "chocolate", "steamed_milk"],
    desc: "No coffee here! Just warm chocolate and steamed milk.",
    history: "Hot chocolate has a history going back over 2,500 years to the ancient Mayan and Aztec civilisations of Central America. It was introduced to Europe by Spanish explorers in the 16th century and became a luxury drink in European courts.",
    who: "Loved by children, non-coffee drinkers and anyone seeking comfort.",
    famous: "Belgium and Switzerland are world-famous for their hot chocolate.",
    tip: "Combine Hot Water + Chocolate + Steamed Milk!",
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
  renderEncyclopedia();
}

function renderEncyclopedia() {
  const grid = document.getElementById("encyclopediaGrid");
  if (!grid) return;
  grid.innerHTML = COFFEES.map((c) => {
    return `<div class="encyclopedia-card">
      <div class="enc-header">
        <span class="enc-emoji">${c.emoji}</span>
        <span class="enc-name">${c.name}</span>
      </div>
      <p class="enc-history">${c.history}</p>
      <div class="enc-meta">
        <span>👤 ${c.who}</span>
      </div>
      <div class="enc-meta">
        <span>🌍 ${c.famous}</span>
      </div>
      <div class="enc-tip">
        ☕ ${c.tip}
      </div>
    </div>`;
  }).join("");
}

renderCollection();
renderEncyclopedia();