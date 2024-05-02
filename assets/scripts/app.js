// const tg = window.Telegram.WebApp;

// Получаем данные пользователя при инициализации
// tg.ready();
function State(pageName, nextState) {
    this.page = pageName
    this.next = nextState
    return this
}
function updateState(page, prev) {
    window.history.replaceState(new State(prev, page), prev)
    window.history.pushState(new State(page), page)
}

const botUserName = 'bot_user_name'
let maxDescriptionLineLength = 35
let clicksRemaining = 1000
let maxClicks = 1000
let balance = 0
let tapStep = 1
const userId = 1    // tg.initDataUnsafe.user.id; // Используем user_id из данных Telegram

let energyLimitEl = document.getElementById('energy-all')
let energyEl = document.getElementById('energy-exists')
let balanceEl = document.getElementById('balance')
let energyIndicator = document.getElementById('energy-indicator')
let bonusEl = document.getElementById('bonus')
let detail = document.getElementById('detail')
let button = document.getElementById('btn-play')

function get_user(userId) {
    return {
        id: userId,
        name: 'test user name',
        icon: '/static/images/images.png'
    }
}

window.addEventListener(
    'popstate',
    (event) => {
        closeWindow(event)
    }
)

function updateEnergyIndicator() {
    energyIndicator.style.width = `${100 / maxClicks * (maxClicks - clicksRemaining)}%`
}

// Функция для обновления баланса пользователя
function updateBalance(newBalance) {
    balance = newBalance;
    balanceEl.innerText = `${balance}`
    updateEnergyIndicator()
}

// Функция для обновления знергии пользователя
function updateEnergy(energy, energyLimit) {
    clicksRemaining = energy
    maxClicks = energyLimit
    energyLimitEl.innerText = energyLimit
    energyEl.innerText = energy
    updateEnergyIndicator()
}

function showNotification(message) {
    let notif = document.getElementById('notification')
    notif.className += ' notification__active'
    notif.innerText = message
    setTimeout(() => {
        notif.className = notif.classList[0]
    }, 1250)
}

async function getButton() {
    let response = await fetch(`/api/user/${userId}/button/`)
    if (!response.ok) return false
    let data = await response.json()
    button.src = data.icon
}

class Game {
    constructor() {
        this.interval = setInterval(this.update, 5000)
        this.websocket = new WebSocket(`ws://${window.location.host}/user/ws/game/`);
        this.websocket.onopen = () => {this.websocket.send(userId); this.update()};
        this.websocket.onerror = this.onError
        this.websocket.onmessage = this.onMessage
        button.onclick = this.clickEgg
        getButton()
    }

    onError() {
        clearInterval(this.interval)
        document.body.innerHTML = `
        <div style="width: 100%; height: 100%; background-color: black; display: flex; justify-content: center; align-items: center">
            <h1 style="color: #AEAEAE; text-align: center">Убедитесь, что игра не запущена ещё где-то с вашего аккаунта.</h1>
        </div>
        `
    }

    update = () => {
        this.websocket.send('get_info')
    }

    clickEgg = (event) => {
        if (clicksRemaining <= 0) return;
        this.websocket.send('inc_balance');
        this.showClickFeedback(event)
    }

    onMessage = message => {
        let data = JSON.parse(message.data);
        tapStep = data.tap_step
        updateBalance(data.balance);
        updateEnergy(data.energy, data.energy_limit);
        updateEnergyIndicator();
        bonusEl.innerText = data.bonus
    }

    showClickFeedback = (event) => {
        const feedback = document.createElement('div');
        feedback.className += 'feedback'
        feedback.textContent = (clicksRemaining >= tapStep) ? `+${tapStep}` : `+${clicksRemaining}`;
        feedback.style.position = 'absolute'
        feedback.style.left = `calc(${event.clientX}px - 20px)`;
        feedback.style.top = `${event.clientY}px`;
        document.body.appendChild(feedback);
        setTimeout(() => feedback.remove(), 500)
    }
}

let game = new Game()

function formatDescription(messageText) {
    return messageText.replace('\n', '<br>')
}

