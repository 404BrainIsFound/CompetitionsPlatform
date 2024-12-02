
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
    fetch(`/students/${username}/rankings`)
        .then(response => {
            if (!response.ok) {
                throw new Error("Failed to fetch rankings for }" + username);
            }
            return response.json();
        })
        .then(data => {
            populateRankingsTable(data);
        })
        .catch(error => {
            console.error("Error fetching rankings:", error);
            rankingsTableBody.innerHTML = `<tr><td colspan="2">Failed to load data - No competition history!</td></tr>`;
        });
}


function closeModal() {
    modal.style.display = "none";
}


function populateRankingsTable(rankings) {
    rankingsTableBody.innerHTML = ""; 
    if (rankings.length === 0) {
        rankingsTableBody.innerHTML = `<tr><td colspan="2" style="text-align: center;">No Rankings Found</td></tr>`;
        return;
    }

    rankings.forEach(rank => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${rank.rank}</td>
            <td>${rank.date}</td>
        `;
        rankingsTableBody.appendChild(row);
    });
}

window.onclick = function (event) {
    if (event.target === modal) {
        closeModal();
    }
};

/*function closeMessage(){
    document.getElementById("error_message").style.display = "none";
}*/

main();