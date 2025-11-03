window.addEventListener('load', init)
        
function init() {
    console.log('Hello, World!')
    alert("odaa")
    document.querySelector('span').style.backgroundColor = 'rebeccapurple'

    document
        .querySelector('#myButton')
        .addEventListener('click', odaaaa)
}
function odaaaa() {
    document 
        .querySelector('span')
        .innerHTML = /*html*/ `<div style="background-color:orange; width: 50%;"> 
        <p> rica hamburguesa </p>
        <img src="https://imgs.search.brave.com/AYlqsM3CHhDf_QQx1vcsINvtDTc92_SIJsOg5YSU9So/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly9zdDMu/ZGVwb3NpdHBob3Rv/cy5jb20vMTMzNDk0/OTQvMzQ4NTMvaS80/NTAvZGVwb3NpdHBo/b3Rvc18zNDg1MzI3/MjQtc3RvY2stcGhv/dG8tYnVyZ2VyLWRh/cmstd29vZGVuLWN1/dHRpbmctYm9hcmQu/anBn" />
        </div>`
}