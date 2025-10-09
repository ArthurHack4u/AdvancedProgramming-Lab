windows.addEventListener('load', init);

function init(){
    console.log('hola')
    alert('oda');
    document.querySelector('span').style.backgroundColor = 'rebeccapurple';

    document
    .querySelector('#btn')
    .addEventListener('click', oda);
}
    function oda(){
    document
        .querySelector('span')
        .innerHTML = '<div style="background-color:orangered; width="50%> <p>Mis ricas papas</p> <img src="assets/images/papa.jpg"></img></div>'
}