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
      name: columns[0].trim(), // Player name
      rating: parseFloat(columns[1].trim()), // Rating
      rd: parseFloat(columns[2].trim()), // RD
    };
  });
}

// Populate dropdowns with player names
function populateDropdowns() {
  const player1Select = document.getElementById("player1");
  const player2Select = document.getElementById("player2");

  // Add default empty option
  const defaultOption = document.createElement("option");
  defaultOption.value = "";
  defaultOption.textContent = "----";
  player1Select.appendChild(defaultOption.cloneNode(true));
  player2Select.appendChild(defaultOption);

  players.forEach(player => {
    const option = document.createElement("option");
    option.value = player.name;
    option.textContent = player.name;
    player1Select.appendChild(option.cloneNode(true));
    player2Select.appendChild(option);
  });
}

// Update player info when selected
function updatePlayerInfo(playerSelectId, infoDivId) {
  const playerName = document.getElementById(playerSelectId).value;
  const player = players.find(p => p.name === playerName);

  const infoDiv = document.getElementById(infoDivId);
  if (player) {
    infoDiv.innerHTML = `<p>Rating: ${player.rating}</p><p>RD: ${player.rd}</p>`;
  } else {
    infoDiv.innerHTML = `<p>Select a player</p>`;
  }
}

// Calculate the g(Δ) function for Glicko
function glickoG(rd) {
  const q = Math.log(10) / 400;
  return 1 / Math.sqrt(1 + (3 * q * q * rd * rd) / (Math.PI * Math.PI));
}

// Calculate winning probability using the Glicko system
function calculateWinProbability(player1, player2) {
  const q = Math.log(10) / 400;
  const rdDiff = Math.sqrt(player1.rd * player1.rd + player2.rd * player2.rd);
  const g = glickoG(rdDiff);
  const exponent = -g * (player1.rating - player2.rating) / 400;
  return 1 / (1 + Math.pow(10, exponent));
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

  const player1WinProb = calculateWinProbability(player1, player2);
  const player2WinProb = 1 - player1WinProb;

  // Display results
  const resultsDiv = document.getElementById("results");
  resultsDiv.innerHTML = `
    <h2>Results</h2>
    <p>${player1.name} Win Probability: ${(player1WinProb * 100).toFixed(2)}%</p>
    <p>${player2.name} Win Probability: ${(player2WinProb * 100).toFixed(2)}%</p>
  `;

  // Draw pie chart
  drawChart(player1WinProb, player2WinProb, player1.name, player2.name);
}

// Draw pie chart using Chart.js
function drawChart(player1WinProb, player2WinProb, player1Name, player2Name) {
  const ctx = document.getElementById("matchupChart").getContext("2d");

  if (matchupChart) {
    matchupChart.destroy();
  }

  matchupChart = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: [`${player1Name} Wins`, `${player2Name} Wins`],
      datasets: [{
        data: [player1WinProb, player2WinProb],
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
