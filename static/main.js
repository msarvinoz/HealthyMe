let elRegBtn = document.querySelector('.btn__1')
let elRegBtn2 = document.querySelector('.btn__2')
let elRegEnter = document.querySelector('#register')
let elLogin = document.querySelector('#login')
let elSingnUp = document.querySelector('#signup')
elRegBtn.addEventListener('click', ()=>{
    elRegEnter.style.display = 'none';
    elSingnUp.style.display = 'block';
}
)

elRegBtn2.addEventListener('click', ()=>{
    elRegEnter.style.display = 'none';
    elLogin.style.display= 'block'

}
)