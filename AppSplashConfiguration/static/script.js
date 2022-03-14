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
    parcelPlantLabelText = document.createTextNode("Plante :");
    parcelPlantLabel.appendChild(parcelPlantLabelText);
    parcelPlantLabel.classList.add("col-sm-2");

    const parcelPlantP = document.createElement('p');
    var parcelPlant = document.createTextNode(parcel.plant);
    parcelPlantP.appendChild(parcelPlant);
    parcelPlantP.classList.add("col");

    plantDiv.appendChild(parcelPlantLabel);
    plantDiv.appendChild(parcelPlantP);

    // Dim div
    var dimDiv = document.createElement("div");
    dimDiv.classList.add("row", "mx-auto", "w-75");

    const parcelDimLabel = document.createElement('p');
    parcelDimLabelText = document.createTextNode("Taille :");
    parcelDimLabel.appendChild(parcelDimLabelText);
    parcelDimLabel.classList.add("col-sm-2");

    const parcelDimP = document.createElement('p');
    var parcelDim = document.createTextNode(parcel.dim);
    parcelDimP.appendChild(parcelDim)
    parcelDimP.classList.add("col");

    dimDiv.appendChild(parcelDimLabel);
    dimDiv.appendChild(parcelDimP);

    // append to global div
    parcelDiv.appendChild(nameDiv);
    parcelDiv.appendChild(plantDiv);
    parcelDiv.appendChild(dimDiv);

    // append to the page
    var directoryDiv = document.getElementById('parcels');
    directoryDiv.appendChild(parcelDiv);
}