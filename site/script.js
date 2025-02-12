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
      name: columns[0].trim(), // Player name is in column index 0
      rating: parseFloat(columns[1].trim()), // Rating is in column index 1
      rd: parseFloat(columns[2].trim()), // RD is in column index 2
    };
  });
}

// Populate dropdowns with player names
function populateDropdowns() {
  const player1Select = document.getElementById("player1");
  const player2Select = document.getElementById("player2");

  players.forEach(player => {
    const option = document.createElement("option");
    option.value = player.name;
    option.textContent = player.name;
    player1Select.appendChild(option.cloneNode(true));
    player2Select.appendChild(option);
  });
}

// Calculate winning probability using Glicko system
function calculateWinProbability(player1, player2) {
  const ratingDiff = player2.rating - player1.rating;
  const probability = 1 / (1 + Math.pow(10, ratingDiff / 400));

  console.log("Player 1:", player1.name, "Rating:", player1.rating);
  console.log("Player 2:", player2.name, "Rating:", player2.rating);
  console.log("Rating Diff:", ratingDiff);
  console.log("Win Probability (Player 1):", probability);

  return probability;
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
