// The list of user parcels
var parcels = []


function addParcel() {
    // Get values from html form
    let name = document.getElementById("name").value;
    let plant = document.getElementById("plant").value;
    let dim = document.getElementById("dimension").value;

    // Init parcel and add parcel
    let parcel = {
        name: name,
        plant: plant,
        dim: dim
    }

    parcels.push(parcel)

    console.log("Parcelles : ", parcels)
}