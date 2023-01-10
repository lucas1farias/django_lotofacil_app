

function reloadPage() {
    return window.location.reload()
}

function isCheckboxChecked({elName}) {
    if (document.getElementById(elName).checked) {
      console.log('SELECIONADO')
    } else {
      console.log('NÃO SELECIONADO')
    }
}

function char() {
    let chars = 'abcdef'
    let numbers = '0123456789'
    let hexadecimal = []

    for (let index of chars) {
      hexadecimal.push(index)
    }

    for (let index of numbers) {
      hexadecimal.push(index)
    }

    return hexadecimal[Math.floor(Math.random() * hexadecimal.length)]
}

function rgbHexa() {
    return `#${char()}${char()}${char()}${char()}${char()}${char()}`
}

function collectDataFromGame({target}) {
    let lotteryNumbers = [...Array(26).keys()]
    lotteryNumbers.splice(0, 1)

    let gameStringShaped = target.textContent.replace('[', '').replace(']', '').replaceAll(',', '').split(' ')
    let gameArrayShaped = []
    gameStringShaped.forEach(stringNumber => {
      gameArrayShaped.push(+stringNumber)
    })
    return gameArrayShaped
}

let changeBackgroundEl = document.getElementById('change-background')
let newGameEl = document.getElementById('new-game')
let reloadTagEl = document.getElementById('reload-msg')
let reportEl = document.getElementById('report')
let resultEl = document.getElementById('result')
let olEl = document.getElementById('game-data')
let divGame = document.querySelector('.new-game')
let divLastGame = document.querySelector('.last-game')
let newGameData = collectDataFromGame({target: divGame})
let lastGameData = collectDataFromGame({target: divLastGame})

// <section id="featured-games">
let divLastGameView = document.getElementById('last-game-view')
let divNewGameView = document.getElementById('new-game-view')

// [html: Novo jogo] jogo novo formatado p/ formato de esferas
for (let i = 0; i < newGameData.length; i++) {
    let newTagDiv = document.createElement('span')

    if (newGameData[i] > 9) {
      newTagDiv.textContent = newGameData[i]
    } else {
      newTagDiv.textContent = `0${newGameData[i]}`
    }

    newTagDiv.className = 'number-cell'
    newTagDiv.style.color = 'yellow'
    newTagDiv.style.fontWeight = 'bold'
    newTagDiv.style.backgroundColor = 'black'
    newTagDiv.style.margin = '.2rem'
    newTagDiv.style.padding = '.5rem'
    newTagDiv.style.borderRadius = '50%'
    newTagDiv.style.boxShadow = '0 0 10px white'
    newTagDiv.style.textAlign = 'center'
    divNewGameView.appendChild(newTagDiv)
}

// [html: Último jogo] último jogo formatado p/ formato de esferas
for (let i = 0; i < lastGameData.length; i++) {
    let newTagDiv = document.createElement('span')

    if (lastGameData[i] > 9) {
      newTagDiv.textContent = lastGameData[i]
    } else {
      newTagDiv.textContent = `0${lastGameData[i]}`
    }

    newTagDiv.className = 'number-cell'
    newTagDiv.style.color = 'black'
    newTagDiv.style.fontWeight = 'bold'
    newTagDiv.style.backgroundColor = 'yellow'
    newTagDiv.style.margin = '.2rem'
    newTagDiv.style.padding = '.5rem'
    newTagDiv.style.borderRadius = '50%'
    newTagDiv.style.boxShadow = '0 0 10px white'
    newTagDiv.style.textAlign = 'center'
    divLastGameView.appendChild(newTagDiv)
}

// todo: Novo
var root = document.compatMode =='BackCompat' ? document.body : document.documentElement
var hasVerticalScrollbar = root.scrollHeight>root.clientHeight
var hasHorizontalScrollbar = root.scrollWidth>root.clientWidth
let windowEl = document.querySelector('.window-properties')

let loop = setInterval(() => {
  
  // todo: Novo
  // -------------------------------------------------------------------------------------------------------------------
  let width  = windowEl.innerWidth || document.documentElement.clientWidth ||
  document.body.clientWidth;
  let height = windowEl.innerHeight|| document.documentElement.clientHeight||
  document.body.clientHeight;

  // Detectar barra de rolagem vertical
  if (hasVerticalScrollbar) {
    console.log('Sim')
    windowEl.textContent = `${width + 17}, ${height}`
  } else {
    windowEl.textContent = `${width}, ${height}` 
  }
  // -------------------------------------------------------------------------------------------------------------------

  // [html: Mudar plano de fundo]
  changeBackgroundEl.addEventListener('click', () => {
    let mainTagEl = document.getElementById('main-tag')
    mainTagEl.style.backgroundImage = `radial-gradient(${rgbHexa()}, ${rgbHexa()}, ${rgbHexa()})`
  })

  newGameEl.addEventListener('click', () => {
    reloadPage()
  })
  
  if (reportEl.textContent === 'False') {
    reportEl.textContent = ''
    reloadTagEl.textContent = 'Criando o jogo...'
    reloadPage()
  } else {
    clearInterval(loop)
  }

}, 1)

reloadTagEl.textContent = 'Jogo aprovado'
