const csvUrl = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRJtlTjWV6j8VcWAR67efp2DDbYSWUEuYo1UYIeNCUW8ioBpKqNYZuEXJEOzYktsxQoy4KF74S3Hl-t/pub?gid=1546031711&single=true&output=csv";

let players = [];
let matchupChart = null;

// Load player data from Google Sheets
async function loadPlayers() {
  try {
    const response = await fetch(csvUrl);
    const csvData = await response.text();
    players = parseCsvData(csvData);
    populateDropdowns();
  } catch (error) {
    console.error("Error loading player data:", error);
  }
}

// Parse CSV data into an array of player objects
function parseCsvData(csvData) {
  const rows = csvData.split("\n").slice(1); // Skip header row
  return rows.map(row => {
    const columns = row.split(",");
    return {
      name: columns[0].trim(),
      rating: parseFloat(columns[1].trim()),
      rd: parseFloat(columns[2].trim()),
    };
  });
}

// Populate dropdowns with player names
function populateDropdowns() {
  const player1Select = document.getElementById("player1");
  const player2Select = document.getElementById("player2");

  // Clear previous options
  player1Select.innerHTML = "";
  player2Select.innerHTML = "";

  // Add default empty option
  const defaultOption = document.createElement("option");
  defaultOption.value = "";
  defaultOption.textContent = "----";
  player1Select.appendChild(defaultOption.cloneNode(true));
  player2Select.appendChild(defaultOption);

  // Add players to dropdowns
  players.forEach(player => {
    const option = document.createElement("option");
    option.value = player.name;
    option.textContent = player.name;
    player1Select.appendChild(option.cloneNode(true));
    player2Select.appendChild(option);
  });

  // Add event listeners to update player info when selection changes
  player1Select.addEventListener("change", updatePlayerInfo);
  player2Select.addEventListener("change", updatePlayerInfo);
}

// Update player info display when a selection is made
function updatePlayerInfo() {
  const player1Name = document.getElementById("player1").value;
  const player2Name = document.getElementById("player2").value;

  const player1 = players.find(p => p.name === player1Name);
  const player2 = players.find(p => p.name === player2Name);

  document.getElementById("player1-name").textContent = player1 ? player1.name : "";
  document.getElementById("player1-rating").textContent = player1 ? player1.rating.toFixed(2) : "";
  document.getElementById("player1-rd").textContent = player1 ? player1.rd.toFixed(2) : "";

  document.getElementById("player2-name").textContent = player2 ? player2.name : "";
  document.getElementById("player2-rating").textContent = player2 ? player2.rating.toFixed(2) : "";
  document.getElementById("player2-rd").textContent = player2 ? player2.rd.toFixed(2) : "";
}

// Calculate the Glicko-1 rating change for a player
function calculateGlickoChange(player, opponent, outcome) {
  const q = Math.log(10) / 400;
  const gRD = 1 / Math.sqrt(1 + (3 * q * q * opponent.rd * opponent.rd) / (Math.PI * Math.PI));
  const expectedScore = 1 / (1 + Math.pow(10, -gRD * (player.rating - opponent.rating) / 400));
  const dSquared = 1 / (q * q * gRD * gRD * expectedScore * (1 - expectedScore));
  const newRating = player.rating + (q / (1 / (player.rd * player.rd) + 1 / dSquared)) * gRD * (outcome - expectedScore);
  const newRD = Math.sqrt(1 / (1 / (player.rd * player.rd) + 1 / dSquared));

  return {
    newRating: newRating,
    newRD: newRD,
    ratingChange: newRating - player.rating, // Calculate rating change
    rdChange: newRD - player.rd, // Calculate RD change
  };
}

// Calculate win probability using the Glicko-1 system
function calculateWinProbability(player1, player2) {
  const q = Math.log(10) / 400;
  const gRD = 1 / Math.sqrt(1 + (3 * q * q * player2.rd * player2.rd) / (Math.PI * Math.PI));
  return 1 / (1 + Math.pow(10, -gRD * (player1.rating - player2.rating) / 400));
}

// Calculate and display matchup results
function calculateMatchup() {
  const player1Name = document.getElementById("player1").value;
  const player2Name = document.getElementById("player2").value;

  const player1 = players.find(p => p.name === player1Name);
  const player2 = players.find(p => p.name === player2Name);

  if (!player1 || !player2) {
    alert("Please select valid players.");
    return;
  }

  // Calculate win probabilities
  const player1WinProb = calculateWinProbability(player1, player2);
  const player2WinProb = 1 - player1WinProb;

  // Calculate rating changes for both scenarios
  const player1Wins = calculateGlickoChange(player1, player2, 1);
  const player1Loses = calculateGlickoChange(player1, player2, 0);
  const player2Wins = calculateGlickoChange(player2, player1, 1);
  const player2Loses = calculateGlickoChange(player2, player1, 0);

  // Display results
  updateResults(player1, player2, player1WinProb, player2WinProb, player1Wins, player1Loses, player2Wins, player2Loses);

  // Draw pie chart
  drawChart(player1WinProb, player2WinProb, player1.name, player2.name);

  // Update pairwise stats
  calculatePairwiseStats();
}

