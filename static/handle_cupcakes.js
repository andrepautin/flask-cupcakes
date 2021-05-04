const BASE_URL = "http://localhost:5000/api";

function generateCupcakeHTML(cupcake) {
    return `
        <div data-cupcake-id=${cupcake.id}>
            <li>
                ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
                <button class="delete-button">X</button>
            </li>
            <img class="cupcake-img"
                src="${cupcake.image}"
                alt="(no image provided)"
        </div>
    `;
}

async function showCupcakesOnStart() {
    // shows cupcakes when the page is loaded
    let response = await axios.get(`${BASE_URL}/cupcakes`);

    for (let cupcake of response.data.cupcakes) {
        let newCupcake = $(generateCupcakeHTML(cupcake));
        $(".cupcakes-list").append(newCupcake)
    }
    console.log("showing cupcakes and form here");
}

// async function createNewCupcake(evt) {
//     evt.preventDefault();

//     let flavor = $("#flavor").val();
//     let size = $("#size").val();
//     let rating = $("#rating").val();
//     let image = $("#image").val();

//     let newCupcakeResponse = await axios.post(`${BASE_URL}/cupcakes`, {
//         flavor, 
//         size, 
//         rating, 
//         image
//     });

//     let newCupcake = $(generateCupcakeHTML(newCupcakeResponse.data));
//     $(".cupcakes-list").append(newCupcake);
//     $("#create-cupcake-form").trigger("reset");
// }

// $("#create-cupcake-form").on("submit", async function (evt) {
async function createNewCupcake(evt) {
    console.log("creating new cupcake");
    evt.preventDefault();
  
    let flavor = $("#form-flavor").val();
    let size = $("#form-size").val();
    let rating = $("#form-rating").val();
    let image = $("#form-image").val();
  
    const newCupcakeResponse = await axios.post(`${BASE_URL}/cupcakes`, {
      flavor,
      size,
      rating,
      image
    });
  
    let newCupcake = $(generateCupcakeHTML(newCupcakeResponse.data.cupcake));
    $(".cupcakes-list").append(newCupcake);
    $("#create-cupcake-form").trigger("reset");
}
  

$("#create-cupcake-form").on("submit", createNewCupcake);
$(showCupcakesOnStart);