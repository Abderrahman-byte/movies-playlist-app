const container = document.getElementById('tending_list_container')

let currentDataPage = 1

const renderMovie = (movie) => {
    const posterCol = document.createElement('td')

    if(movie.poster_path !== null) {
        posterCol.innerHTML = `<img class='poster' alt="${movie.title || movie.name}" src="https://image.tmdb.org/t/p/w200${movie.poster_path}" />`
    } else {
        posterCol.innerHTML = `<img class='poster' src="null" alt='No Image' />`
    }

    const titleCol = document.createElement('td')
    titleCol.innerHTML = `<h5>${movie.title || movie.name}</h5>`

    const mediaTypeCol = document.createElement('td')
    mediaTypeCol.textContent = movie.media_type == 'movie' ? 'Movie': 'Tv Show'

    const releaseDateCol = document.createElement('td')
    releaseDateCol.textContent = movie.release_date

    const voteCol = document.createElement('td')
    voteCol.textContent = movie.vote_average

    const detailBtnCol = document.createElement('td')
    detailBtnCol.innerHTML = `<a class="btn btn-info" href="#">Details</a>`

    const addToBtnCol = document.createElement('td')
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
    const res = await getTrends()
    setupUI(res)
}

addEventListener('DOMContentLoaded', loadContent)