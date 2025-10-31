window.addEventListener('load', init);

const STORAGE_KEY = 'tabla_registros';
let btnAdd

function init () {
    btnAdd = document
        .querySelector('#btn-add')
    btnAdd 
        .addEventListener('click', add)

    loadFromStorage()
}

function add (evt) {

    evt.preventDefault()

    let nombre = 
        document.querySelector('#A1')
        .value

    console.log(nombre)

    let apellido =
        document.querySelector('#A2')
        .value

    console.log(apellido)

    let sexo =
        document.querySelector('input[name=sexo]:checked ')
        .value

    console.log(sexo)

    let fecha =
        document.querySelector('#fecha')
        .value

    console.log(fecha)

    let rol =
        document.querySelector('#id_rol')
        .value
    
    console.log(rol)

    let cal =
        document.querySelector('#cal')
        .value

    console.log(cal)

    let table =
        document.querySelector("table tbody")

    let file = document.createElement('tr')

    let colNombre = document.createElement('td')
    colNombre.innerText = nombre
    file.appendChild(colNombre)

    let colapellido = document.createElement('td')
    colapellido.innerText = apellido
    file.appendChild(colapellido)

    let colsexo = document.createElement('td')
    colsexo.innerText = sexo
    file.appendChild(colsexo)

    let colfecha = document.createElement('td')
    colfecha.innerText = fecha
    file.appendChild(colfecha)

    let colrol = document.createElement('td')
    colrol.innerText = rol
    file.appendChild(colrol)

    let colcal = document.createElement('td')
    colcal.innerText = cal
    file.appendChild(colcal)

    table.appendChild(file)

    saveRow({ nombre, apellido, sexo, fecha, rol, cal })
}

function saveRow(row) {
    const data = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]')
    data.push(row)
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data))
}

function loadFromStorage() {
    const data = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]')
    const table = document.querySelector("table tbody")
    data.forEach(row => {
        let file = document.createElement('tr')

        let colNombre = document.createElement('td')
        colNombre.innerText = row.nombre
        file.appendChild(colNombre)

        let colapellido = document.createElement('td')
        colapellido.innerText = row.apellido
        file.appendChild(colapellido)

        let colsexo = document.createElement('td')
        colsexo.innerText = row.sexo
        file.appendChild(colsexo)

        let colfecha = document.createElement('td')
        colfecha.innerText = row.fecha
        file.appendChild(colfecha)

        let colrol = document.createElement('td')
        colrol.innerText = row.rol
        file.appendChild(colrol)

        let colcal = document.createElement('td')
        colcal.innerText = row.cal
        file.appendChild(colcal)

        table.appendChild(file)
    })
}
