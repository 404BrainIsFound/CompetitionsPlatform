
async function getUserData(){
    const response = await fetch('/api/users');
    return response.json();
}

function loadTable(users){
    const table = document.querySelector('#result');
    for(let user of users){
        table.innerHTML += `<tr>
            <td>${user.id}</td>
            <td>${user.username}</td>
        </tr>`;
    }
}

async function main(){
    const users = await getUserData();
    loadTable(users);
}

function openNav(){
    document.getElementById("sidepanel").style.width = "25vw";
}
  
function closeNav(){
    document.getElementById("sidepanel").style.width = "0";
}


//Below is added code - not in original JS

const modal = document.getElementById("statsModal");
const rankingsTableBody = document.querySelector("#rankingsTable tbody");

function openModal() {
    modal.style.display = "block";

    const username = document.querySelector(".profile-details h2").textContent.trim();
    const history = fetch(`/students/${username}/rankings`);

    //create a graph below:

    const xValues = [50,60,70,80,90,100,110,120,130,140,150];
    const yValues = [7,8,8,9,9,9,10,11,14,14,15];

    new Chart("myChart", {
        type: "line",
        data: {
          labels: xValues,
          datasets: [{
            fill: false,
            lineTension: 0,
            backgroundColor: "rgba(0,0,255,1.0)",
            borderColor: "rgba(0,0,255,0.1)",
            data: yValues
          }]
        },
        options: {
          legend: {display: false},
          scales: {
            yAxes: [{ticks: {min: 6, max:16}}],
          }
        }
      });

    // const username = document.querySelector(".profile-details h2").textContent.trim();
    // fetch(`/students/${username}/rankings`)
    //     .then(response => {
    //         if (!response.ok) {
    //             throw new Error("Failed to fetch rankings for }" + username);
    //         }
    //         return response.json();
    //     })
    //     .then(data => {
    //         populateRankingsTable(data);
    //     })
    //     .catch(error => {
    //         console.error("Error fetching rankings:", error);
    //         rankingsTableBody.innerHTML = `<tr><td colspan="2">Failed to load data for {username}</td></tr>`;
    //     });
}


function closeModal() {
    modal.style.display = "none";
}


window.onclick = function (event) {
    if (event.target === modal) {
        closeModal();
    }
};

main();