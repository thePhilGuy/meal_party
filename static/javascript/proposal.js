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
	var user_email = document.getElementById('user-email').value;
	// Verify if valid email?
	var user_phone = document.getElementById('user-phone').value;
	// Verify if valide phone also?

	var proposal_zip = zip;
	var from_time = document.getElementById('meal-from').value;
	var until_time = document.getElementById('meal-until').value;
	var date = document.getElementById('meal-date').value;
	// verify from_time before until_time and date after today

	var min_size = document.getElementById('min-size-select').value;
	var ideal_size = document.getElementById('ideal-size-select').value;
	var max_size = document.getElementById('max-size-select').value;
	// verify min_size <= ideal_size <= max_size

	var cuisines = getCuisines();

	var user_proposal = {
		email: user_email,
		phone: user_phone,
		zip: proposal_zip,
		date: date,
		from: from_time,
		until: until_time,
		min_size: min_size,
		max_size: max_size,
		ideal_size: ideal_size,
		cuisines: cuisines
	}

	var user_test = {
		email: "pglosembe@gmail.com",
		phone: "9179694303",
		zip: '10025',
		date: '12/15/2015',
		from: '13:00',
		until: '15:00',
		min_size: 1,
		max_size: 6,
		ideal_size: 3,
		cuisines: ['Chinese', 'Mexican']
	}

	console.log(user_test);
	$.ajax({
		url: "/party",
		type: "POST",
		dataType: "json",
		data: JSON.stringify(user_test)
	});
}