// Update results section
function updateResults(player1, player2, player1WinProb, player2WinProb, player1Wins, player1Loses, player2Wins, player2Loses) {
  const resultsDiv = document.getElementById("results");
  const player1WinClass = player1WinProb > player2WinProb ? "change-pos" : "change-neg";
  const player2WinClass = player2WinProb > player1WinProb ? "change-pos" : "change-neg";

  resultsDiv.innerHTML = `
    <div class="results-table">
      <div class="row header">
        <div class="cell">Name:</div>
        <div class="cell">${player1.name}</div>
        <div class="cell">${player2.name}</div>
      </div>
      <div class="row">
        <div class="cell">Win %</div>
        <div class="cell ${player1WinClass}">${(player1WinProb * 100).toFixed(2)}%</div>
        <div class="cell ${player2WinClass}">${(player2WinProb * 100).toFixed(2)}%</div>
      </div>
      <div class="row">
        <div class="cell">RD Change:</div>
        <div class="cell">${player1Wins.rdChange.toFixed(2)}</div>
        <div class="cell">${player2Loses.rdChange.toFixed(2)}</div>
      </div>
      <div class="row">
        <div class="cell">Rating Change (P1 Wins):</div>
        <div class="cell ${player1Wins.ratingChange >= 0 ? "change-pos" : "change-neg"}">
          ${player1Wins.ratingChange.toFixed(1)}
        </div>
        <div class="cell ${player2Loses.ratingChange >= 0 ? "change-pos" : "change-neg"}">
          ${player2Loses.ratingChange.toFixed(1)}
        </div>
      </div>
      <div class="row">
        <div class="cell">Rating Change (P2 Wins):</div>
        <div class="cell ${player1Loses.ratingChange >= 0 ? "change-pos" : "change-neg"}">
          ${player1Loses.ratingChange.toFixed(1)}
        </div>
        <div class="cell ${player2Wins.ratingChange >= 0 ? "change-pos" : "change-neg"}">
          ${player2Wins.ratingChange.toFixed(1)}
        </div>
      </div>
    </div>
  `;
}

// Draw pie chart using Chart.js
function drawChart(player1WinProb, player2WinProb, player1Name, player2Name) {
  const ctx = document.getElementById("matchupChart").getContext("2d");

  // Properly destroy previous chart instance before creating a new one
  if (matchupChart !== null) {
    matchupChart.destroy();
    matchupChart = null;
  }

  // Create new chart instance
  matchupChart = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: [`${player1Name} Wins`,`${player2Name} Wins`],
      datasets: [{
        data: [player1WinProb * 100, player2WinProb * 100], // Convert to percentages
        backgroundColor: ['#36A2EB', '#FF6384'],
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
    }
  });
}

// Calculate and display pairwise stats
function calculatePairwiseStats() {
  const player1 = document.getElementById("player1").value;
  const player2 = document.getElementById("player2").value;

  if (!player1 || !player2 || !playerStats[player1] || !playerStats[player1][player2]) {
    document.getElementById("pairwise-results").innerHTML = "<p>No data available for this matchup.</p>";
    return;
  }

  const stats = playerStats[player1][player2];
  const totalGames = stats.wins + stats.losses;
  const winPctP1 = ((stats.wins / totalGames) * 100).toFixed(2);
  const winPctP2 = ((stats.losses / totalGames) * 100).toFixed(2);

  document.getElementById("pairwise-results").innerHTML = `
    <div class="results-table">
      <div class="row header">
        <div class="cell">Pairwise Stats</div>
        <div class="cell">${player1}</div>
        <div class="cell">${player2}</div>
      </div>
      <div class="row">
        <div class="cell">Total Games Played</div>
        <div class="cell" colspan="2">${totalGames}</div>
      </div>
      <div class="row">
        <div class="cell">Wins</div>
        <div class="cell ${stats.wins > stats.losses ? 'change-pos' : 'change-neg'}">${stats.wins}</div>
        <div class="cell ${stats.losses > stats.wins ? 'change-pos' : 'change-neg'}">${stats.losses}</div>
      </div>
      <div class="row">
        <div class="cell">Win %</div>
        <div class="cell ${winPctP1 > winPctP2 ? 'change-pos' : 'change-neg'}">${winPctP1}%</div>
        <div class="cell ${winPctP2 > winPctP1 ? 'change-pos' : 'change-neg'}">${winPctP2}%</div>
      </div>
      <div class="row">
        <div class="cell">Avg. Points</div>
        <div class="cell ${stats.avgScored > stats.avgAgainst ? 'change-pos' : 'change-neg'}">${stats.avgScored.toFixed(2)}</div>
        <div class="cell ${stats.avgAgainst > stats.avgScored ? 'change-pos' : 'change-neg'}">${stats.avgAgainst.toFixed(2)}</div>
      </div>
    </div>
  `;
}

// Initialize the page
document.addEventListener("DOMContentLoaded", () => {
  loadPlayers();
  document.getElementById("calculate-button").addEventListener("click", calculateMatchup);
});
