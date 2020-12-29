const levelsReplicant = nodecg.Replicant('levels');
const bannersReplicant = nodecg.Replicant('bunners');

function upBanner(smID, type){
	var elID;
	var targetX = 160;
	if(smID<5){
		elID = document.getElementById('blueBanner' + (smID+1));
	}else{
		elID = document.getElementById('redBanner' + (smID-4));
		targetX = -targetX;
	}
	anime({	targets: elID, 
			translateX: targetX});
}

function downBanner(smID){
	var elID;
	if(smID<5){
		elID = document.getElementById('blueBanner' + (smID+1));
	}else{
		elID = document.getElementById('redBanner' + (smID-4));
	}
	anime({	targets: elID, 
			translateX: 0});
}

function setText(smID, type){
	var idName;
	var elID;
	if(type=="level") idName = "Level";
	if(type=="csmin") idName = "CSmin";
	
	if(smID<5){
		idName = "blue" + idName + (smID+1);
	}else{
		idName = "red" + idName + (smID-4);
	}
	elID = document.getElementById(idName);
	elID.innerText = "lv" + levelsReplicant.value[smID];
}

bannersReplicant.on('change', newValue => {
	console.log(bannersReplicant.value);
	console.log(levelsReplicant.value);
	for(let i=0; i<10; i++){
		var type = newValue[i]
		if(type=="none"){
			downBanner(i)
		}else{
			setText(i, type);
			upBanner(i);
		}
	}
})
