// Constante où on stock le host du serveur contenant l'api (http://localhost:5000)
const host = window.location.protocol + "//" + window.location.host;
// Au chargement de la page, on ajoute un listener au formulaire create-game-form,
if (createGameForm != null) {
// Récupérer l'objet contenant les données de notre formulaire
// Appel de l'API create-game qui se fait en asynchrone
// afin de mettre le message de retour de l'api
if (!response.ok) {
console.log(error)
const gameId = await response.json();
// http://localhost:5000/views/manage_fleet.html?game-id=4&player-name=Tatanor
playerName;
}
const createGameForm = document.getElementById("create-game-form");
  // url complète de l'api create-game
const url = host + "/create-game";
  // à la soumission la fonction create_game(event) sera appelée
window.onload = function () {
const createGameForm = document.getElementById("create-game-form");
  createGameForm.addEventListener("submit", create_game); }
};
  async function create_game(event) { event.preventDefault(); console.log("start request")
  // Récupérer l'objet qui représente le fomulaire concerné
const form = event.currentTarget; const formData = new FormData(form);
  // notez que les attributs name des elements html du formulaire doivent // contenir les mêmes noms attendus par l’api
const plainFormData = Object.fromEntries(formData.entries());
const formDataJsonString = JSON.stringify(plainFormData);
  // le await pour stocker le résultat dans response quand il sera reçu
const response = await postData(url, formDataJsonString)
// Récupérer l'element html identifié par "create-game-result"
  const resultCreateGame = document.getElementById("create-game-result"); let h1 = document.createElement('H1');
resultCreateGame.appendChild(h1)
  // le await est ajouté ici parceque response est un objet qu'on recevra plutard en asynchrone
const error = await response.json();
  h1.innerHTML = "Erreur: " + error.message;
h1.className = "error"; } else {
  h1.innerHTML = "Partie créée avec l'id : " + gameId + "<br>";
// Dans l'element html qui contient le résultat on ajoute un lien
// pour diriger l'utilisateur vers la page de gestion de création des vaisseaux // avec l'id de la partie créée :
  let linkToVessels = document.createElement("a");
const playerName = document.getElementById("player-name").value; linkToVessels.href = "manage_fleet.html?game-id=" + gameId + "&player-name=" +
  linkToVessels.text = "Créer votre flotte !" h1.appendChild(linkToVessels);
h1.className = "success";}