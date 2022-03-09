// The list of user parcels
var parcels = []


function addParcel() {
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


    console.log("Parcelles : ", parcels)
}