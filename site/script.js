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
  const resultsDiv = document.getElementById("results");
  resultsDiv.innerHTML = `
    <h2>Results</h2>
    <p><strong>${player1.name} Win Probability:</strong> ${(player1WinProb * 100).toFixed(2)}%</p>
    <p><strong>${player2.name} Win Probability:</strong> ${(player2WinProb * 100).toFixed(2)}%</p>
    <p><strong>Player 1 RD Change:</strong> ${player1Wins.rdChange.toFixed(2)}</p>
    <p><strong>Player 2 RD Change:</strong> ${player2Loses.rdChange.toFixed(2)}</p>
    <h3>If ${player1.name} Wins:</h3>
    <p><strong>${player1.name} Rating Change:</strong> ${player1Wins.ratingChange >= 0 ? "+" : ""}${player1Wins.ratingChange.toFixed(2)}</p>
    <p><strong>${player2.name} Rating Change:</strong> ${player2Loses.ratingChange >= 0 ? "+" : ""}${player2Loses.ratingChange.toFixed(2)}</p>
    <h3>If ${player2.name} Wins:</h3>
    <p><strong>${player1.name} Rating Change:</strong> ${player1Loses.ratingChange >= 0 ? "+" : ""}${player1Loses.ratingChange.toFixed(2)}</p>
    <p><strong>${player2.name} Rating Change:</strong> ${player2Wins.ratingChange >= 0 ? "+" : ""}${player2Wins.ratingChange.toFixed(2)}</p>
  `;

  // Draw pie chart
  drawChart(player1WinProb, player2WinProb, player1.name, player2.name);
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
      labels: [`${player1Name} Wins`, `${player2Name} Wins`],
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

// Initialize the page
loadPlayers();
