function detailsForm() {
	var values = [];
	$("#floating-cuisines :checked").each(function() {
		values.append($(this).val());
	});
	console.log(values);
}