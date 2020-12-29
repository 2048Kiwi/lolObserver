const start = document.getElementById('start');
const clear = document.getElementById('stop');
const reset = document.getElementById('reset');
const set = document.getElementById('set');
const levelsReplicant = nodecg.Replicant('levels');
const bannersReplicant = nodecg.Replicant('bunners');
var id;
var start_frag = false;

function getData(){
	var req = new XMLHttpRequest();
	req.open('GET', 'http://localhost:3000/');
	req.send(null);
	req.onreadystatechange = function() {
	if (req.readyState == 4 && req.status == 200) {
		console.log(req.responseText);
		var data = JSON.parse(req.responseText);
		levelsReplicant.value = data["level"];
		bannersReplicant.value = data["banner"];
	}};
	console.log(levelsReplicant.value);
	console.log(bannersReplicant.value);
}

start.addEventListener('click', () => {
	if(!start_frag){
		start_frag = true
		id = setInterval(getData, 200);
	}
})

clear.addEventListener('click', () => {
	start_frag = false;
	clearInterval(id);
})

reset.addEventListener('click', () => {
	levelsReplicant.value = {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1};
	bannersReplicant.value = {0: "none", 1: "none", 2: "none", 3: "none", 4: "none", 5: "none", 6: "none", 7: "none", 8: "none", 9: "none"}
})

set.addEventListener('click', () => {
	levelsReplicant.value = {0: 16, 1: 2, 2: 3, 3: 4, 4: 5, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1};
	bannersReplicant.value = {0: "level", 1: "level", 2: "level", 3: "level", 4: "level", 5: "level", 6: "level", 7: "level", 8: "level", 9: "level"}
})