async function openBoost(event) {
    updateState('detail', 'boost')
    let name = event.currentTarget.dataset.name
    let data = await (await fetch(`/api/user/${userId}/boost/${name}`)).json()
    detail.innerHTML = `
        <button class="detail__exit" onclick="window.history.back()">x</button>
        <div class="detail__info-block">
            <div class="detail__img-container">
                <img src="${data.icon}" alt="" class="detail__icon">
            </div>
            <div class="detail__description-block">
                <div class="detail__title">${data.name}</div>
                <div class="detail__short-description">${data.short_description??""}</div>
                <p class="detail__description">${formatDescription(data.description??"")}</p>
                <div class="detail__price-block">
                    <div class="detail__price">
                        <div class="detail__coin"><img class="detail__coin-icon" src="/static/images/hen-head.png" alt=""></div>
                        <span ${(data.price > balance)?'style="color: red"' : ""}>${data.price}</span>
                    </div>
                </div>
            </div>
        </div>
        <div class="detail__payment-block">
            <div class="detail__user-balance-block">
                <span>Твой баланс:</span>
                <span class="detail__user-balance">
                    <div class="detail__coin"><img class="detail__coin-icon" src="/static/images/hen-head.png" alt=""></div>
                    <span>${balance}</span>
                </span>
            </div>
            <div class="detail__buy-button" onclick="buyBust('${name}')">Купить</div>
        </div>
    `
    detail.className += ' detail_open'
}

async function buyBust(name) {
    let response = await fetch(`/api/user/${userId}/buy/${name}`)
    let data = await response.json()
    if (!response.ok) return showNotification(data.detail)
    showNotification(data.message)
    window.history.back()
    game.update()
    await getBoosts()
}

function renderBoost(boost, own) {
    let li = document.createElement('li')
    li.className = 'boost__item'
    if (!own) li.onclick = openBoost
    else li.onclick = selectButton
    let list = button.src.split('/')
    let name = list[list.length - 1].split('_')[0]
    let list2 = boost.icon.split('/')
    let name2 = list2[list2.length - 1].split('_')[0]
    console.log(name, name2)
    li.dataset.name = boost.name
    li.innerHTML = `
        <div class="boost__img-container">
            <img class="boost__icon" src="${boost.icon}" alt="">
        </div>
        <div class="boost__info${(own)? '_my': ''}">
            <span class="boost__name">${boost.name}</span>
            <div class="boost__price" ${(own)? 'style="display: none"': ''}>
                <div class="detail__coin"><img class="detail__coin-icon" src="/static/images/hen-head.png" alt=""></div>
                <span ${(boost.price > balance)?'style="color: red"' : ""}>${boost.price}</span>
            </div>
            ${(name === name2)? '<div class="boost__selected"></div>': ''}
        </div>
    `
    return li
}

function renderStep(user) {
        let li = document.createElement('li')
        li.className = 'detail__item'
        li.dataset.id = user.user_id
        let telegramUser = get_user(user)
        li.innerHTML =
        `
        <div class="statistic__img-container">
            <img width="90" height="90" class="detail__icon" src="${telegramUser.icon}" alt="">
        </div>
        <div class="detail__info">
            <span class="detail__name">${telegramUser.name}</span>
            <div class="statistic__level">
                <span class="statistic__id">id: ${user.user_id}</span>
                <span class="statistic__level">level: ${user.level}</span>
                <span class="statistic__balance">balance: ${user.balance}</span>
            </div>
        </div>
        `
        return li
}

async function getStatistics() {
    let response = await fetch(`/api/user/${userId}/statistics/`)
    let data = await response.json()
    if (!response.ok) showNotification(data.detail)
    let ul = document.createElement('ul')
    ul.className = 'detail__list'
    let statistics = data.map(renderStep)
    for (let li of statistics) ul.appendChild(li)
    if (statistics.length === 0) ul.innerHTML = `<div style="font-size: 25px; text-align: center; position: absolute; top: 40%; left: 50%; transform: translateX(-50%)">Statistics not found</div>`
    let content = document.createElement('div')
    content.className = 'detail__content'
    content.innerHTML =`<h1 class="detail__title" onclick="window.history.back()">↶ Рейтинг (топ: 100)</h1>`
    content.appendChild(ul)
    detail.innerHTML = ''
    detail.className = detail.className + " " + detail.classList[0] + '_open'
    detail.appendChild(content)
    updateState('detail', 'home')
}

async function copyToClipboard(src) {
    let textToCopy = document.getElementById(src).value
    // Navigator clipboard api needs a secure context (https)
    if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(textToCopy);
    } else {
        // Use the 'out of viewport hidden text area' trick
        const textArea = document.createElement("textarea");
        textArea.value = textToCopy;
        // Move textarea out of the viewport so it's not visible
        textArea.style.position = "absolute";
        textArea.style.left = "0";
        textArea.style.transform = 'translateX(-100%)'
        document.body.prepend(textArea);
        textArea.select();
        try {document.execCommand('copy');} catch (error) {console.error(error);} finally {textArea.remove();}
    }
    showNotification('copied')
}

