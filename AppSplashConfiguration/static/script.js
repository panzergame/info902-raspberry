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

    // To display user parcels
    if (parcels.length == 1) {
        document.getElementById("parcels").style.display = "inline";
    }

    displayNewParcel(parcel);
}

function displayNewParcel(parcel) {
    var parcelDiv = document.createElement("div");
    parcelDiv.classList.add("parcel_div");

    const parcelNameP = document.createElement('p');
    var parcelName = document.createTextNode(parcel.name);
    parcelNameP.appendChild(parcelName);

    const parcelPlantP = document.createElement('p');
    var parcelPlant = document.createTextNode(parcel.plant);
    parcelPlantP.appendChild(parcelPlant);

    const parcelTypeP = document.createElement('p');
    var parcelType = document.createTextNode(parcel.dim);
    parcelTypeP.appendChild(parcelType)

    parcelDiv.appendChild(parcelNameP);
    parcelDiv.appendChild(parcelPlantP);
    parcelDiv.appendChild(parcelTypeP);

    var directoryDiv = document.getElementById('parcels');
    directoryDiv.appendChild(parcelDiv);
}
