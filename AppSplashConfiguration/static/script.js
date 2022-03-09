// The list of user parcels
var parcels = []


function addNewParcel() {
    // Get values from html form
    let name = document.getElementById("name");
    let plant = document.getElementById("plant");
    let dim = document.getElementById("dimension");

    // Throw error if empty input
    if (name.value == "" || plant.value == "" || dim.value == "") {
        throw 'Invalid form values !';
    }

    // Init new parcel
    let parcel = {
        name: name.value,
        plant: plant.value,
        dim: dim.value,
    }

    // Add parcel to parcels list
    parcels.push(parcel)

    // Reset form 
    name.value = "";
    plant.value = "";
    dim.value = "";

    newParcelHtml(parcel);

    // To display user parcels div    
    if (parcels.length == 1) {
        document.getElementById("parcels").style.display = "inline";
        document.getElementById("div-save-button").style.display = "inline";
    }

    document.getElementById("parcels-data").value = JSON.stringify(parcels);
}

function newParcelHtml(parcel) {
    // Global parcel div
    var parcelDiv = document.createElement("div");
    parcelDiv.classList.add("parcel_div");

    // Name div
    var nameDiv = document.createElement("div");
    nameDiv.classList.add("row", "mx-auto", "w-75");

    const parcelNameLabel = document.createElement('p');
    parcelNameLabelText = document.createTextNode("Name :");
    parcelNameLabel.appendChild(parcelNameLabelText);
    parcelNameLabel.classList.add("col-sm-2");

    const parcelNameP = document.createElement('p');
    var parcelName = document.createTextNode(parcel.name);
    parcelNameP.appendChild(parcelName);
    parcelNameP.classList.add("col");

    nameDiv.appendChild(parcelNameLabel);
    nameDiv.appendChild(parcelNameP);

    // Plant div
    var plantDiv = document.createElement("div");
    plantDiv.classList.add("row", "mx-auto", "w-75");

    const parcelPlantLabel = document.createElement('p');
    parcelPlantLabelText = document.createTextNode("Plant :");
    parcelPlantLabel.appendChild(parcelPlantLabelText);
    parcelPlantLabel.classList.add("col-sm-2");

    const parcelPlantP = document.createElement('p');
    var parcelPlant = document.createTextNode(parcel.plant);
    parcelPlantP.appendChild(parcelPlant);
    parcelPlantP.classList.add("col");

    plantDiv.appendChild(parcelPlantLabel);
    plantDiv.appendChild(parcelPlantP);

    // Type div
    var typeDiv = document.createElement("div");
    typeDiv.classList.add("row", "mx-auto", "w-75");

    const parcelTypeLabel = document.createElement('p');
    parcelTypeLabelText = document.createTextNode("Type :");
    parcelTypeLabel.appendChild(parcelTypeLabelText);
    parcelTypeLabel.classList.add("col-sm-2");

    const parcelTypeP = document.createElement('p');
    var parcelType = document.createTextNode(parcel.dim);
    parcelTypeP.appendChild(parcelType)
    parcelTypeP.classList.add("col");

    typeDiv.appendChild(parcelTypeLabel);
    typeDiv.appendChild(parcelTypeP);

    // append to global div
    parcelDiv.appendChild(nameDiv);
    parcelDiv.appendChild(plantDiv);
    parcelDiv.appendChild(typeDiv);

    // append to the page
    var directoryDiv = document.getElementById('parcels');
    directoryDiv.appendChild(parcelDiv);
}