async function getFriends() {
    let response = await fetch(`/api/user/${userId}/friends/`)
    let result = await response.json()
    let token = result.token
    let data = result.data
    if (!response.ok) showNotification(data.detail)
    let ul = document.createElement('ul')
    ul.className = 'detail__list'
    let friends = data.map(renderStep)
    for (let li of friends) ul.appendChild(li)
    if (friends.length === 0) ul.innerHTML = `<div style="font-size: 30px; text-align: center; position: absolute; top: 40%; left: 50%; transform: translateX(-50%)">Friends not found</div>`
    let content = document.createElement('div')
    content.className = 'detail__content'
    content.innerHTML =`
    <h1 class="detail__title" onclick="window.history.back()">↶ Друзья</h1>
    ${
        (token)?
        `<div class="ref-friends">
            <span class="ref-friends__title">Реферал:</span>
            <div class="ref-link">
                <input class="ref-link__token" type="button" id="token-src" value="https://t.me/${botUserName}?start=${token}" onclick="copyToClipboard(this.id)">
                <img class="ref-link__icon" src="/static/images/copy.png" class="copy-button" onclick="copyToClipboard('token-src')">
            </div>
        </div>
        `
        :
        ''
    }
    `
    content.appendChild(ul)
    detail.innerHTML = ''
    detail.className = detail.className + " " + detail.classList[0] + '_open'
    detail.appendChild(content)
    updateState('detail', 'home')
}

function renderTask(task) {
    let li = document.createElement('li')
    li.className = 'detail__item'
    li.dataset.id = task.name
    li.innerHTML =
    `
    <div class="statistic__img-container">
        <img width="90" height="90" class="detail__icon" src="${task.icon}" alt="">
    </div>
    <div class="detail__info">
        <a href="${task.link}" class="detail__name">${task.name}</a>
        <div class="statistic__info">
            ${(task.expires_at) ? `<span class="statistic__level">: ${task.expires_at}</span>` : ''}
            <span class="statistic__balance">bonus: ${task.payment}</span>
        </div>
    </div>
    `
    return li
}

async function getTaks() {
    let response = await fetch(`/api/user/${userId}/tasks/`)
    let data = await response.json()
    if (!response.ok) showNotification(data.detail)
    let ul = document.createElement('ul')
    ul.className = 'detail__list'
    let tasks = data.map(renderTask)
    for (let li of tasks) ul.appendChild(li)
    if (tasks.length === 0) ul.innerHTML = `<div style="font-size: 30px; text-align: center; position: absolute; top: 40%; left: 50%; transform: translateX(-50%)">Tasks not found</div>`
    let content = document.createElement('div')
    content.className = 'detail__content'
    content.innerHTML =`<h1 class="detail__title" onclick="window.history.back()">↶ Задание</h1>`
    content.appendChild(ul)
    detail.innerHTML = ''
    detail.className += " " + detail.classList[0] + '_open'
    detail.appendChild(content)
    updateState('detail', 'home')
}

async function getBoosts(event) {
    let response = await fetch(`/api/user/${userId}/boosts/my`)
    let response2 = await fetch(`/api/user/${userId}/boosts/new`)
    if (!response2.ok) showNotification('boosts not found')
    let data = await response.json()
    let data2 = await response2.json()
    let list = document.getElementById('boost-list')
    list.innerHTML = ''
    for (let boost of data) list.appendChild(renderBoost(boost, true))
    for (let boost of data2) list.appendChild(renderBoost(boost, false))
    let boostPage = document.getElementById('boost')
    boostPage.className = boostPage.className + " " + boostPage.className + "_open"
    updateState('boost', 'home')
}

function closeWindow(event) {
    if (event.state?.next === undefined) return
    let page = document.getElementById(event.state.next)
    page.className = page.classList[0]
    if (event.state?.page === 'home') game.update()
}

async function selectButton(event) {
    let name = event.currentTarget.dataset.name
    let response = await fetch(`/api/user/${userId}/select/${name}/`)
    if (response.ok) {
        getButton()
        showNotification(`${name} selected`)
    }
    else {
        let data = await response.json()
        showNotification(data.detail)
    }
    window.history.back()
}

document.getElementById('back-button').onclick = () => window.history.back()
document.getElementById('magazin').onclick = getBoosts
document.getElementById('statistics').onclick = getStatistics
document.getElementById('friends').onclick = getFriends
document.getElementById('task').onclick = getTaks
window.history.pushState(new State('home'), 'home')
