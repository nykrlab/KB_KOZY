const API_KEY="d2c902d6ac6326cbb6156dacfebcb420"

function onGeoOk(position){
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;
    const url = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${API_KEY}&units=metric`;
    fetch(url).then(response => response.json()).then(data => {
        const temp = document.querySelector("#temp")
        const weather = document.querySelector("#weather")
        const tempMin = document.querySelector("#tempMin")
        const tempMax = document.querySelector("#tempMax")

        temp.innerHTML = `${Math.round(data.main.temp)}<em>o</em>`
        weather.innerHTML = `${data.weather[0].main}`
        tempMin.innerHTML = `${Math.round(data.main.temp_min)}<b>o</b>`
        tempMax.innerHTML = `${Math.round(data.main.temp_max)}<b>o</b>`
        });
}
function onGeoError(){
    alert("Can't find you. No weather for you")
}

navigator.geolocation.getCurrentPosition(onGeoOk,onGeoError)