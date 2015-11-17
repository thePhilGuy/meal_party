function getCuisines() {
	// Get chosen cuisines
	var cuisines = [];
	$('#floating-cuisines :checked').each(function() {
		cuisines.push($(this).val());
	});
	console.log(cuisines);
	return cuisines;
}

function parseProposalForm() {
	
}
