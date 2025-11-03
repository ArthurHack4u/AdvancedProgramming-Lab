const API = 'https://fi.jcaguilar.dev/v1/escuela/persona'
const txtField = document.querySelector('#txt')
const btnSearch = document.querySelector('#btn-buscar')
const img = document.querySelector('#img')

function init () {
    btnSearch.addEventListener('click', search3);

    promesa()
}

function search (evt) {
    evt.preventDefault()
    $.ajax({
        url: `https://pokeapi.co/api/v2/pokemon/${ txtField.value }`,

        //callback
        success: function (respuesta) {
            console.log(respuesta)
            search2(evt)
            if(respuesta.count){return}
            img.src = respuesta.sprites.front_default
        },

        //callback
        error: () => {
            alert('Ocurrio un error.')
        }

    })
}

function promesa() {
    let p = new Promise((resolver, rechazar) => {
        setTimeout(()=> {
            let moneda = Math.random() > 0.5
                ? 'cara'
                : 'cruz'
            setTimeout(() =>{
                let jugador = prompt('cara o cruz?')

                setTimeout(() => {
                    if (jugador == moneda){
                        resolver('oda ganaste')
                    } else{
                        rechazar('oda GameOver')
                    }
                }, 2500)
            }, 2500)
        }, 2500)
    })

    p
      .then(msj => { alert(msj) })
      .catch(err => { alert(err) })

}

function search2 (evt) {
    evt.preventDefault()
    fetch(`https://pokeapi.co/api/v2/pokemon/${ txtField.value }/`)
    .then ( respuesta => {
        console.log(respuesta)
        return respuesta.json()
    })

    .then(datos => {
        img.src = datos.sprites.front_default

    }

    )

    .catch( err => {
        console.error(err)
    })  
}


async function search3 (evt) {
    evt.preventDefault()

    try {
    
    //Lanzar la solicitud
    let request = await fetch(`https://pokeapi.co/api/v2/pokemon/${ txtField.value }/`)

    //Obtener la respuesta
    let respuesta = await respuesta.json()

    //Utiliza los datos de la respuesta
    img.src = respuesta.sprites.front_default

    } catch(err) {
        console.error(err)
    }
}

window.addEventListener('load', init)


//Pokeomon API