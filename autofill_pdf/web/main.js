async function getCSV() {
	var csv = await eel.btn_csv_click()();
		if (csv) {
			document.getElementById("input_CSV").value = csv;
		}
		return csv;
	}

async function getPDF() {
	var PDF_template = await eel.btn_pdf_click()();
		if (PDF_template) {
			document.getElementById("PDFtemplate").value = PDF_template;
		}
	}

async function getFolder() {
	var output_loc = await eel.btn_folder_click()();
		if (output_loc) {
			document.getElementById("outputpath").value = output_loc;
		}
		return output_loc;
	}

function CSV_PDF() {
	document.getElementById("complete").style.display = "none";
	document.getElementById("error").style.display = "none";
	document.getElementById("Loader").style.display = "inline";
	var csv = document.getElementById('input_CSV').value;
	var PDF_template = document.getElementById('PDFtemplate').value;
	var output_loc = document.getElementById('outputpath').value;
	var output_filename = document.getElementById('out_filename').value;

	if (document.getElementById('colkey').value == '') {
		var colkey = null;
	} else {
		var colkey = document.getElementById('colkey').value;
	}
	
	if (document.getElementById('checkbox_fields').value == '') {
		
		var checkbox_fields = null;
	} else {
		var checkbox_fields = document.getElementById('checkbox_fields').value;
	}
	
	eel.csv_to_pdf(csv, PDF_template, output_loc, output_filename, colkey, checkbox_fields);
}

eel.expose(finished);
function finished() {
	document.getElementById("Loader").style.display = "none";
	document.getElementById("complete").style.display = "inline";
}

eel.expose(error);
function error(message) {
	document.getElementById("Loader").style.display = "none";
	document.getElementById("error_message").textContent = message;
	document.getElementById("error").style.display = "inline";
}