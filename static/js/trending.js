const container = document.getElementById('tending_list_container')

let currentDataPage = 1
let isLoading = false

const renderSkeltons = () => {
    for(let i= 0; i < 20; i++) {
        html = `<tr class='skelton_row'>
            <th scope="col"><span class="skelton_poster"></span></th>
            <th scope="col"><span class="skelton"></span></th>
            <th scope="col"><span class="skelton"></span></th>
            <th scope="col"><span class="skelton"></span></th>
            <th scope="col"><span class="skelton"></span></th>
            <th scope="col"></th>
            <th scope="col"></th>
        </tr>`

        container.innerHTML += html
    }
}

const removeSkeltons = () => {
    const skeltons = document.querySelectorAll('.skelton_row')
    skeltons.forEach(skelton => {
        skelton.parentNode.removeChild(skelton)
    })
}

const renderMovie = (movie) => {
    const posterCol = document.createElement('td')

    if(movie.poster_path !== null) {
        posterCol.innerHTML = `<img class='poster' alt="${movie.title || movie.name}" src="https://image.tmdb.org/t/p/w200${movie.poster_path}" />`
    } else {
        posterCol.innerHTML = `<img class='poster' src="null" alt='No Image' />`
    }

    const titleCol = document.createElement('td')
    titleCol.innerHTML = `<h5 class="row_title">${movie.title || movie.name}</h5>`

    const mediaTypeCol = document.createElement('td')
    mediaTypeCol.textContent = movie.media_type == 'movie' ? 'Movie': 'Tv Show'

    const releaseDateCol = document.createElement('td')
    releaseDateCol.className = 'no_break'
    releaseDateCol.textContent = movie.release_date || movie.first_air_date

    const voteCol = document.createElement('td')
    voteCol.textContent = movie.vote_average

    const detailBtnCol = document.createElement('td')
    detailBtnCol.innerHTML = `<a class="btn btn-info" href="#">Details</a>`

    const addToBtnCol = document.createElement('td')
    addToBtnCol.className = 'btn_row'
    const addToBtn = document.createElement('button')
    addToBtn.textContent = 'Add To'
    addToBtn.className = 'btn btn-primary'

    addToBtnCol.appendChild(addToBtn)

    const row = document.createElement('tr')
    row.setAttribute('data-id', movie.id)

    row.appendChild(posterCol)
    row.appendChild(titleCol)
    row.appendChild(mediaTypeCol)
    row.appendChild(releaseDateCol)
    row.appendChild(voteCol)
    row.appendChild(detailBtnCol)
    row.appendChild(addToBtnCol)

    container.appendChild(row)
}

const setupUI = (results) => {
    results.forEach(media => {
        renderMovie(media)
    });
}

const getTrends = async () => {
    url = `/api/trending/?page=${currentDataPage}`
    const request = await fetch(url)
    const response = await request.json()

    currentDataPage++

    return response.results
}

const loadContent = async () => {
    isLoading = true
    renderSkeltons()
    const res = await getTrends()
    removeSkeltons()
    isLoading = false
    setupUI(res)
}

addEventListener('DOMContentLoaded', loadContent)

addEventListener('scroll', () => {
    const height = document.documentElement.offsetHeight
    const offset = document.documentElement.scrollTop + window.innerHeight;

    if(!isLoading && offset >= height) {
        loadContent()
    }
})