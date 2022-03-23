// let autocomplete;
function initAutocomplete() {
    let autocomplete = new google.maps.places.Autocomplete(
        document.getElementById("autocomplete"),
        {
            //types: ["establishments"],
            componentRestrictions: { country: "us" },
            fields: ["place_id", "geometry", "name"],
        }
    );
}
