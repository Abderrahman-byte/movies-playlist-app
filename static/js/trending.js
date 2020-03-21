const container = document.getElementById('tending_list_container')
const playlistModel = document.getElementById('playlist_model_body')

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

const addMovieToPlaylist = (playlist, movie) => {
    const url = `/api/playlist/add/${playlist.uid}/`
    const data = {'item_id': movie.id, 'media_type': movie.media_type}

    fetch(url, { method: 'POST', body: JSON.stringify(data)})
    .then(() => {
        const closeBtn = document.getElementById('close_model')
        closeBtn.click()
    }).catch(err => console.log(err))
}

const renderPlaylistBtn = (playlist, movie) => {
    const btn = document.createElement('button')
    btn.className = 'btn btn-info'
    btn.textContent = `add to ${playlist.title}`

    btn.addEventListener('click', () => {
        addMovieToPlaylist(playlist, movie)
    })

    const btnDiv = document.createElement('div')
    btnDiv.className = 'row my-1 px-2'
    btnDiv.appendChild(btn)

    return btnDiv
}

const renderCreatePlBtn = () => {
    const btn = document.createElement('a')
    btn.className = 'btn btn-secondary'
    btn.textContent = 'Create new playlist'
    btn.href = '/playlists/add/'

    const btnDiv = document.createElement('div')
    btnDiv.className = 'row my-1 px-2'
    btnDiv.appendChild(btn)

    return btnDiv
}

const showPlaylists = (movie) => {
    fetch('/api/playlists_lite/')
    .then(res => res.json())
    .then(data => {
        playlistModel.innerHTML = ''
        data.forEach(playlist => {
            playlistModel.appendChild(renderPlaylistBtn(playlist, movie))
        })
        
        playlistModel.appendChild(renderCreatePlBtn())
    })
    .catch(err => console.log(err))
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
    addToBtn.setAttribute('data-toggle', 'modal')
    addToBtn.setAttribute('data-target', '#playlist_model')

    addToBtnCol.appendChild(addToBtn)
    addToBtn.addEventListener('click', () => {
        showPlaylists(movie)
    })

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