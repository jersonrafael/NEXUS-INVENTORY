
document.addEventListener("keyup", e=>{

    // e.target.matches('#buscador')

    // console.log(e.target.value)
    if (e.target.matches("#buscador")){
  
        // if (e.key ==="Escape")e.target.value = ""
  
        document.querySelectorAll("#producto").forEach(fruta =>{
  
            fruta.textContent.toLowerCase().includes(e.target.value.toLowerCase())
              ?fruta.classList.remove("filtro")
              :fruta.classList.add("filtro")
        })
  
    }
  
  
  })