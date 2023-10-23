// timer de 60 min

var tempoInicial = 60;

var tempoMilissegundos = tempoInicial * 60 * 1000;

function atualizarContador() {
    if (document.hasFocus()){
        var minutos = Math.floor(tempoMilissegundos / 1000 / 60);
        var segundos = Math.floor((tempoMilissegundos % (1000 * 60)) / 1000);
    
        minutos = minutos < 10 ? "0" + minutos : minutos;
        segundos = segundos < 10 ? "0" + segundos : segundos;
        document.getElementById("logoutTimer").textContent = ` ${minutos}:${segundos}`;
    
        tempoMilissegundos -= 1000;
    
        if (tempoMilissegundos < 0) {
           window.location.href = '/admin/logout' 
        }
    }
}

var contadorInterval = setInterval(atualizarContador, 1000);

function reiniciarContador() {
    document.getElementById("logoutTimer").textContent = " 60:00";
    clearInterval(contadorInterval);
    tempoMilissegundos = tempoInicial * 60 * 1000;
    contadorInterval = setInterval(atualizarContador, 1000);
}
  
document.addEventListener("mousemove", reiniciarContador);