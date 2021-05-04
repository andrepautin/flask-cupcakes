const BASE_URL = "http://localhost:5000";

async function getCupcakes() {
    let response = await axios.get("/api/cupcakes");

    for (let cupcake of response.data.cupcakes) {
        let $cupcake = $(`<li>flavor: ${cupcake.flavor}
                        size: ${cupcake.size}
                        rating: ${cupcake.rating}
                        image: ${cupcake.image}
          </li>`);
        $(".cupcakes-list").append($cupcake);
    }
}

$(getCupcakes);